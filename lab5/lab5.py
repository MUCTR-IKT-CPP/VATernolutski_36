import random
import time
import heapq
import matplotlib.pyplot as plt

def generate_graph(n, min_edges):
    matrix = [[0] * n for _ in range(n)]
    # Создание связного графа (дерева)
    added = {0}
    remaining = set(range(1, n))
    while remaining:
        u = random.choice(list(added))
        v = random.choice(list(remaining))
        weight = random.randint(1, 20)
        matrix[u][v] = weight
        matrix[v][u] = weight
        added.add(v)
        remaining.remove(v)
    
    # Добавление рёбер до достижения минимальной степени
    for _ in range(n * 2):  # Ограничение числа попыток
        all_ok = True
        for u in range(n):
            current_degree = sum(1 for x in matrix[u] if x != 0)
            if current_degree < min_edges:
                all_ok = False
                possible = [v for v in range(n) if v != u and matrix[u][v] == 0]
                needed = min_edges - current_degree
                if len(possible) < needed:
                    needed = len(possible)
                if needed == 0:
                    continue
                selected = random.sample(possible, needed)
                for v in selected:
                    weight = random.randint(1, 20)
                    matrix[u][v] = weight
                    matrix[v][u] = weight
        if all_ok:
            break
    return matrix

def prim_optimized(matrix):
    n = len(matrix)
    key = [float('inf')] * n
    parent = [-1] * n
    key[0] = 0
    heap = []
    heapq.heappush(heap, (0, 0))
    in_tree = set()
    
    while heap:
        weight, u = heapq.heappop(heap)
        if u in in_tree:
            continue
        in_tree.add(u)
        for v in range(n):
            if matrix[u][v] != 0 and v not in in_tree and matrix[u][v] < key[v]:
                key[v] = matrix[u][v]
                parent[v] = u
                heapq.heappush(heap, (key[v], v))
    
    edges = []
    for v in range(1, n):
        if parent[v] != -1:
            edges.append((parent[v], v, key[v]))
    return edges

def print_adjacency_matrix(matrix):
    print("Матрица смежности:")
    for row in matrix:
        print(' '.join(map(str, row)))

def main():
    sizes = [10, 20, 50, 100]
    min_edges_list = [3, 4, 10, 20]
    tests_per_size = 5
    time_results = {n: [] for n in sizes}
    
    for n, min_edges in zip(sizes, min_edges_list):
        print(f"\nОбработка графа с {n} вершинами...")
        for test in range(tests_per_size):
            print(f"Тест {test + 1}/{tests_per_size}")
            # Генерация графа
            start_gen = time.time()
            graph = generate_graph(n, min_edges)
            end_gen = time.time()
            print(f"Время генерации: {end_gen - start_gen:.2f} сек")
            
            if n <= 10 and test == 0:  # Печать матрицы для малых графов
                print_adjacency_matrix(graph)
            
            # Замер времени алгоритма Прима
            start_prim = time.time()
            prim_optimized(graph)
            end_prim = time.time()
            time_taken = end_prim - start_prim
            time_results[n].append(time_taken)
            print(f"Время Прима: {time_taken:.4f} сек")
        
        avg_time = sum(time_results[n]) / tests_per_size
        time_results[n] = avg_time
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, [time_results[n] for n in sizes], marker='o', linestyle='-', color='b')
    plt.xlabel('Количество вершин (N)')
    plt.ylabel('Среднее время выполнения (сек)')
    plt.title('Зависимость времени выполнения алгоритма Прима от размера графа')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()