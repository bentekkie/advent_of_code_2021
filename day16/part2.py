import abc
from operator import mul
from functools import reduce

from dataclasses import dataclass

byte_to_bits = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

@dataclass 
class Packet(abc.ABC):
    version: int
    id: int

    @abc.abstractmethod
    def apply(self) -> int:
        pass

@dataclass
class Literal(Packet):
    value: int

    def apply(self) -> int:
        return self.value

@dataclass
class Operator(Packet):
    sub_packets: list[Packet]

    def apply(self):
        sub_values = [p.apply() for p in self.sub_packets]
        if self.id == 0:
            return sum(sub_values)
        elif self.id == 1:
            return reduce(mul,sub_values,1)
        elif self.id == 2:
            return min(sub_values)
        elif self.id == 3:
            return max(sub_values)
        elif self.id == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self.id == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self.id == 7:
            return 1 if sub_values[0] == sub_values[1] else 0


def parse_packet(bits):
    version = int(bits[:3],base=2)
    id = int(bits[3:6], base=2)
    if id == 4:
        start = 6
        group = bits[start:start + 5]
        number_bits = ""
        while group[0] == "1":
            number_bits += group[1:]
            start += 5
            group = bits[start:start + 5]
        number_bits += group[1:]
        return Literal(version, id, int(number_bits, base=2)), start + 5
    else:
        length_id = bits[6]
        sub_packets = []
        if length_id == "0":
            total_subpacket_len = int(bits[7:22], base=2)
            start = 22
            end = start + total_subpacket_len
            while start < end:
                packet, len_used = parse_packet(bits[start:end])
                start += len_used
                sub_packets.append(packet)
        else:
            start = 18
            for _ in range(int(bits[7:18], base=2)):
                packet, len_used = parse_packet(bits[start:])
                start += len_used
                sub_packets.append(packet)
        return Operator(version, id, sub_packets), start

def to_bits(hex_str : str):
    return "".join(byte_to_bits[b] for b in hex_str)



with open("input.txt") as f:
    bits = to_bits(f.readline().strip())


packet, _ = parse_packet(bits)

print(packet.apply())