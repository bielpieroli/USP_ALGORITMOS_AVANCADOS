# a fórmula é ((a ∗ t) mod p = 1), precisamos do valor de 'a'
# O Pequeno Teorema de Fermat estabelece que, se 'p' é primo e 'k' é um inteiro não divisível por 'p', então k^{p-1} = 1 (mod p). 
# Considerando que a * t = 1 (mod p) [fórmula dada], substituindo 'a' por t^{p-1} (o inverso multiplicativo), chega que t^{p-2} = 1 (mod p)
def inversoMultiplicativo(t,p):
  return pow(t, p-2, p)

# Cria uma lista com os números primos, a partir do crivo de booleanos
def crivoErastotenes(limit):
    if limit < 2:
        return []
    isPrime = [True] * (limit + 1)
    isPrime[0] = isPrime[1] = False

    # Itera sobre os números até srqt do limite, colocando todos os múltiplos dos números como não-primos
    for i in range(2, int(limit ** 0.5) + 1): 
        if isPrime[i]:
            for j in range(i * i, limit + 1, i):
                isPrime[j] = False 

    return [i for i, prime in enumerate(isPrime) if prime] # Cria uma lista com os números itself, ignorando aqueles que não são primos


# A função do 'nextPrime' utiliza do crivo de erastótenes segmentado, vendo os primos a partir daquele número num bloco
def nextPrime(n, tamanhoBloco=1000000):
    if n < 2:
        return 2
    if n == 2:
        return 3

    # Começa no próximo número ímpar (primos > 2 só podem ser ímpares)
    low = n + 1 if n % 2 == 0 else n + 2

    while True:
        high = low + tamanhoBloco - 1

        # Cria o crivo base até sqrt(high), ou seja, com os primos possíveis divisores até o limite superior
        limit = int(high ** 0.5) + 1
        possiveisDivisores = crivoErastotenes(limit)

        # Inicializa todos os números do intervalo [low, high] como primos
        primosIntervalo = [True] * (high - low + 1)

        # Constroi a lista de primos no intervalo, com base no mesmo príncipio do crivo
        for p in possiveisDivisores:
            begin = max(p * p, ((low + p - 1) // p) * p) # Note que aqui o begin, que é onde começa as iterações, pode mudar se avançarmos o bloco
            for j in range(begin, high + 1, p):
                primosIntervalo[j - low] = False

        # Retorna o primeiro número marcado como primo
        for i in range(high - low + 1):
            if primosIntervalo[i]:
                return low + i

        # Se não retornar nada, avançamos no bloco do crivo
        low += tamanhoBloco


numeroPrimo, t = map(int, input().strip().split())
print(inversoMultiplicativo(t, nextPrime(numeroPrimo)))