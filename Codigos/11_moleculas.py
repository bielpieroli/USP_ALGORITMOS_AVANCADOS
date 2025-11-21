DEBUG = False

def dfs(v, visitado, grafo):
    visitado[v] = True
    for vertice in grafo[v]:
        if not visitado[vertice]:
            dfs(vertice, visitado, grafo)

            
numOfTestes = int(input())
print(f"testes = {numOfTestes}") if DEBUG else ""

for _ in range(numOfTestes):

  qntdAtomos, qntdConexoes = map(int, input().strip().split())
  print(f"atomos = {qntdAtomos}, conexoes = {qntdConexoes}") if DEBUG else "" 
  
  grafo = [[] for _ in range(qntdAtomos + 1)]  

  for _ in range(qntdConexoes):
      elem1, elem2 = map(int, input().strip().split()) 
      grafo[elem1].append(elem2)
      grafo[elem2].append(elem1)
      print(f"  Conexão adicionada: {elem1} <-> {elem2}") if DEBUG else ""

  if DEBUG:
      print("\nGrafo montado:")
      for i in range(1, qntdAtomos + 1):
          print(f"  {i}: {grafo[i]}")  
    
  visitado = [False] * (qntdAtomos + 1)
  componentes = 0

  for v in range(1, qntdAtomos + 1):
      if not visitado[v]:
          dfs(v, visitado, grafo)
          componentes += 1

  print(componentes)