#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>

using namespace std;

typedef struct Pessoa {
    int id;
    bool temDiabetes;
    int paiId;
    int maeId;
    bool visitado;
    
    // Default dos argumentos
    Pessoa() : id(-1), temDiabetes(false), paiId(-1), maeId(-1), visitado(false) {}

    // Quando receber argumentos, atribui
    Pessoa(int _id, bool _diabetes, int _pai, int _mae) 
        : id(_id), temDiabetes(_diabetes), paiId(_pai), maeId(_mae), visitado(false) {}
} Pessoa;

class DiabetesAnalyzer {
private:
    // Unordered_map é um hash
    unordered_map<int, Pessoa> pessoas;

    int contadorHeranca;

    bool herdouDiabetes(int pessoaId) {
        // Procura pela pessoa
        if (pessoas.find(pessoaId) == pessoas.end()) return false;

        Pessoa& p = pessoas[pessoaId];

        // Verifica a herança dela
        bool herdou = false;
        if (p.temDiabetes) {
            if ((p.paiId != -1 && pessoas[p.paiId].temDiabetes) ||
                (p.maeId != -1 && pessoas[p.maeId].temDiabetes)) {
                herdou = true;
            }
        }
        return herdou;
    }

public:
    int analisarArvoreGenealogica(const vector<Pessoa>& dados) {
        pessoas.clear();

        // Colocam-se todas as pessoas no hash map
        for (const Pessoa& p : dados) {
            pessoas[p.id] = p;
        }

        // Verifica a herança exaustivamente de cada pessoa
        int contador = 0;
        for (auto& [id, p] : pessoas) {
            if (herdouDiabetes(id)) {
                contador++;
            }
        }
        return contador;
    }
};

int main() {
    int numberOfTests;
    cin >> numberOfTests;
    // cout << numberOfTests << endl;

    DiabetesAnalyzer analyzer;
    
    for (int test = 1; test <= numberOfTests; test++) {
        // cout <<  "Test Number: " << test << endl;

        int numberOfFamilyMembers;
        cin >> numberOfFamilyMembers;
        // cout << numberOfFamilyMembers << endl;

        vector<Pessoa> dados;
        dados.reserve(numberOfFamilyMembers);
        
        for (int i = 0; i < numberOfFamilyMembers; i++) {
            int id, paiId, maeId;
            string diabetesStatus;
            
            cin >> id >> diabetesStatus >> paiId >> maeId;
            // cout << "id: " << id << ", status: " << diabetesStatus << ", idPai: " << paiId << ", idMae: " << maeId << endl;

            bool temDiabetes = (diabetesStatus == "sim");

            // Criando a nova pessoa e adicionando no vetor de dados (no final dele)
            Pessoa novaPessoa(id, temDiabetes, paiId, maeId);
            dados.push_back(novaPessoa);
        }
        
        // Analisa a árvore genealógica usando backtracking
        int resultado = analyzer.analisarArvoreGenealogica(dados);
        cout << resultado << "\n";
    }
    
    return 0;
}