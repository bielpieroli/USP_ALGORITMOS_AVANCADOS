DEBUG = False

def debug(*args):
    if DEBUG:
        print(*args)


def ehPrefixo(s, sub):
    if len(sub) > len(s): 
        return False
    for i in range(len(sub)):
        if s[i] != sub[i]: 
            return False
    return True 


def ehSufixo(s, sub):
    if len(sub) > len(s):
        return False 
    diff = len(s) - len(sub)
    for i in range(len(sub)): 
        if s[diff + i] != sub[i]:
            return False
    return True 


def maiorPrefixSufix(s): 
    n = len(s)
    debug(f"\nString: '{s}'")

    for tam in range(n - 1, 0, -1): 
        sub = "" 
        for i in range(tam):
            sub += s[i]

        debug(f"Testando tamanho {tam}: '{sub}'")
 
        if ehPrefixo(s, sub) and ehSufixo(s, sub):
            debug(f">>> Achou: '{sub}'\n")
            return sub 

    debug(">>> Nenhum prefixo/sufixo encontrado\n")
    return ""

 
numOfTestes = int(input())

for _ in range(numOfTestes): 
    s = input().strip()
    print(maiorPrefixSufix(s))
 
  
