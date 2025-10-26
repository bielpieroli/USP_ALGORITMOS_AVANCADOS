DEBUG = True
n = int(input())
vidas = list(map(int, input().split()))

if DEBUG:
    print(vidas)
    
# dp[i][0] é que eu vou quebrar esse bloco, considerando o mínimo do passado
# dp[i][1] é que eu considero que o bloco anterior foi quebrado + resto do dano de queda, ou que está no efeito cascata

dp = [[0,0] for _ in range(n+1)]

dp[0][0] = 0 
dp[0][1] = 1 

for i in range(1, n+1):
    altura = i-1
    
    # Altura é o número de relíquias abaixo dela
    # Resto é quanto de vida sobra se houver dano de queda 
    resto = vidas[altura] - altura if vidas[altura] - altura > 0 else 0

    if DEBUG:
        print(f"--- Iteração i={i} (Relíquia {altura}) ---")
        print(f"altura = {altura}, vidas = {vidas[altura]}, resto = {resto}")
    
    # dp[i][0]: Quebra o bloco, considerando o mínimo de antes
    dp[i][0] = min(dp[i-1][0], dp[i-1][1]) + vidas[altura]
    
    if DEBUG:
        print(f"dp[{i}][0] = {dp[i][0]} = min({dp[i-1][0]}, {dp[i-1][1]}) + {vidas[altura]}")
    
    
    # dp[i][1]: S[i-1] é
    # Opção 1: Custo anterior (considerando que quebrou o anterior) + dano de queda
    # Opção 2: Custo anterior (cascata) + a vida que tinha - 1 de dano tomado
    dp[i][1] = min(resto + dp[i-1][0], dp[i-1][1] + vidas[altura] -1) 

    if DEBUG:
        print(f"dp[{i}][1] = {dp[i][1]} = min({resto + dp[i-1][0]}, {dp[i-1][1] + vidas[altura] -1}) ")
        print(f"DP atual: {dp[i]}")

if DEBUG:
    print("--- Resultado Final (DP) ---")
    print(dp)

print(min(dp[n][0], dp[n][1]))
