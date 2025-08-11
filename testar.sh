#!/bin/bash

# Verifica se o programa e a pasta de testes foram passados como argumentos
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <programa.py> <pasta_de_testes>"
    exit 1
fi

programa=$1
pasta_testes=$2

# Verifica se o arquivo Python existe
if [ ! -f "$programa" ]; then
    echo "Erro: Programa '$programa' não encontrado."
    exit 1
fi

# Verifica se a pasta de testes existe
if [ ! -d "$pasta_testes" ]; then
    echo "Erro: Pasta de testes '$pasta_testes' não encontrada."
    exit 1
fi

# Contadores para os resultados
PASSARAM=0
FALHARAM=0
ERROS=0
TEMPO_TOTAL=0

# Itera sobre os arquivos de teste na pasta (ordenando numericamente)
for entrada in $(ls "$pasta_testes"/in/*.in | sort -V); do
    nome_base=$(basename "$entrada" .in)
    saida_esperada="$pasta_testes/out/$nome_base.out"

    # Verifica se o arquivo de saída esperada existe
    if [ ! -f "$saida_esperada" ]; then
        echo "Aviso: Arquivo de saída esperado '$saida_esperada' não encontrado. Pulando teste."
        continue
    fi

    echo "============================================="
    echo "Executando teste '$nome_base'..."
    echo "============================================="

    # Mede o tempo de execução
    start_time=$(date +%s.%N)
    
    # Executa o programa Python
    python3 "$programa" < "$entrada" > saida_obtida.tmp 2> erros.tmp
    status=$?
    
    end_time=$(date +%s.%N)
    elapsed_time=$(echo "$end_time - $start_time" | bc)
    TEMPO_TOTAL=$(echo "$TEMPO_TOTAL + $elapsed_time" | bc)

    # Verifica se houve erro na execução
    if [ $status -ne 0 ]; then
        echo "🔴 Teste '$nome_base': ERRO (código $status)"
        cat erros.tmp
        ERROS=$((ERROS + 1))
        FALHARAM=$((FALHARAM + 1))
        rm -f saida_obtida.tmp erros.tmp
        continue
    fi

    # Compara a saída obtida com a saída esperada, ignorando espaços e quebras de linha extras
    if diff -w -B -q saida_obtida.tmp "$saida_esperada" > /dev/null; then
        printf "✅ Teste $nome_base: SUCESSO $elapsed_time s\n"
        PASSARAM=$((PASSARAM + 1))
    else
        printf "❌ Teste $nome_base: FALHOU $elapsed_time s\n" 
        echo "--- Saída esperada: ---"
        cat "$saida_esperada"
        echo "--- Saída obtida: ---"
        cat saida_obtida.tmp
        echo "--- Linhas divergentes: ---"
        diff -w -B -y --suppress-common-lines "$saida_esperada" saida_obtida.tmp | sed 's/^/    /'
        FALHARAM=$((FALHARAM + 1))
    fi

    # Limpa os arquivos temporários
    rm -f saida_obtida.tmp erros.tmp
done

# Exibir resumo dos resultados
echo "============================================="
echo "Resumo dos Resultados:"
echo "============================================="
[ "$PASSARAM" -ne 0 ] && echo "✅ Passaram: $PASSARAM"
[ "$FALHARAM" -ne 0 ] && echo "❌ Falharam: $FALHARAM"
[ "$ERROS" -ne 0 ] && echo "🔴 Erros de execução: $ERROS"
printf "⏱️  Tempo total da testagem: $TEMPO_TOTAL s\n"
echo "============================================="