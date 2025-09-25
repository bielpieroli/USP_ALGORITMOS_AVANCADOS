#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <map>
#include <sstream>
#include <algorithm>
#include <iomanip>
#include <limits>

using namespace std;

const bool DEBUG = false;

double level_to_productivity(const string& level) {
    map<string, double> productivity_map = {
        {"Aprendiz", 0.75},
        {"Aventureiro", 1.0},
        {"Cavaleiro", 1.2},
        {"Mestre", 1.5},
        {"Lenda", 2.0}
    };
    
    auto it = productivity_map.find(level);
    return (it != productivity_map.end()) ? it->second : 1.0;
}

struct Quest {
    int index;
    int base_time;
    vector<int> dependencies;
    double ready_time;
    double finish_time;
    
    Quest() : index(0), base_time(0), ready_time(0.0), finish_time(0.0) {}
};

struct Hero {
    string name;
    string level;
    double productivity;
    vector<int> assigned_quests;
    double free_time;
    
    Hero() : productivity(0.0), free_time(0.0) {}
};

vector<Hero> process_heroes(int number_of_heroes) {
    vector<Hero> heroes(number_of_heroes);
    
    for (int i = 0; i < number_of_heroes; i++) {
        cin >> heroes[i].name >> heroes[i].level;
        heroes[i].productivity = level_to_productivity(heroes[i].level);
    }
    
    if (DEBUG) {
        cout << "DEBUG: HEROES PROCESSADOS" << endl;
        for (const auto& h : heroes) {
            cout << "  " << h.name << " (" << h.level << "): Prod = " 
                 << fixed << setprecision(2) << h.productivity << endl;
        }
    }
    
    return heroes;
}

vector<Quest> process_quests(int number_of_quests) {
    vector<Quest> quests(number_of_quests);
    
    for (int i = 0; i < number_of_quests; i++) {
        string line;
        cin.ignore();
        getline(cin, line);
        
        istringstream iss(line);
        vector<int> values;
        int value;
        while (iss >> value) {
            values.push_back(value);
        }
        
        quests[i].index = values[0];
        quests[i].base_time = values[1];
        
        // Processa dependências (ignora 0)
        for (int j = 2; j < int(values.size()); j++) {
            if (values[j] != 0) {
                quests[i].dependencies.push_back(values[j]);
            }
        }
        
        if (DEBUG) {
            string deps_str = "";
            for (int j = 0; j < int(quests[i].dependencies.size()); j++) {
                if (j > 0) deps_str += ",";
                deps_str += to_string(quests[i].dependencies[j]);
            }
            cout << "DEBUG: QUEST " << quests[i].index << ": BaseTime = " 
                 << quests[i].base_time << ", Deps = {" << deps_str << "}" << endl;
        }
    }
    
    return quests;
}

vector<int> topological_order(const vector<Quest>& quests, int M) {
    vector<vector<int>> graph(M + 1);
    vector<int> in_degree(M + 1, 0);
    
    // Constrói o grafo de dependências
    for (const auto& quest : quests) {
        for (int dep : quest.dependencies) {
            graph[dep].push_back(quest.index);
            in_degree[quest.index]++;
        }
    }
    
    if (DEBUG) {
        cout << "\nDEBUG: GRAFO DE DEPENDENCIAS E GRAU DE ENTRADA" << endl;
        for (int i = 1; i <= M; i++) {
            if (in_degree[i] > 0 || !graph[i].empty()) {
                string neighbors_str = "";
                for (int j = 0; j < int(graph[i].size()); j++) {
                    if (j > 0) neighbors_str += ", ";
                    neighbors_str += to_string(graph[i][j]);
                }
                cout << "  Quest " << i << " (inDegree=" << in_degree[i] 
                     << ") precede: " << neighbors_str << endl;
            }
        }
    }
    
    queue<int> q;
    vector<int> topo_order;
    
    // Adiciona quests sem dependências na fila
    for (int i = 1; i <= M; i++) {
        if (in_degree[i] == 0) {
            q.push(i);
        }
    }
    
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        topo_order.push_back(current);
        
        // Remove aresta e atualiza grau de entrada dos vizinhos
        for (int neighbor : graph[current]) {
            in_degree[neighbor]--;
            if (in_degree[neighbor] == 0) {
                q.push(neighbor);
            }
        }
    }
    
    if (DEBUG) {
        cout << "DEBUG: ORDEM TOPOLOGICA FINAL" << endl;
        string order_str = "";
        for (int i = 0; i < int(topo_order.size()); i++) {
            if (i > 0) order_str += " -> ";
            order_str += to_string(topo_order[i]);
        }
        cout << "  Ordem: " << order_str << endl;
        
        if (int(topo_order.size()) != M) {
            cout << "!!! ALERTA: CICLO DETECTADO NO GRAFO DE DEPENDENCIAS (TopoOrder size: " 
                 << topo_order.size() << ", M: " << M << ") !!!" << endl;
        }
    }
    
    return topo_order;
}

double assign_quests(vector<Hero>& heroes, vector<Quest>& quests, int M) {
    vector<int> topo_order = topological_order(quests, M);
    
    map<int, int> quest_index_map;
    for (int i = 0; i < int(quests.size()); i++) {
        quest_index_map[quests[i].index] = i;
    }
    
    for (int quest_index : topo_order) {
        int quest_array_index = quest_index_map[quest_index];
        Quest& current_quest = quests[quest_array_index];
        
        double ready_time = 0.0;
        for (int dep_index : current_quest.dependencies) {
            int dep_array_index = quest_index_map[dep_index];
            ready_time = max(ready_time, quests[dep_array_index].finish_time);
        }
        current_quest.ready_time = ready_time;
        
        if (DEBUG) {
            cout << "\nDEBUG: PROCESSANDO QUEST " << quest_index 
                 << " (baseTime=" << current_quest.base_time << ")" << endl;
            cout << "  ReadyTime (max finish das deps): " 
                 << fixed << setprecision(2) << ready_time << endl;
        }
        
        int best_hero = -1;
        double best_finish_time = numeric_limits<double>::infinity();
        
        for (int i = 0; i < int(heroes.size()); i++) {
            double start_time = max(ready_time, heroes[i].free_time);
            double execution_time = current_quest.base_time / heroes[i].productivity;
            double finish_time = start_time + execution_time;
            
            if (best_hero == -1 || finish_time < best_finish_time) {
                best_finish_time = finish_time;
                best_hero = i;
            }
            else if (finish_time == best_finish_time) {
                if (i < best_hero) {
                    best_hero = i;
                }
            }
        }
        
        heroes[best_hero].assigned_quests.push_back(quest_index);
        heroes[best_hero].free_time = best_finish_time;
        current_quest.finish_time = best_finish_time;
        
        if (DEBUG) {
            cout << "  ATRIBUIDO: Quest " << quest_index << " para Heroi " 
                 << heroes[best_hero].name << " (Prod=" << fixed << setprecision(2) 
                 << heroes[best_hero].productivity << ")" << endl;
            cout << "  FinishTime (Quest e Heroi): " << fixed << setprecision(2) 
                 << best_finish_time << endl;
        }
    }
    
    double min_time = 0.0;
    for (const auto& quest : quests) {
        min_time = max(min_time, quest.finish_time);
    }
    
    return min_time;
}

void formatar_saida(const vector<Hero>& heroes, double min_time) {
    for (const auto& hero : heroes) {
        string quests_str = "";
        for (int i = 0; i < int(hero.assigned_quests.size()); i++) {
            if (i > 0) quests_str += ",";
            quests_str += to_string(hero.assigned_quests[i]);
        }
        cout << hero.name << " = {" << quests_str << "}" << endl;
    }
    
    cout << "Tempo mínimo: " << fixed << setprecision(2) << min_time << endl;
}

int main() {
    int number_of_tests;
    cin >> number_of_tests;
    
    for (int i = 0; i < number_of_tests; i++) {
        int number_of_heroes, number_of_quests;
        cin >> number_of_heroes >> number_of_quests;
        
        vector<Hero> heroes = process_heroes(number_of_heroes);
        vector<Quest> quests = process_quests(number_of_quests);
        
        double min_time = assign_quests(heroes, quests, number_of_quests);
        formatar_saida(heroes, min_time);
        
        if (i != number_of_tests - 1) {
            cout << endl;
        }
    }
    
    return 0;
}