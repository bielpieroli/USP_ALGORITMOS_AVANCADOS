#include <bits/stdc++.h>

using namespace std;

int toMinutes(const string &hora) {
    int h = stoi(hora.substr(0, 2));
    int m = stoi(hora.substr(3, 2));
    return h * 60 + m;
}

vector<vector<tuple<int, int, int>>> lerDados(int numberOfCarTypes, int numberOfRents) {

    vector<vector<tuple<int, int, int>>> modelos(numberOfCarTypes + 1);
    
    for (int i = 0; i < numberOfRents; i++) {
        int cliente, modelo;
        string inicio, fim;
        cin >> cliente >> inicio >> fim >> modelo;

        int iniMinutes = toMinutes(inicio);
        int endMinutes = toMinutes(fim);

        modelos[modelo].push_back({endMinutes, iniMinutes, cliente});
        // tupla é (fim, inicio, cliente)
    }
    
    return modelos;
}

vector<int> processarModelo(vector<tuple<int, int, int>> &pedidos) {
    sort(pedidos.begin(), pedidos.end(), [](const auto &a, const auto &b) {
        if (get<0>(a) != get<0>(b)) // Primeiro, sort pelo fim
            return get<0>(a) < get<0>(b);
        else if (get<1>(a) != get<1>(b)) // Senão for pelo fim, é pelo começo
            return get<1>(a) < get<1>(b);
        else // Do contrário, é pelo cliente mesmo
            return get<2>(a) < get<2>(b);
    });

    vector<int> escolhidos;
    int ultimoFim = -1;

    for (auto [fim, inicio, cliente] : pedidos) {
        if (inicio >= ultimoFim) {
            escolhidos.push_back(cliente);
            ultimoFim = fim;
        }
    }

    return escolhidos;
}

string formatarSaida(int modelo, const vector<int> &escolhidos) {

    stringstream saida;    
    saida << modelo << ": " << escolhidos.size();  
    if (!escolhidos.empty()) saida << " = ";

    for (size_t i = 0; i < escolhidos.size(); i++) {
        if (i > 0) saida << ", ";
        saida << escolhidos[i];
    }

    return saida.str();    
}

int main() {

    int numberOfTests;
    cin >> numberOfTests;

    while (numberOfTests--) {   

        int numberOfCarTypes, numberOfRents;
        cin >> numberOfCarTypes >> numberOfRents;

        auto modelos = lerDados(numberOfCarTypes, numberOfRents);   
        vector<string> respostas;

        for (int modelo = 1; modelo <= numberOfCarTypes; modelo++) {
            auto escolhidos = processarModelo(modelos[modelo]);
            respostas.push_back(formatarSaida(modelo, escolhidos)); 
        }

        for (size_t i = 0; i < respostas.size(); i++) { 
            if (i > 0) cout << " | ";
            cout << respostas[i];
        }
        cout << "\n";
    }

    return 0;
}