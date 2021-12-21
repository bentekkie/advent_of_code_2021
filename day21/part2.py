from collections import Counter, defaultdict

with open("input.txt") as f:
    p1 = int(f.readline().strip()[-1])
    p2 = int(f.readline().strip()[-1])

turn = Counter(a+b+c for a in range(1,4) for b in range(1,4) for c in range(1,4))


wins = [0,0]
scores : dict[tuple[tuple[int,int],tuple[int,int],int],int] = {((p1,p2),(0,0)):1}

def is_win(player: int, score : tuple[tuple[int,int],...]):
    return sum(s[player] for s in score[1:]) >= 21

def fix(s : int):
    return s if s <= 10 else s-10

found_wins = {}

changed = True
whos_turn = 0
while len(scores):
    changed = False
    new_scores = defaultdict(int)
    for ((p1_last_pos,p2_last_pos),(p1_total_score,p2_total_score)),num_games in scores.items():
        for new_turn,new_games in turn.items():
            if whos_turn:
                new_pos = (p1_last_pos, fix(p2_last_pos+new_turn))
                new_score = (p1_total_score,p2_total_score+new_pos[1])
            else:
                new_pos = (fix(p1_last_pos+new_turn), p2_last_pos)
                new_score = (p1_total_score+new_pos[0],p2_total_score)
            new_total_games = num_games * new_games
            if new_score[whos_turn] >= 21:
                wins[whos_turn] += new_total_games
            else:
                new_scores[new_pos,new_score] += new_total_games
    scores = new_scores
    whos_turn = (whos_turn + 1) % 2
    print(wins,len(scores))

print(max(wins))