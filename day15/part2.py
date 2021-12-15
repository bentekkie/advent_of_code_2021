from dijkstar import Graph, find_path
import numpy as np
graph = Graph()


def add_edge(i, j, weight):
    graph.add_edge((i-1, j), (i, j), int(weight))
    graph.add_edge((i+1, j), (i, j), int(weight))
    graph.add_edge((i, j-1), (i, j), int(weight))
    graph.add_edge((i, j+1), (i, j), int(weight))


with open("input.txt") as f:
    original_grid = np.matrix([[int(w) for w in line.strip()]
                              for line in f.readlines()])

vinc = np.vectorize(lambda x: x+1 if x+1 < 10 else 1)


col = np.vstack((
    original_grid,
    vinc(original_grid),
    vinc(vinc(original_grid)),
    vinc(vinc(vinc(original_grid))),
    vinc(vinc(vinc(vinc(original_grid)))),
)
)

full = np.hstack((
    col,
    vinc(col),
    vinc(vinc(col)),
    vinc(vinc(vinc(col))),
    vinc(vinc(vinc(vinc(col)))),
)
)

for (i, j), weight in np.ndenumerate(full):
    add_edge(i, j, weight)

print(find_path(graph, (0, 0), (full.shape[0]-1, full.shape[1]-1)).total_cost)
