estoque = {}

numero_cadastros = int(input())
# print(f"O número de cadastros é {numero_cadastros}")

for _ in range(numero_cadastros):
  cadastro = input().strip().split()
  preco_por_kg = float(cadastro[-1])
  codigo_item = cadastro[0]
  if codigo_item not in estoque:
    # print(f"Item a ser cadastrado {codigo_item} custando RS{preco_por_kg}")
    estoque[codigo_item] = preco_por_kg  
  else:
    print(f"Produto com código {codigo_item} já cadastrado.")

# print(estoque)

numero_compras = int(input())
# print(f"O número de compras é {numero_compras}")

while(numero_compras != -1):
  total_compra = 0
  for _ in range(numero_compras):
    compra = input().strip().split()
    quantidade_item = float(compra[-1])
    codigo_compra = compra[0]
    if codigo_compra not in estoque:
      print(f"Produto com código {codigo_compra} não cadastrado.")
    else:
      # print(f"Item {codigo_compra} em quantidade {quantidade_item} kg")
      total_compra += quantidade_item * estoque[codigo_compra]
  print(f"R${total_compra:.2f}")
  numero_compras = int(input())
  # print(f"O número de compras é {numero_compras}")

# ****************
# Quitanda do João
# ****************
# Desenvolver um sistema automatizado para a quitanda do João que:
# 1. Cadastra produtos (código + preço por kg).
# 2. Registra compras de clientes, calculando o valor total por item.
# 3. Exibe mensagens de erro em casos de:
# i) Código duplicado no cadastro.
# ii) Código inexistente durante a compra.
# 4. Calcula o total da compra ao final de cada atendimento.

# ****************
# Formatação
# ****************

# ================
# Entrada
# ================
# Cadastro de Produtos:
# a) Um inteiro N (1 ≤ N ≤ 10.000) indicando quantos produtos serão cadastrados.

# b) N linhas no formato:
# #XXXX preço/kg
# #XXXX: Código do produto (4 dígitos).

# Registro de Compras:
# a) Um inteiro M (1 ≤ M ≤ 10.000) indicando quantos itens tem a compra.

# b) M linhas no formato:
# #XXXX Peso do item
# #XXXX: Código do produto.

# Ao receber M = -1, encerra o programa.

# ================
# Saída
# ================

# MENSAGENS DE ERRO:
# 1. Se um código já foi cadastrado:
# Produto com código #XXXX já cadastrado. 
 
# 2. Se um código não existe na compra:
# Produto com código #XXXX não cadastrado. 
 
# Total da compra:
# R$X.XX  
# (2 casas decimais).

# ****************
# EX. CASO TESTE
# ****************
# ================
# Entrada
# ================
# 5  
# #1234 12.0  
# #2345 5.0  
# #3456 7.0  
# #4567 8.0  
# #1234 10.0  
# 3  
# #2345 2.2  
# #4567 0.7  
# #3456 3.5  
# 1  
# #1234 1.8  
# 2  
# #9010 2.5  
# #2345 0.5  
# -1  
# ================
# Saída
# ================
# Produto com código #1234 já cadastrado.  
# R$41.10  
# R$21.60  
# Produto com código #9010 não cadastrado.  
# R$2.50  
