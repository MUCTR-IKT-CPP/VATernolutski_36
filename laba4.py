import random
import time
import os
import csv
import matplotlib.pyplot as plt

def format_time(t):
    if t < 1e-6:
        return "0s"
    elif t < 1e-3:
        return f"{t*1e6:.1f}µs"
    elif t < 1:
        return f"{t*1e3:.4g}ms"
    else:
        return f"{t:.4g}s"

class Graph:
    def __init__(self, vertices, edges=None, directed=False, edge_list=None):
        """
        Если edge_list задан, то граф создаётся по нему (для демонстрации);
        иначе генерируются случайные ребра (при условии, что edges не None).
        """
        self.vertices = vertices
        self.directed = directed
        self.adj_matrix = [[0 for _ in range(vertices)] for _ in range(vertices)]
        self.adj_list = {i: [] for i in range(vertices)}
        self.edge_list = []
        if edge_list is not None:
            self.edge_list = edge_list
            self.edges = len(edge_list)
            for (u, v) in edge_list:
                if u != v and self.adj_matrix[u][v] == 0:
                    self.adj_matrix[u][v] = 1
                    self.adj_list[u].append(v)
                    if not directed:
                        self.adj_matrix[v][u] = 1
                        self.adj_list[v].append(u)
        else:
            self.edges = edges if edges is not None else 0
            self.generate_edges()
        self.generate_inc_matrix()

    def generate_edges(self):
        """Генерация случайных рёбер для графа."""
        edge_count = 0
        random.seed(time.time_ns())
        while edge_count < self.edges:
            u = random.randint(0, self.vertices - 1)
            v = random.randint(0, self.vertices - 1)
            if u != v and self.adj_matrix[u][v] == 0:
                self.adj_matrix[u][v] = 1
                self.adj_list[u].append(v)
                self.edge_list.append((u, v))
                if not self.directed:
                    self.adj_matrix[v][u] = 1
                    self.adj_list[v].append(u)
                edge_count += 1

    def generate_inc_matrix(self):
        """Генерация матрицы инцидентности на основе списка рёбер."""
        num_edges = len(self.edge_list)
        self.inc_matrix = [[0 for _ in range(num_edges)] for _ in range(self.vertices)]
        for i, (u, v) in enumerate(self.edge_list):
            self.inc_matrix[u][i] = 1
            if not self.directed:
                self.inc_matrix[v][i] = 1

    def print_adj_matrix(self):
        print("Выдача матрицы смежности:")
        for row in self.adj_matrix:
            print("[" + " ".join(str(x) for x in row) + "]")

    def print_inc_matrix(self):
        print("Выдача матрицы инцидентности:")
        for row in self.inc_matrix:
            print("[" + " ".join(str(x) for x in row) + "]")

    def print_adj_list(self):
        print("Выдача списка смежности:")
        # Для вывода в том же порядке, что в примере, сортируем ключи по убыванию
        for vertex in sorted(self.adj_list.keys(), reverse=True):
            # Выводим соседей через пробел
            neighbors = " ".join(str(n) for n in self.adj_list[vertex])
            print(f"{vertex}: [{neighbors}]")

    def print_edge_list(self):
        print("Выдача списка ребер:")
        for (u, v) in self.edge_list:
            print(f"{u} - {v}")

    def BFS(self, start, target):
        """Проверка наличия пути от start до target методом поиска в ширину (BFS)."""
        visited = [False] * self.vertices
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node == target:
                return True
            if not visited[node]:
                visited[node] = True
                queue.extend(self.adj_list[node])
        return False

    def DFS(self, start, target):
        """Проверка наличия пути от start до target методом поиска в глубину (DFS)."""
        visited = [False] * self.vertices

        def dfs_recursive(node):
            if node == target:
                return True
            if visited[node]:
                return False
            visited[node] = True
            for neighbor in self.adj_list[node]:
                if dfs_recursive(neighbor):
                    return True
            return False

        return dfs_recursive(start)

    def shortest_path_bfs(self, start, target):
        """Нахождение кратчайшего пути от start до target с использованием BFS."""
        if start == target:
            return [start], True
        visited = [False] * self.vertices
        prev = [-1] * self.vertices
        queue = [start]
        visited[start] = True
        while queue:
            node = queue.pop(0)
            for neighbor in self.adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    prev[neighbor] = node
                    queue.append(neighbor)
                    if neighbor == target:
                        path = []
                        at = target
                        while at != -1:
                            path.insert(0, at)
                            at = prev[at]
                        return path, True
        return None, False

    def find_path_dfs(self, start, target):
        """Нахождение (любого) пути от start до target с использованием DFS."""
        visited = [False] * self.vertices
        path = []

        def dfs_recursive(node):
            if visited[node]:
                return False
            visited[node] = True
            path.append(node)
            if node == target:
                return True
            for neighbor in self.adj_list[node]:
                if dfs_recursive(neighbor):
                    return True
            path.pop()  
            return False

        if dfs_recursive(start):
            return path, True
        return None, False

def demo_graph_results():
    print("Результаты расчётов:")
    demo_edge_list = [(2,3), (1,0), (2,1), (1,4), (2,0),
                      (3,4), (2,4), (3,1), (0,4), (3,0)]
    demo_graph = Graph(5, directed=False, edge_list=demo_edge_list)
    demo_graph.print_adj_matrix()
    demo_graph.print_inc_matrix()
    demo_graph.print_adj_list()
    demo_graph.print_edge_list()

    start, target = 0, 4
    bfs_path, bfs_found = demo_graph.shortest_path_bfs(start, target)
    dfs_path, dfs_found = demo_graph.find_path_dfs(start, target)
    if bfs_found:
        print(f"Кратчайший путь (BFS) из {start} в {target}: " + "[" + " ".join(str(x) for x in bfs_path) + "]")
    else:
        print(f"BFS: Пути из {start} в {target} не существует")
    if dfs_found:
        print(f"Путь (DFS) из {start} в {target}: " + "[" + " ".join(str(x) for x in dfs_path) + "]")
    else:
        print(f"DFS: Пути из {start} в {target} не существует")
    print(f"Длина пути (BFS): {len(bfs_path) if bfs_path else 0}")
    print(f"Длина пути (DFS): {len(dfs_path) if dfs_path else 0}")

def run_performance_test(test_name, vertices_list, edge_multiplier, directed=False):
    results = []  # каждый элемент: (V, E, DFS_time, BFS_time)
    for V in vertices_list:
        E = V * edge_multiplier
        graph = Graph(V, edges=E, directed=directed)
        start, target = 0, V - 1

        t1 = time.perf_counter_ns()
        graph.DFS(start, target)
        t2 = time.perf_counter_ns()
        dfs_time = (t2 - t1) / 1e9

        t1 = time.perf_counter_ns()
        graph.BFS(start, target)
        t2 = time.perf_counter_ns()
        bfs_time = (t2 - t1) / 1e9

        results.append((V, E, dfs_time, bfs_time))
    print(f"\n{test_name}:")
    print("V, E, DFS, BFS")
    for (V, E, dfs_t, bfs_t) in results:
        print(f"{V},{E},{format_time(dfs_t)},{format_time(bfs_t)}")
    return results

def plot_performance(test_name, results):
    vertices = [r[0] for r in results]
    dfs_times = [r[2] for r in results]
    bfs_times = [r[3] for r in results]
    plt.figure(figsize=(8, 6))
    plt.title(f"BFS vs DFS Execution Times ({test_name})")
    plt.xlabel("Number of Vertices")
    plt.ylabel("Time (s)")
    plt.plot(vertices, dfs_times, color='blue', marker='o', label='DFS')
    plt.plot(vertices, bfs_times, color='red', marker='o', label='BFS')
    plt.legend()
    filename = f"results_{test_name}.png"
    plt.savefig(filename)
    print(f"Сохранён график: {filename}")

def main():
    demo_graph_results()

    
    vertices_test1 = list(range(100, 1001, 100))
    res1 = run_performance_test("Test1", vertices_test1, edge_multiplier=20, directed=False)
    plot_performance("Test1", res1)

    vertices_test2 = list(range(100, 1001, 100))
    res2 = run_performance_test("Test2", vertices_test2, edge_multiplier=20, directed=True)
    plot_performance("Test2", res2)

    vertices_test3 = list(range(10, 101, 10))
    res3 = run_performance_test("Test3", vertices_test3, edge_multiplier=2, directed=False)
    plot_performance("Test3", res3)

    vertices_test4 = list(range(10, 101, 10))
    res4 = run_performance_test("Test4", vertices_test4, edge_multiplier=2, directed=True)
    plot_performance("Test4", res4)

    csv_filename = "performance.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Test", "Vertices", "Edges", "DFS_time", "BFS_time"])
        for test_name, res in zip(["Test1", "Test2", "Test3", "Test4"], [res1, res2, res3, res4]):
            for (V, E, dfs_t, bfs_t) in res:
                writer.writerow([test_name, V, E, format_time(dfs_t), format_time(bfs_t)])
    print(f"\nРезультаты замеров записаны в {csv_filename}")

if __name__ == "__main__":
    main()

