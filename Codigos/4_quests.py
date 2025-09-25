from collections import deque

DEBUG = False

def level_to_productivity(level):
    """Mapeia o nível do herói para sua produtividade"""
    productivity_map = {
        "Aprendiz": 0.75,
        "Aventureiro": 1.0,
        "Cavaleiro": 1.2,
        "Mestre": 1.5,
        "Lenda": 2.0
    }
    return productivity_map.get(level, 1.0)

class Quest:
    def __init__(self):
        self.index = 0
        self.base_time = 0
        self.dependencies = []
        self.ready_time = 0.0
        self.finish_time = 0.0

class Hero:
    def __init__(self):
        self.name = ""
        self.level = ""
        self.productivity = 0.0
        self.assigned_quests = []
        self.free_time = 0.0

def process_heroes(number_of_heroes):
    heroes = []
    
    for _ in range(number_of_heroes):
        line = input().split()
        hero = Hero()
        hero.name = line[0]
        hero.level = line[1]
        hero.productivity = level_to_productivity(hero.level)
        heroes.append(hero)
    
    if DEBUG:
        print("DEBUG: HEROES PROCESSADOS")
        for h in heroes:
            print(f"  {h.name} ({h.level}): Prod = {h.productivity:.2f}")
    
    return heroes

def process_quests(number_of_quests):
    quests = []
    
    for _ in range(number_of_quests):
        line = list(map(int, input().split()))
        quest = Quest()
        quest.index = line[0]
        quest.base_time = line[1]
        
        # Processa dependências (ignora 0)
        quest.dependencies = []
        for dep in line[2:]:
            if dep != 0:
                quest.dependencies.append(dep)
        
        if DEBUG:
            deps_str = ",".join(map(str, quest.dependencies))
            print(f"DEBUG: QUEST {quest.index}: BaseTime = {quest.base_time}, Deps = {{{deps_str}}}")
        
        quests.append(quest)
    
    return quests

def topological_order(quests, M):
    """Realiza ordenação topológica das quests usando algoritmo de Kahn"""
    graph = [[] for _ in range(M + 1)]
    in_degree = [0] * (M + 1)
    
    # Constrói o grafo de dependências
    for quest in quests:
        for dep in quest.dependencies:
            graph[dep].append(quest.index)
            in_degree[quest.index] += 1
    
    if DEBUG:
        print("\nDEBUG: GRAFO DE DEPENDENCIAS E GRAU DE ENTRADA")
        for i in range(1, M + 1):
            if in_degree[i] > 0 or graph[i]:
                neighbors_str = ", ".join(map(str, graph[i]))
                print(f"  Quest {i} (inDegree={in_degree[i]}) precede: {neighbors_str}")
    
    queue = deque()
    topo_order = []
    
    # Adiciona quests sem dependências na fila
    for i in range(1, M + 1):
        if in_degree[i] == 0:
            queue.append(i)
    
    while queue:
        current = queue.popleft()
        topo_order.append(current)
        
        # Remove aresta e atualiza grau de entrada dos vizinhos
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if DEBUG:
        print("DEBUG: ORDEM TOPOLOGICA FINAL")
        order_str = " -> ".join(map(str, topo_order))
        print(f"  Ordem: {order_str}")
        
        if len(topo_order) != M:
            print(f"!!! ALERTA: CICLO DETECTADO NO GRAFO DE DEPENDENCIAS (TopoOrder size: {len(topo_order)}, M: {M}) !!!")
    
    return topo_order

def assign_quests(heroes, quests, M):
    
    topo_order = topological_order(quests, M)
    
    quest_index_map = {}
    for i, quest in enumerate(quests):
        quest_index_map[quest.index] = i
    

    for quest_index in topo_order:
        quest_array_index = quest_index_map[quest_index]
        current_quest = quests[quest_array_index]
        
        ready_time = 0.0
        for dep_index in current_quest.dependencies:
            dep_array_index = quest_index_map[dep_index]
            ready_time = max(ready_time, quests[dep_array_index].finish_time)
        current_quest.ready_time = ready_time
        
        if DEBUG:
            print(f"\nDEBUG: PROCESSANDO QUEST {quest_index} (baseTime={current_quest.base_time})")
            print(f"  ReadyTime (max finish das deps): {ready_time:.2f}")
        
        best_hero = -1
        best_finish_time = float('inf')
        
        for i, hero in enumerate(heroes):

            start_time = max(ready_time, hero.free_time)
            execution_time = current_quest.base_time / hero.productivity
            finish_time = start_time + execution_time
            

            if best_hero == -1 or finish_time < best_finish_time:
                best_finish_time = finish_time
                best_hero = i

            elif finish_time == best_finish_time:
                if i < best_hero:
                    best_hero = i
        
        heroes[best_hero].assigned_quests.append(quest_index)
        heroes[best_hero].free_time = best_finish_time
        current_quest.finish_time = best_finish_time
        
        if DEBUG:
            print(f"  ATRIBUIDO: Quest {quest_index} para Heroi {heroes[best_hero].name} (Prod={heroes[best_hero].productivity:.2f})")
            print(f"  FinishTime (Quest e Heroi): {best_finish_time:.2f}")
    
    min_time = 0.0
    for quest in quests:
        min_time = max(min_time, quest.finish_time)
    
    return min_time

def formatar_saida(heroes, min_time):
    for hero in heroes:
        quests_str = ",".join(map(str, hero.assigned_quests))
        print(f"{hero.name} = {{{quests_str}}}")
    
    print(f"Tempo mínimo: {min_time:.2f}")

def main():
    number_of_tests = int(input())
    
    for i in range(number_of_tests):
        number_of_heroes, number_of_quests = map(int, input().split())
        
        heroes = process_heroes(number_of_heroes)
        quests = process_quests(number_of_quests)
        
        min_time = assign_quests(heroes, quests, number_of_quests)
        formatar_saida(heroes, min_time)
        print() if i != number_of_tests - 1 else ""
        
if __name__ == "__main__":
    main()