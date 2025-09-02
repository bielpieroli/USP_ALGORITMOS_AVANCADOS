#include <iostream>
#include <map>
#include <string>
#include <iomanip>
using namespace std;

int main() {
    map<string, double> estoque;
    int numero_cadastros;
    cin >> numero_cadastros;
    // cout << "O número de cadastros é " << numero_cadastros << endl;

    for (int i = 0; i < numero_cadastros; i++) {
        string codigo_item;
        double preco_por_kg;
        cin >> codigo_item >> preco_por_kg;

        if (estoque.find(codigo_item) == estoque.end()) {
            // cout << "Item a ser cadastrado " << codigo_item << " custando R$" << preco_por_kg << endl;
            estoque[codigo_item] = preco_por_kg;
        } else {
            cout << "Produto com código " << codigo_item << " já cadastrado." << endl;
        }
    }
    // cout << estoque.size() << endl;

    int numero_compras;
    cin >> numero_compras;
    // cout << "O número de compras é " << numero_compras << endl;

    while (numero_compras != -1) {
        double total_compra = 0.0;

        for (int i = 0; i < numero_compras; i++) {
            string codigo_compra;
            double quantidade_item;
            cin >> codigo_compra >> quantidade_item;

            if (estoque.find(codigo_compra) == estoque.end()) {
                cout << "Produto com código " << codigo_compra << " não cadastrado." << endl;
            } else {
                // cout << "Item " << codigo_compra << " em quantidade " << quantidade_item << " kg" << endl;
                total_compra += quantidade_item * estoque[codigo_compra];
            }
        }
        cout << fixed << setprecision(2);
        cout << "R$" << total_compra << endl;

        cin >> numero_compras;
        // cout << "O número de compras é " << numero_compras << endl;
    }

    return 0;
}

// ****************
// Quitanda do João
// ****************
// Desenvolver um sistema automatizado para a quitanda do João que:
// 1. Cadastra produtos (código + preço por kg).
// 2. Registra compras de clientes, calculando o valor total por item.
// 3. Exibe mensagens de erro em casos de:
// i) Código duplicado no cadastro.
// ii) Código inexistente durante a compra.
// 4. Calcula o total da compra ao final de cada atendimento.

// ****************
// Formatação
// ****************

// ================
// Entrada
// ================
// Cadastro de Produtos:
// a) Um inteiro N (1 ≤ N ≤ 10.000) indicando quantos produtos serão cadastrados.
//
// b) N linhas no formato:
// #XXXX preço/kg
// #XXXX: Código do produto (4 dígitos).
//
// Registro de Compras:
// a) Um inteiro M (1 ≤ M ≤ 10.000) indicando quantos itens tem a compra.
//
// b) M linhas no formato:
// #XXXX Peso do item
// #XXXX: Código do produto.
//
// Ao receber M = -1, encerra o programa.
//
// ================
// Saída
// ================
//
// MENSAGENS DE ERRO:
// 1. Se um código já foi cadastrado:
// Produto com código #XXXX já cadastrado. 
// 
// 2. Se um código não existe na compra:
// Produto com código #XXXX não cadastrado. 
// 
// Total da compra:
// R$X.XX  
// (2 casas decimais).
//
// ****************
// EX. CASO TESTE
// ****************
// ================
// Entrada
// ================
// 5  
// #1234 12.0  
// #2345 5.0  
// #3456 7.0  
// #4567 8.0  
// #1234 10.0  
// 3  
// #2345 2.2  
// #4567 0.7  
// #3456 3.5  
// 1  
// #1234 1.8  
// 2  
// #9010 2.5  
// #2345 0.5  
// -1  
// ================
// Saída
// ================
// Produto com código #1234 já cadastrado.  
// R$41.10  
// R$21.60  
// Produto com código #9010 não cadastrado.  
// R$2.50  
