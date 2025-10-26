import sys

def mergeSortCountInversoes(array):
    tamanho = len(array)
    if tamanho <= 1:
        return array, 0

    meio = tamanho // 2
    
    # Recursão em pré-ordem
    esquerdaOrdenada, inversoesEsquerda = mergeSortCountInversoes(array[:meio])
    direitaOrdenada, inversoesDireita = mergeSortCountInversoes(array[meio:])

    listaMesclada = []
    indiceEsquerda = indiceDireita = 0
    inversoesDivisao = 0

    while indiceEsquerda < len(esquerdaOrdenada) and indiceDireita < len(direitaOrdenada):
        if esquerdaOrdenada[indiceEsquerda] <= direitaOrdenada[indiceDireita]:
            listaMesclada.append(esquerdaOrdenada[indiceEsquerda])
            indiceEsquerda += 1
        else:
            # Houve inversão (ultrapassagem)
            listaMesclada.append(direitaOrdenada[indiceDireita])
            indiceDireita += 1
            inversoesDivisao += (len(esquerdaOrdenada) - indiceEsquerda)

    listaMesclada.extend(esquerdaOrdenada[indiceEsquerda:])
    listaMesclada.extend(direitaOrdenada[indiceDireita:])

    inversoesTotais = inversoesEsquerda + inversoesDireita + inversoesDivisao
    return listaMesclada, inversoesTotais


numTrechos = int(input())

resultados = []

for indiceTrecho in range(numTrechos):

    numJogadores = int(input())

    dadosJogadores = []

    # Recebe os dados dos kartistas
    for _ in range(numJogadores):
        linha = input()
        if not linha: 
            break
        posicaoInicial, posicaoFinal = map(int, linha.split())
        dadosJogadores.append((posicaoInicial, posicaoFinal))

    # Dá sort com base na posição inicial primeiramente
    dadosJogadores.sort(key=lambda x: x[0])

    arrayPosicaoFinal = [posicaoFinal for posicaoInicial, posicaoFinal in dadosJogadores]

    # Dá merge sort contando o número de inversões (ultrapassagens)
    _, numUltrapassagens = mergeSortCountInversoes(arrayPosicaoFinal)
    resultados.append((indiceTrecho, numUltrapassagens))

resultados.sort(key=lambda x: x[1], reverse=True)

for indiceT, numU in resultados:
    print(f"{indiceT} {numU}")