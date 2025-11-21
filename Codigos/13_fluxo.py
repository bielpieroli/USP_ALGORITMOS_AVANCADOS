DEBUG = False

def debug(*args):
    if DEBUG:
        print(*args)


from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        self.capacity = [[0]*vertices for _ in range(vertices)]

    def addEdge(self, u, v, w):
        debug(f"Adicionando aresta: {u+1} -> {v+1} com capacidade {w}")
        self.graph[u].append(v)
        self.graph[v].append(u) # aresta reversa para fluxo residual
        self.capacity[u][v] += w

    def bfs(self, source, target, parent):
        visited = [False] * self.V
        dequeGraph = deque([source])
        visited[source] = True
        parent[source] = -1

        while dequeGraph:
            u = dequeGraph.popleft()

            for v in self.graph[u]:
                if not visited[v] and self.capacity[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    dequeGraph.append(v)

                    if v == target:
                        return True

        return False

    def maxFlow(self, source, target):
        parent = [-1] * self.V
        fluxoTotal = 0

        while self.bfs(source, target, parent):
            caminho = float('inf')
            v = target
            while v != source:
                u = parent[v]
                caminho = min(caminho, self.capacity[u][v])
                v = u

            debug(f"Aumentando fluxo em {caminho}")

            v = target
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= caminho
                self.capacity[v][u] += caminho
                v = u

            fluxoTotal += caminho

        return fluxoTotal

vertices, arestas = map(int, input().split())
debug(f"vertices = {vertices}, arestas = {arestas}")
grafo = Graph(vertices)

for _ in range(arestas):
    comp1, comp2, peso = map(int, input().split())
    debug(f"[{comp1}] <== {peso} ==> [{comp2}]")
    grafo.addEdge(comp1 - 1, comp2 - 1, peso)

fluxoMax = grafo.maxFlow(0, vertices - 1)

print(fluxoMax)