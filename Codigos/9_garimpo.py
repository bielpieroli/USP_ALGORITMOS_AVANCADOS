DEBUG = False

numFases = int(input()) 

for fase in range(numFases):
    
    numDiamantes = int(input())  
    numDias = int(input())  
    valores = list(map(int, input().split())) 

    if DEBUG:
        print(f"\n=== Fase {fase+1} ===")
        print(f"Diamantes iniciais: {numDiamantes}")
        print(f"Valores: {valores}")
        print("-"*15)

    # dp[i][0] -> sem passe
    # dp[i][1] -> com passe
    # dp[i][2] -> descansando (após garimpo)

    # Inicializa-se tudo com - infinito e com o valor inicial de dimas
    dp = [[float('-inf')] * 3 for _ in range(numDias + 2)]
    dp[0][0] = numDiamantes  

    # A dp aqui utiliza 'i' como variável considerando-a como dia anterior, portanto, calcula-se sempre 'i+1' com base em i, para que projetemos o futuro no passado (dp)

    for i in range(numDias):
        # Estados do dia "anterior"
        dpDiaAnterior = dp[i][:]

        if DEBUG:
            print(f"\n--- Dia {i} ---")
            print(f"Valor do dia: {valores[i]}")
            print(f"Estado atual dp[{i}] = {dp[i]}")

        # Estado 0: sem passe
        if dpDiaAnterior[0] != float('-inf'):
            # 1) Pular o dia
            dp[i+1][0] = max(dp[i+1][0], dpDiaAnterior[0])
            if DEBUG:
                print(f"Sem passe -> Pula dia: dp[{i+1}][0] = {dp[i+1][0]}")

            # 2) Comprar passe (se tiver dimas suficientes)
            if dpDiaAnterior[0] - valores[i] >= 0:
                dp[i+1][1] = max(dp[i+1][1], dpDiaAnterior[0] - valores[i])
                if DEBUG:
                    print(f"Sem passe -> Compra passe: dp[{i+1}][1] = {dp[i+1][1]} (gastou {valores[i]})")

        # Estado 1: com passe
        if dpDiaAnterior[1] != float('-inf'):
            # 1) Pular o dia mantendo o passe
            dp[i+1][1] = max(dp[i+1][1], dpDiaAnterior[1])
            if DEBUG:
                print(f"Com passe -> Pula dia: dp[{i+1}][1] = {dp[i+1][1]}")

            # 2) Garimpar -> vai para descanso no dia seguinte
            if i <= numDias + 1: # Note que depois de garimpar, você deve ter um dia para descansar, por isso, +1
                dp[i+1][2] = max(dp[i+1][2], dpDiaAnterior[1] + valores[i])
                if DEBUG:
                    print(f"Com passe -> Garimpa: dp[{i+1}][2] = {dp[i+1][2]} (ganhou {valores[i]})")

        # Estado 2: descansando
        if dpDiaAnterior[2] != float('-inf'):
            # volta para livre sem passe no próximo dia
            dp[i+1][0] = max(dp[i+1][0], dpDiaAnterior[2])
            if DEBUG:
                print(f"Descansando -> volta livre: dp[{i+1}][0] = {dp[i+1][0]}")

    # Resultado final: max dos estados no último dia, fruto do caminho que maximiza o passado
    resultado = max(dp[numDias][0], dp[numDias][1], dp[numDias][2])
    print(resultado)

    if DEBUG:
        print("\n--- DP Final ---")
        for i in range(numDias+1):
            print(f"Dia {i}: {dp[i]}")
        print(f"Resultado final: {resultado}")
        print("==============================\n")
