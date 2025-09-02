#include <bits/stdc++.h>

using namespace std;


void printResult(const vector<string> &escolhidos, double somaEscolhidos, int numberOfDays) {
    int qtd = escolhidos.size();
    cout << qtd << " " << (qtd == 1 ? "dia" : "dias") << " (";

    for (int i = 0; i < qtd; i++) {
        if (i > 0) cout << ", ";
        cout << escolhidos[i];
    }

    cout << ") | soma=" << fixed << setprecision(2) << somaEscolhidos;
    cout << " | " << fixed << setprecision(2) << (100.0 * qtd / numberOfDays) << "% dos dias totais\n";
}

void sortDates(vector<string> &datas) {
  sort(datas.begin(), datas.end(), [](const string &a, const string &b) {
      // s = "DD/MM/AAAA" -> "AAAAMMDD"
      string orderedA = a.substr(6,4) + a.substr(3,2) + a.substr(0,2);
      string orderedB = b.substr(6,4) + b.substr(3,2) + b.substr(0,2);
      // cout << "ordenando: " << orderedA << " vs " << orderedB << " -> " << (orderedA < orderedB ? "True" : "False") << endl;
      return orderedA < orderedB;
  });
}

pair<map<string,double>, double> inputVendas(int numberOfDays) {
    map<string,double> vendas;
    double somaVendas = 0.0;

    for (int j = 0; j < numberOfDays; j++) {
        string data;
        double valor;
        cin >> data >> valor;
        vendas[data] = valor;
        somaVendas += valor;
        // cout << "Data: " << data << endl;
        // cout << "Valor: " << valor << endl;
    }
    return {vendas, somaVendas};
}


int main () {
  int numberOfTestes;
  cin >> numberOfTestes;

  for (int t = 0; t < numberOfTestes; t++) {
    int numberOfDays;
    cin >> numberOfDays;

    auto [vendas, somaVendas] = inputVendas(numberOfDays);

    vector<pair<string, double>> ordenados(vendas.begin(), vendas.end());
    sort(ordenados.begin(), ordenados.end(), [](auto &a, auto &b) {
      return a.second > b.second; 
    });

    vector<string> escolhidos;
    double somaEscolhidos = 0;

    for (int k = 0; somaEscolhidos < somaVendas - somaEscolhidos; k++) {
      escolhidos.push_back(ordenados[k].first);

      somaEscolhidos += ordenados[k].second;
    }
  
    sortDates(escolhidos);

    printResult(escolhidos, somaEscolhidos, numberOfDays);
  }
}
