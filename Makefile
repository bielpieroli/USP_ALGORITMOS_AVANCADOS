CODIGOS_DIR = Codigos
TEST_DIR = Testes
SRC = $(wildcard $(CODIGOS_DIR)/*.py)

all:

# Regra para rodar um programa Python
run:
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make run NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	if [ -f "$(CODIGOS_DIR)/$$name.py" ]; then \
		python3 "$(CODIGOS_DIR)/$$name.py"; \
	else \
		echo "Erro: Arquivo $$name.py não encontrado em $(CODIGOS_DIR)/."; \
	fi

# Regra para testar um programa
testes:
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make testes NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	test_dir="$(TEST_DIR)/$$name"; \
	if [ -f "$(CODIGOS_DIR)/$$name.py" ] && [ -d "$$test_dir" ]; then \
		./testar.sh "$(CODIGOS_DIR)/$$name.py" "$$test_dir"; \
	else \
		echo "Erro: Programa $$name.py ou pasta de testes não encontrados."; \
	fi

# Rodar teste específico
especifico:
	@if [ -z "$(word 2, $(MAKECMDGOALS))" ]; then \
		echo "Uso: make especifico NOME_DO_PROGRAMA"; \
		exit 1; \
	fi; \
	echo "Digite o número do caso teste:"; \
	read caso_teste; \
	name="$(word 2, $(MAKECMDGOALS))"; \
	test_dir="$(TEST_DIR)/$$name"; \
	if [ -f "$(CODIGOS_DIR)/$$name.py" ] && [ -d "$$test_dir" ]; then \
		input_file="$$test_dir/in/$$caso_teste.in"; \
		expected_output="$$test_dir/out/$$caso_teste.out"; \
		if [ -f "$$input_file" ] && [ -f "$$expected_output" ]; then \
			echo "Executando teste $$caso_teste..."; \
			python3 "$(CODIGOS_DIR)/$$name.py" < "$$input_file" > output.tmp; \
			echo "Diferenças encontradas (saída esperada vs. obtida):"; \
			diff -w -B -y "$$expected_output" output.tmp; \
			if [ $$? -eq 0 ]; then \
				echo "✅ Teste $$caso_teste passou!"; \
			else \
				echo "❌ Teste $$caso_teste falhou!"; \
			fi; \
			rm -f output.tmp; \
		else \
			echo "Erro: Arquivos de teste $$caso_teste.in ou $$caso_teste.out não encontrados em $$test_dir"; \
		fi; \
	else \
		echo "Erro: Programa $$name.py ou pasta de testes não encontrados."; \
	fi

%:  # Captura argumentos extras
	@:

# Criar diretórios de testes automaticamente
dirs: $(TEST_DIR)
	@for src in $(SRC); do \
		dirname=$$(basename $$src .py); \
		mkdir -p "$(TEST_DIR)/$$dirname"; \
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
	if [ -f "$(CODIGOS_DIR)/$$name.py" ]; then \
		echo "all:" > "$(CODIGOS_DIR)/Makefile"; \
		echo "" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "run:" >> "$(CODIGOS_DIR)/Makefile"; \
		echo "	python3 $$name.py" >> "$(CODIGOS_DIR)/Makefile"; \
		(cd "$(CODIGOS_DIR)" && zip -r ../15678578.zip "$$name.py" Makefile); \
		rm -f "$(CODIGOS_DIR)/Makefile"; \
		echo "Arquivo 15678578.zip criado com sucesso!"; \
	else \
		echo "Erro: Arquivo $$name.py não encontrado em $(CODIGOS_DIR)/."; \
		exit 1; \
	fi

.PHONY: run testes especifico dirs deszipar zip
