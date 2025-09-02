CODIGOS_DIR = Codigos
TEST_DIR = Testes
EXEC_DIR = Executaveis
SRC = $(wildcard $(CODIGOS_DIR)/*.cpp)

CFLAGS = -Wall -Werror -std=c++17
LDFLAGS = 

createExecDir: clean
	mkdir -p $(EXEC_DIR)

all: createExecDir 
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make all NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	if [ -f "$(CODIGOS_DIR)/$$name.cpp" ]; then \
		g++ $(CFLAGS) "$(CODIGOS_DIR)/$$name.cpp" -o "$(EXEC_DIR)/$$name" $(LDFLAGS); \
		echo "Compilado: $(EXEC_DIR)/$$name"; \
	else \
		echo "Erro: Arquivo $$name.cpp não encontrado em $(CODIGOS_DIR)/."; \
		exit 1; \
	fi

run: all
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make run NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	if [ -f "$(EXEC_DIR)/$$name" ]; then \
		./"$(EXEC_DIR)/$$name"; \
	else \
		echo "Erro: Executável $$name não encontrado em $(EXEC_DIR)/."; \
		exit 1; \
	fi

# Regra para testar um programa
testes: clean all
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make testes NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	test_dir="$(TEST_DIR)/$$name"; \
	if [ -f "$(EXEC_DIR)/$$name" ] && [ -d "$$test_dir" ]; then \
		./testar.sh "$(EXEC_DIR)/$$name" "$$test_dir"; \
	else \
		echo "Erro: Programa executável $$name ou pasta de testes não encontrados."; \
		exit 1; \
	fi

# Rodar teste específico
especifico: all
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make especifico NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	test_dir="$(TEST_DIR)/$$name"; \
	if [ ! -f "$(EXEC_DIR)/$$name" ] || [ ! -d "$$test_dir" ]; then \
		echo "Erro: Programa executável $$name ou pasta de testes não encontrados."; \
		exit 1; \
	fi; \
	echo "Digite o número do caso teste:"; \
	read caso_teste; \
	input_file="$$test_dir/in/$$caso_teste.in"; \
# 	expected_output="$$test_dir/out/$$caso_teste.out"; \
	if [ ! -f "$$input_file" ]; then \
		echo "Erro: Arquivo de teste $$caso_teste.in não encontrado em $$test_dir/in/"; \
		exit 1; \
	fi; \
	echo "Executando teste $$caso_teste..."; \
# 	./"$(EXEC_DIR)/$$name" < "$$input_file" > output.tmp; \
	./"$(EXEC_DIR)/$$name" < "$$input_file"; \
# 	echo "Diferenças encontradas (saída esperada vs. obtida):"; \
# 	diff -w -B -y "$$expected_output" output.tmp; \
# 	if [ $$? -eq 0 ]; then \
# 		echo "✅ Teste $$caso_teste passou!"; \
# 	else \
# 		echo "❌ Teste $$caso_teste falhou!"; \
# 	fi; \
# 	rm -f output.tmp

# Criar diretórios de testes automaticamente
dirs: $(TEST_DIR)
	@for src in $(SRC); do \
		dirname=$$(basename $$src .cpp); \
		mkdir -p "$(TEST_DIR)/$$dirname/in"; \
		mkdir -p "$(TEST_DIR)/$$dirname/out"; \
	done
	@echo "Pastas de testes criadas em '$(TEST_DIR)'."

$(TEST_DIR):
	@mkdir -p "$(TEST_DIR)"

# Descompactar arquivos de testes
deszipar:
	@for dir in "$(TEST_DIR)"/*; do \
		if [ -d "$$dir" ]; then \
			echo "Descompactando arquivos em $$dir"; \
			unzip -o "$$dir"/*.zip -d "$$dir"/; \
		fi; \
	done

# Compactar um programa para entrega
zip:
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make zip NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	if [ -f "$(CODIGOS_DIR)/$$name.cpp" ]; then \
		echo "all: clean" > "$(CODIGOS_DIR)/Makefile"; \
		echo "	g++ -Wall -Werror -std=c++17 $$name.cpp -o $$name" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "run: all" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "	./$$name" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "clean:" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "	rm -f $$name" >> "$(CODIGOS_DIR)/Makefile"; \
		make all 0_coordenadas; \
		(cd "$(CODIGOS_DIR)" && zip -r ../15678578.zip "$$name.cpp" "../Executaveis/$$name" Makefile); \
		rm -f $(CODIGOS_DIR)/Makefile; \
		echo "Arquivo 15678578.zip criado com sucesso!"; \
	else \
		echo "Erro: Arquivo $$name.cpp não encontrado em $(CODIGOS_DIR)/."; \
		exit 1; \
	fi

# Limpar executáveis
clean:
	rm -rf $(EXEC_DIR) 15678578.zip

%:  # Captura argumentos extras
	@:

.PHONY: createExecDir run testes especifico dirs deszipar zip clean