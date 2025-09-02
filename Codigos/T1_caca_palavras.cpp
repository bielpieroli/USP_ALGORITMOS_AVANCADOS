#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>

#define DEBUG false // Booleano indicador de debug para prints de debug

using namespace std;

typedef struct TrieNode {
    TrieNode* children[26];
    bool isEndWord;
    string word;
    char debugChar;
    
    // Inicializando o nó
    TrieNode() {
        for (int i = 0; i < 26; i++) {
            children[i] = nullptr;
        }
        isEndWord = false;
        word = "";
        debugChar = '\0';
    }
 } TRIENODE;

class Trie {
private:
    TRIENODE* root;
    
    // [DEBUG] Trie
    void printTrieDebug(TRIENODE* node, int level, const string& prefix) {
        if (node == nullptr) return;
        
        string indent(level * 2, ' ');
        
        if (node->debugChar != '\0') {
            cout << indent << node->debugChar;
            if (node->isEndWord) {
                cout << " -> '" << node->word << "'";
            }
            cout << endl;
        } else if (level == 0) {
            cout << indent << "ROOT" << endl;
        }
        
        for (int i = 0; i < 26; i++) {
            if (node->children[i] != nullptr) {
                printTrieDebug(node->children[i], level + 1, prefix + char('A' + i));
            }
        }
    }
    
    // Deleta a Trie interativo/recursivamente
    void deleteTrie(TRIENODE* node) {
        if (node == nullptr) return;
        
        for (int i = 0; i < 26; i++) {
            deleteTrie(node->children[i]);
        }
        delete node;
    }

public:
    Trie() {
        root = new TrieNode();
    }
    
    ~Trie() {
        deleteTrie(getRoot());
    }
    
    // Insere uma nova palavra na Trie
    void insert(const string& word) {
        TrieNode* current = getRoot();
        
        for (char c : word) {
            int index = c - 65; // Valor Ascii 'A' = 65
            // Para cada letra ainda não existente na conexão da Trie, cria-se o nó
            if (current->children[index] == nullptr) {
                current->children[index] = new TrieNode();
                current->children[index]->debugChar = c;
            }
            current = current->children[index];
        }
        
        current->isEndWord = true;
        current->word = word;
    }
    
    // Acesso ao nó raiz da Trie, como se fosse um TAD, para não ter acesso direto
    TrieNode* getRoot() {
        return root;
    }
    
    // [DEBUG] impressão da Trie
    void printTrie() {
        if (!DEBUG) return;
        
        cout << "\n" << string(50, '=') << endl;
        cout << "DEBUG: ESTRUTURA DA TRIE" << endl;
        cout << string(50, '=') << endl;
        printTrieDebug(getRoot(), 0, "");
        cout << string(50, '=') << endl;
    }
};

class cacaPalavras {
private:
    // Estruturas de dados para o grid e estado da busca
    int rows, cols;
    vector<vector<char>> grid;
    vector<vector<bool>> visited;

    // Conjunto de palavras encontradas
    set<string> foundWords;

    // Direções para busca (8 direções) (dx,dy)
    const int dx[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
    const int dy[8] = {0, 1, 1, 1, 0, -1, -1, -1};
    
    // Verifica se uma posição está dentro dos limites do grid
    bool isValid(int x, int y) {
        return x >= 0 && x < rows && y >= 0 && y < cols;
    }
    
    // [DEBUG] caminho e grid impressos
    void printarGridPosicao(int x, int y, const string& currentWord) {
        if (!DEBUG) return;
        
        cout << "\nDEBUG: Explorando posição (" << x << ", " << y << ") = '" << grid[x][y] << "'" << endl;
        cout << "DEBUG: Caminho atual: " << currentWord << endl;
        cout << "DEBUG: Grid com posição atual:" << endl;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (i == x && j == y) {
                    cout << "[" << grid[i][j] << "] ";
                } else {
                    cout << " " << grid[i][j] << "  ";
                }
            }
            cout << endl;
        }
    }

    // Impressão da matriz das letras visitadas
    void printarMatrizVisitados(int x, int y) {
        if (!DEBUG) return;
        
        cout << "DEBUG: Matriz de visitados:" << endl;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (i == x && j == y) {
                    cout << (visited[i][j] ? "[X] " : "[.] ");
                } else {
                    cout << (visited[i][j] ? " X  " : " .  ");
                }
            }
            cout << endl;
        }
    }
    
    // Busca em profundidade (DFS)
    void dfs(int x, int y, int dir, TrieNode* trieNode, string& currentWord) {
        // Verifica se a posição é válida e ainda não foi visitada
        if (!isValid(x, y) || visited[x][y]) {
            if (DEBUG) {
                cout << "DEBUG: Posição inválida ou já visitada: (" << x << ", " << y << ")" << endl;
            }
            return;
        }
        
        // Verifica se o caractere atual existe na Trie, se não existir, o programa já para por aqui e volta na recursão
        int charIndex = grid[x][y] - 'A';
        if (trieNode->children[charIndex] == nullptr) {
            if (DEBUG) {
                cout << "DEBUG: Prefixo '" << currentWord + grid[x][y] << "' não existe na Trie - ABORTANDO" << endl;
            }
            return;
        }
        
        // Avança para o próximo nó na Trie e acresce a palavra
        trieNode = trieNode->children[charIndex];
        currentWord += grid[x][y];
        
        if (DEBUG) {
            printarGridPosicao(x, y, currentWord);
            printarMatrizVisitados(x, y);
            cout << "DEBUG: Prefixo '" << currentWord << "' existe na Trie - CONTINUANDO" << endl;
        }
        
        // Verifica se encontrou uma palavra válida, colocando-a no set
        if (trieNode->isEndWord && currentWord.length() >= 2) {
            foundWords.insert(currentWord);
            if (DEBUG) {
                cout << "🎉 DEBUG: PALAVRA ENCONTRADA: '" << currentWord << "'" << endl;
                cout << "🎉 DEBUG: Na posição: (" << x << ", " << y << ")" << endl;
            }
        }
        
        // Marca como visitado e continua a busca
        visited[x][y] = true;
        
        // Explora as direções
        if (dir == -1) {
            if (DEBUG) {
                cout << "DEBUG: Explorando 8 direções a partir de (" << x << ", " << y << ")" << endl;
            }
            // Explora todas as 8 direções se for a primeira chamada
            for (int i = 0; i < 8; i++) {
                int newX = x + dx[i];
                int newY = y + dy[i];
                if (DEBUG) {
                    cout << "DEBUG: → Direção " << i << " (" << dx[i] << ", " << dy[i] << "): nova posição (" << newX << ", " << newY << ")" << endl;
                }
                dfs(newX, newY, i, trieNode, currentWord);
            }
            // Do contrário, ela deve continuar na mesma direção
        } else {
            int newX = x + dx[dir];
            int newY = y + dy[dir];
            if (DEBUG) {
                cout << "DEBUG: → Continuando direção " << dir << " (" << dx[dir] << ", " << dy[dir] << "): nova posição (" << newX << ", " << newY << ")" << endl;
            }
            dfs(newX, newY, dir, trieNode, currentWord);
        }
        
        // Backtracking, desmarcando a posição visitada e o caracter
        visited[x][y] = false;
        currentWord.pop_back();
        
        if (DEBUG) {
            cout << "DEBUG: Backtrack na posição (" << x << ", " << y << ") - desmarcando visita" << endl;
        }
    }

public:
    cacaPalavras(int r, int c) : rows(r), cols(c) {
        grid.resize(rows, vector<char>(cols));
        visited.resize(rows, vector<bool>(cols, false));
    }
    
    // Configura o grid a partir da entrada
    void setGrid(const vector<string>& inputGrid) {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                grid[i][j] = inputGrid[i][j];
            }
        }
    }
    
    // Encontra todas as palavras do dicionário no grid
    vector<string> buscaPalavras(Trie& dictionary) {
        foundWords.clear();
        
        // Para cada posição do grid, inicia uma busca
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (DEBUG) {
                    cout << "\n" << string(60, '=') << endl;
                    cout << "DEBUG: INICIANDO BUSCA A PARTIR DE (" << i << ", " << j << ") = '" << grid[i][j] << "'" << endl;
                    cout << string(60, '=') << endl;
                }
                
                // Reseta a matriz de visitados para cada nova posição inicial
                for (int x = 0; x < rows; x++) {
                    for (int y = 0; y < cols; y++) {
                        visited[x][y] = false;
                    }
                }
                
                string currentWord = "";
                dfs(i, j, -1, dictionary.getRoot(), currentWord);
            }
        }
        
        // Converte o set para um vetor, retornando-o
        vector<string> result(foundWords.begin(), foundWords.end());
        return result;
    }
};

int main() {    

    // Entradas do programa
    int amountOfLines, amountOfColumns;
    cin >> amountOfLines >> amountOfColumns;
    
    vector<string> gridInput(amountOfLines);
    for (int i = 0; i < amountOfLines; i++) {
        cin >> gridInput[i];
    }
    
    int amountOfDictWords;
    cin >> amountOfDictWords;
    
    // Construção do dicionário Trie
    Trie dictionary;
    for (int i = 0; i < amountOfDictWords; i++) {
        string word;
        cin >> word;
        dictionary.insert(word);
    }
    
    // Printa a Trie final se estiver no modo debug
    if (DEBUG) {
        dictionary.printTrie();
    }
    
    // Configuração e execução do solucionador
    cacaPalavras solver(amountOfLines, amountOfColumns);
    solver.setGrid(gridInput);
    
    vector<string> foundWords = solver.buscaPalavras(dictionary);
    
    // Saída dos resultados
    cout << foundWords.size() << endl;
    for (const string& word : foundWords) {
        cout << word << endl;
    }
    
    return 0;
}