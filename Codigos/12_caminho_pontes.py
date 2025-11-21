DEBUG = False

def debug(*args):
    if DEBUG:
        print(*args)

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def addEdge(self, u, v, w):
        # debug(f"Adicionando aresta: {u+1} - {v+1} com custo {w}")
        self.graph.append([u, v, w])

    def find(self, parent, i):
        # debug(f"Find: procurando root de {i}, parent atual = {parent[i]}")
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        # debug(f"Union: unindo {x} e {y}")
        # debug(f"Rank antes: {rank}")

        # Attach smaller rank tree under root of 
        # high rank tree (Union by Rank) 
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        # If ranks are same, then make one as root 
        # and increment its rank by one 
        else:
            parent[y] = x
            rank[x] += 1

        # debug(f"Parent depois: {parent}")
        # debug(f"Rank depois: {rank}")

    def MST(self):
        result = []
        i = 0
        e = 0

        # debug("\n--- ORDENANDO ARESTAS ---")
        self.graph.sort(key=lambda item: item[2])
        # debug("Arestas ordenadas:", self.graph)

        parent = [node for node in range(self.V)]
        rank = [0] * self.V

        # debug(f"Parent inicial: {parent}")
        # debug(f"Rank inicial: {rank}\n")

        while e < self.V - 1:
            if i >= len(self.graph):
                debug("Sem arestas suficientes, ou seja, grafo desconexo")
                return None, None

            u, v, w = self.graph[i]
            # debug(f"Edge #{i}: {u+1} - {v+1}, custo {w}")
            i += 1

            x = self.find(parent, u)
            y = self.find(parent, v)
            # debug(f"Roots encontrados: {x}, {y}")

            if x != y:
                debug(f"Aceitando aresta {u+1}-{v+1}")
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            else:
                debug(f"Rejeitando aresta {u+1}-{v+1} (formaria ciclo)")

        custoTotal = sum(w for _, _, w in result)

        debug("\n--- MST FINAL ---")
        debug("Arestas da MST:", result)
        # debug("Custo total:", custoTotal)

        return custoTotal, result


numTestes = int(input())
# debug(f"Numero de testes: {numTestes}")

for _ in range(numTestes):

    numAcamp, numPontes = map(int, input().strip().split())
    # debug(f"\nTeste novo: {numAcamp} acampamentos, {numPontes} pontes")

    grafo = Graph(numAcamp)

    custosVistos = set()
    custoRepetido = False

    for _ in range(numPontes):
        ac1, ac2, custo = map(int, input().strip().split())
        # debug(f"Lido: ({ac1}, {ac2}) com custo {custo}")

        if custo in custosVistos:
            debug(f"Custo {custo} repetido!")
            custoRepetido = True
        custosVistos.add(custo)

        grafo.addEdge(ac1 - 1, ac2 - 1, custo)

    if custoRepetido:
        print("Esse nao e o caminho correto para a Cidade Perdida de Z.\n")
        continue

    custoTotal, arestasMST = grafo.MST()

    if custoTotal is None:
        print("O vale nao pode ser completamente atravessado.\n")
        continue

    print(f"Custo minimo: {custoTotal}")
    print("Pontes reconstruidas:")

    for u, v, custo in arestasMST:
        a, b = (u, v) if u < v else (v, u)
        print(f"{a+1} - {b+1}")

    print()
