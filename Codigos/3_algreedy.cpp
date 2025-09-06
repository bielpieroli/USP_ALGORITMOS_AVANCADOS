#include <bits/stdc++.h>
using namespace std;

int toMinutes(const string &hora) {
    int h = stoi(hora.substr(0, 2));
    int m = stoi(hora.substr(3, 2));
    return h * 60 + m;
}

int main() {
    int numberOfTests;
    cin >> numberOfTests; 

    while (numberOfTests--) {
        int numberOfCarTypes, numberOfRents;
        cin >> numberOfCarTypes >> numberOfRents;

        vector<vector<tuple<int,int,int>>> modelos(numberOfCarTypes+1);
        // cada tupla: (fim, inicio, cliente)

        for (int i = 0; i < numberOfRents; i++) {
            int cliente, modelo;
            string inicio, fim;
            cin >> cliente >> inicio >> fim >> modelo;

            int iniMinutes = toMinutes(inicio);
            int endMinutes = toMinutes(fim);

            modelos[modelo].push_back({endMinutes, iniMinutes, cliente});
        }

        vector<string> respostas;

        for (int modelo = 1; modelo <= numberOfCarTypes; modelo++) {
            auto &pedidos = modelos[modelo];
            sort(pedidos.begin(), pedidos.end());

            vector<int> escolhidos;
            int ultimoFim = -1;

            for (auto [fim, inicio, cliente] : pedidos) {
                if (inicio >= ultimoFim) {
                    escolhidos.push_back(cliente);
                    ultimoFim = fim;
                }
            }

            // Monta saída para esse modelo
            stringstream ss;
            ss << modelo << ": " << escolhidos.size() << " = ";
            for (size_t i = 0; i < escolhidos.size(); i++) {
                if (i > 0) ss << ", ";
                ss << escolhidos[i];
            }
            respostas.push_back(ss.str());
        }

        // Imprime todos os modelos separados por " | "
        for (size_t i = 0; i < respostas.size(); i++) {
            if (i > 0) cout << " | ";
            cout << respostas[i];
        }
        cout << "\n";
    }

    return 0;
}
