import re

DEBUG = False 

def recebeListaTuplas(linha):
    return [sum(map(int, m)) for m in re.findall(r'\((\d+),(\d+)\)', linha)] # Reggex da formatação inicial, coletando apenas o necessário e já guardando a soma

def maxPontos(pecas, i, j, dp):
    
    # Caso base: apenas uma peça restante
    if i == j:
        return pecas[i]
    
    # Se já foi calculado, retorna o valor memorizado, não calculando estados já calculados
    if dp[i][j] != -1:
        return dp[i][j]
    
    # Escolher a peça da esquerda (índice i) 
    # O oponente jogará otimamente no intervalo [i+1, j]
    escolhe_esquerda = pecas[i] - maxPontos(pecas, i + 1, j, dp) # ==> Vantagem de pontos tendo em vista a peça escolhida e o subarray acumulado
    
    # Escolher a peça da direita (índice j)
    # O oponente jogará otimamente no intervalo [i, j-1]
    escolhe_direita = pecas[j] - maxPontos(pecas, i, j - 1, dp) # ==> Vantagem de pontos tendo em vista a peça escolhida e o subarray acumulado
    
    # A dp vai armazenar o máximo valor entre os filhos direito e esquerdo da árvore, que está representada na do
    dp[i][j] = max(escolhe_esquerda, escolhe_direita)
    
    if DEBUG:
      print(f"dp[{i}][{j}] = {dp[i][j]} = max({escolhe_esquerda, escolhe_direita})")

    return dp[i][j]

numOfTestes = int(input())

for _ in range(numOfTestes):
    
    qntdPecas = int(input())
    pecas = recebeListaTuplas(input())

    if DEBUG:
      print(pecas)
    
    dp = [[-1] * qntdPecas for _ in range(qntdPecas)]

    # A recursão vai mme retornar a maior diferença de pontos entre Maria e João jogando otimamente
    diferencaMaxima = maxPontos(pecas, 0, qntdPecas - 1, dp)
    
    if DEBUG:
      for linha in dp:
        print(linha)

    soma_total = sum(pecas)

    if DEBUG:
      print(f"A soma de todas as peças é {soma_total} e a diferença máxima {diferencaMaxima}")

    # Maria = João + Diferença ==> Soma Total = Maria + Maria - Difereça ==> Maria = (Soma Total + Diferença)/2
    pontuacaoMaria = (soma_total + diferencaMaxima) // 2
    
    print(pontuacaoMaria)