from dijkstar import Graph, find_path

graph = Graph()

with open("inputex.txt") as f:
    max_i = 0
    max_j = 0
    for i,line in enumerate(f.readlines()):
        max_i = i
        for j,weight in enumerate(line.strip()):
            max_j = j
            graph.add_edge((i-1,j),(i,j), int(weight))
            graph.add_edge((i+1,j),(i,j), int(weight))
            graph.add_edge((i,j-1),(i,j), int(weight))
            graph.add_edge((i,j+1),(i,j), int(weight))

path = find_path(graph,(0,0),(max_i,max_j))

print(path.total_cost)