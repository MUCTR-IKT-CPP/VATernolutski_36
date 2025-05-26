import random
import time
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Для AVL дерева

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return
        
        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = Node(key)
                    return
                current = current.left
            elif key > current.key:
                if current.right is None:
                    current.right = Node(key)
                    return
                current = current.right
            else:
                return  # Дубликаты не вставляем

    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, key):
        parent = None
        current = self.root
        
        # Поиск удаляемого узла
        while current is not None and current.key != key:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        
        if current is None:
            return  # Узел не найден
        
        # Случай 1: У узла нет детей или только один ребенок
        if current.left is None or current.right is None:
            new_child = current.left if current.left else current.right
            
            if parent is None:
                self.root = new_child
            else:
                if parent.left == current:
                    parent.left = new_child
                else:
                    parent.right = new_child
        else:
            # Случай 2: У узла два ребенка
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            
            current.key = successor.key
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Дубликаты не вставляем
        
        # Обновление высоты
        node.height = 1 + max(self._get_height(node.left),
                            self._get_height(node.right))
        
        # Балансировка
        balance = self._get_balance(node)
        
        # Left Left
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        
        # Right Right
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node

    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        
        if node is None:
            return node
        
        # Обновление высоты
        node.height = 1 + max(self._get_height(node.left),
                            self._get_height(node.right))
        
        # Балансировка
        balance = self._get_balance(node)
        
        # Left Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        
        # Left Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        
        # Right Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        
        # Right Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        
        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        z.height = 1 + max(self._get_height(z.left),
                         self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                         self._get_height(y.right))
        
        return y

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        y.height = 1 + max(self._get_height(y.left),
                         self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left),
                         self._get_height(x.right))
        
        return x

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

def run_tests():
    repeats = 2
    sizes = [2**(8+i) for i in range(12)]  # От 256 до 8192 элементов
    results = {
        'insert': {'BST': [], 'AVL': [], 'Array': []},
        'search': {'BST': [], 'AVL': [], 'Array': []},
        'delete': {'BST': [], 'AVL': [], 'Array': []}
    }

    for size in sizes:
        print(f"\nTesting size: {size}")
        
        # Инициализация результатов для текущего размера
        for op in results:
            for ds in results[op]:
                results[op][ds].append(0)
        
        for r in range(repeats):
            print(f"  Repeat {r+1}/{repeats}")
            
            # Генерация данных (первые 5 тестов - отсортированные, последние - случайные)
            if sizes.index(size) < 3:  # Первые 3 размера - отсортированные
                data = list(range(size))
            else:
                data = [random.randint(0, size*10) for _ in range(size)]
            
            random.shuffle(data)  # Для BST важно не передавать отсортированные данные
            
            # Тестирование вставки
            for ds in ['BST', 'AVL', 'Array']:
                start = time.time()
                
                if ds == 'BST':
                    tree = BST()
                    for num in data:
                        tree.insert(num)
                elif ds == 'AVL':
                    tree = AVLTree()
                    for num in data:
                        tree.insert(num)
                else:  # Array
                    arr = []
                    for num in data:
                        arr.append(num)
                
                results['insert'][ds][-1] += (time.time() - start)/repeats
            
            # Подготовка структур для тестов поиска/удаления
            bst = BST()
            avl = AVLTree()
            arr = []
            for num in data:
                bst.insert(num)
                avl.insert(num)
                arr.append(num)
            
            # Тестирование поиска (1000 операций)
            search_keys = random.sample(data, min(1000, size))
            for ds in ['BST', 'AVL', 'Array']:
                start = time.time()
                
                if ds == 'BST':
                    for key in search_keys:
                        bst.search(key)
                elif ds == 'AVL':
                    for key in search_keys:
                        avl.search(key)
                else:  # Array
                    for key in search_keys:
                        key in arr
                
                total_time = time.time() - start
                results['search'][ds][-1] += (total_time/len(search_keys))/repeats
            
            # Тестирование удаления (1000 операций)
            delete_keys = random.sample(data, min(1000, size))
            for ds in ['BST', 'AVL', 'Array']:
                start = time.time()
                
                if ds == 'BST':
                    for key in delete_keys:
                        bst.delete(key)
                elif ds == 'AVL':
                    for key in delete_keys:
                        avl.delete(key)
                else:  # Array
                    arr_copy = arr.copy()
                    for key in delete_keys:
                        if key in arr_copy:
                            arr_copy.remove(key)
                
                total_time = time.time() - start
                results['delete'][ds][-1] += (total_time/len(delete_keys))/repeats

    # Построение графиков
    operations = ['insert', 'search', 'delete']
    for op in operations:
        plt.figure(figsize=(10, 6))
        for ds in ['BST', 'AVL', 'Array']:
            plt.plot(sizes, results[op][ds], label=ds, marker='o')
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Number of elements')
        plt.ylabel('Time per operation (s)')
        plt.title(f'{op.capitalize()} performance comparison')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{op}_performance.png')
        plt.close()

    print("\nTesting completed!")
    print("Graphs saved as: insert_performance.png, search_performance.png, delete_performance.png")

if __name__ == '__main__':
    run_tests()