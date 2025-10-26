class Sistema:
    def __init__(self, id, x, y, ordem):
        """
        id: nome do sistema
        x: coordenada em x
        y: coordenada em y
        ordem: indice no qual o sistema estava na entrada
        """
        self.id = id
        self.x = x
        self.y = y
        self.ordem = ordem 

    def getCoords(self):
        return self.x, self.y


class ClosestPair:
    def __init__(self, sistema1="", sistema2="", distancia=float('inf'), ordem1=float('inf'), ordem2=float('inf')):
        """
        sistema1: nome do sistema 1
        sistema2: nome do sistema 2
        distancia: distância entre eles
        ordem1: índice da posição do input do sistema 1
        ordem2: índice da posição do input do sistema 2
        """
        self.sistema1 = sistema1
        self.sistema2 = sistema2
        self.distancia = distancia
        self.ordem1 = ordem1
        self.ordem2 = ordem2

    def getSystems(self):
        return self.sistema1, self.sistema2
    
    def getDistance(self):
        return self.distancia
    
    def __lt__(self, outro):
        if self.distancia != outro.distancia:
            return self.distancia < outro.distancia
        
        ordem1_self = self.ordem1 if self.ordem1 is not None else float('inf')
        ordem2_self = self.ordem2 if self.ordem2 is not None else float('inf')
        ordem1_outro = outro.ordem1 if outro.ordem1 is not None else float('inf')
        ordem2_outro = outro.ordem2 if outro.ordem2 is not None else float('inf')

        return (ordem1_self, ordem2_self) < (ordem1_outro, ordem2_outro)


class ConjuntoDisjunto:
    def __init__(self, n):
        self.pai = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.pai[x] != x:
            self.pai[x] = self.find(self.pai[x])
        return self.pai[x]
    
    def uniao(self, x, y):
        raizX = self.find(x)
        raizY = self.find(y)
        if raizX == raizY:
            return False
        if self.rank[raizX] < self.rank[raizY]:
            self.pai[raizX] = raizY
        elif self.rank[raizX] > self.rank[raizY]:
            self.pai[raizY] = raizX
        else:
            self.pai[raizY] = raizX
            self.rank[raizX] += 1
        return True

def calcularDistancia(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return(dx * dx + dy * dy)**(1/2) 

def kruskalMst(sistemasImportantes, tensaoMaxima):
    n = len(sistemasImportantes)
    arestas = []
    
    # Busca pelas distâncias que estão dentro do limite
    for i in range(n):
        for j in range(i + 1, n): # O I+1 reduz a quantidade de iterações, evitando repetições e comparações desnecessárias e/ou repetidas

            dist = calcularDistancia(sistemasImportantes[i], sistemasImportantes[j])

            if dist <= tensaoMaxima:
                sis1, sis2 = sistemasImportantes[i], sistemasImportantes[j]

                if sis1.ordem > sis2.ordem:
                    sis1, sis2 = sis2, sis1

                arestas.append(ClosestPair(sis1.id, sis2.id, dist, sis1.ordem, sis2.ordem))
    
    # Dá sort e monsta um conjunto disjunto, retornando-o
    arestas.sort()
    conjunto = ConjuntoDisjunto(n)
    mst = []
    indiceSistema = {sistemasImportantes[i].id: i for i in range(n)}
    
    for aresta in arestas:
        idx1 = indiceSistema[aresta.sistema1]
        idx2 = indiceSistema[aresta.sistema2]
        if conjunto.uniao(idx1, idx2):
            mst.append(aresta)
            if len(mst) == n - 1:
                break

    return mst


def faixaMaisProxima(faixa, d):

    maisProximo = ClosestPair(distancia=d)
    faixa.sort(key=lambda s: s.y)

    for i in range(len(faixa)):
        j = i + 1
        while j < len(faixa) and (faixa[j].y - faixa[i].y) < maisProximo.getDistance():
            dist = calcularDistancia(faixa[i], faixa[j])
            sis1, sis2 = faixa[i], faixa[j]

            # Troca de acordo com a ordenação da entrada
            if sis1.ordem > sis2.ordem:
                sis1, sis2 = sis2, sis1

            # Se a distância for menor, troca
            if (dist < maisProximo.getDistance() or
            
            # Se a distância for igual, dá prioridade para quem estava primeiro na entrada
                (dist == maisProximo.getDistance() and (sis1.ordem, sis2.ordem) < (maisProximo.ordem1, maisProximo.ordem2))):
                maisProximo = ClosestPair(sis1.id, sis2.id, dist, sis1.ordem, sis2.ordem)

            j += 1
    return maisProximo


def closestPairRecursive(sistemasX, sistemasY):

    n = len(sistemasX)

    # Caso base da recursão
    if n <= 3:
        minPar = ClosestPair()

        for i in range(n):
            for j in range(i+1, n): # O I+1 reduz a quantidade de iterações, evitando repetições e comparações desnecessárias e/ou repetidas

                sis1, sis2 = sistemasX[i], sistemasX[j]
                dist = calcularDistancia(sis1, sis2)

                # Ajusta a ordem entre sis1 e sis2 de acordo com a entrada
                if sis1.ordem > sis2.ordem:
                    sis1, sis2 = sis2, sis1
                
                # A distância é menor
                if (dist < minPar.getDistance() or 
                    # A mesma distância e tem prioridade na ordem de entrada
                    (dist == minPar.getDistance() and 
                     (sis1.ordem, sis2.ordem) < (minPar.ordem1, minPar.ordem2))):
                    minPar = ClosestPair(sis1.id, sis2.id, dist, sis1.ordem, sis2.ordem)

        return minPar

    # Divisão e conquista
    meio = n // 2

    pontoMeio = sistemasX[meio]

    # Divisão à metade com base em X 
    esquerdaX = sistemasX[:meio]
    direitaX = sistemasX[meio+1:]

    # Divide considerando o ponto de meio de X
    esquerdaY = [s for s in sistemasY if s.x <= pontoMeio.x]
    direitaY = [s for s in sistemasY if s.x > pontoMeio.x]

    # Propaga a recursão verificadndo à direita e à esquerda qual apresenta menor distância
    maisProximoEsq = closestPairRecursive(esquerdaX, esquerdaY)
    maisProximoDir = closestPairRecursive(direitaX, direitaY)

    # Verifica o mínimo entre os dois
    minimoAtual = maisProximoEsq if maisProximoEsq < maisProximoDir else maisProximoDir


    faixa = [s for s in sistemasY if abs(s.x - pontoMeio.x) < minimoAtual.getDistance()]
    faixaProxima = faixaMaisProxima(faixa, minimoAtual.getDistance())

    return faixaProxima if faixaProxima < minimoAtual else minimoAtual


def findClosestPair(sistemas):

    # Se não existir sistemas, ou houver apenas 1, não existe a possibilidade sequer de formar um par
    if len(sistemas) <= 1:
        return ClosestPair()
    
    # Ordena por cada tipo de coordenada

    sistemasX = sorted(sistemas, key=lambda s: s.x)
    sistemasY = sorted(sistemas, key=lambda s: s.y)

    # Inicia a divisão e conquista recusriva
    return closestPairRecursive(sistemasX, sistemasY)


numProblemas = int(input())

for _ in range(numProblemas):

    # Recebe as informações de entrada
    totalSistemas, qtdImportantes, tensaoMaxima = input().split()
    totalSistemas = int(totalSistemas)
    qtdImportantes = int(qtdImportantes)
    tensaoMaxima = float(tensaoMaxima)

    todosSistemas = []
    sistemasImportantes = []

    for i in range(totalSistemas):

        # Criando o sistema
        idSistema, x, y = input().split()
        x, y = float(x), float(y)
        sistema = Sistema(idSistema, x, y, i)

        # No closestPair, precisa de todos
        todosSistemas.append(sistema)

        # Deve adicionar apenas os 'qtdImportantes' primeiros para o kruskalMst
        if i < qtdImportantes:
            sistemasImportantes.append(sistema)

    # Primeira parte é com kruskal
    mst = kruskalMst(sistemasImportantes, tensaoMaxima)
   

   # Segunda parte é com closestPair
    maisProximo = findClosestPair(todosSistemas)
    dist = maisProximo.getDistance()

    # Se não houver distância mais próxima, deixa de printar coisas
    if dist == float('inf'):
        maisProximo.sistema1 = ""
        maisProximo.sistema2 = ""
        dist = ""


    for aresta in mst:
        sis1, sis2 = aresta.getSystems()
        print(f"{sis1}, {sis2}, {aresta.getDistance():.2f}")

    print(f"Ponto de Ressonância: {maisProximo.sistema1}, {maisProximo.sistema2}, {dist:.2f}\n")
