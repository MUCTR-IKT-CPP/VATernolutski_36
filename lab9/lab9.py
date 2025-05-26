import hashlib
import random
import string
import timeit
import matplotlib.pyplot as plt

# Генерация случайной строки заданной длины
def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Модификация строки на заданное количество символов
def modify_string(s, num_changes):
    indices = random.sample(range(len(s)), num_changes)
    new_s = list(s)
    for idx in indices:
        new_s[idx] = random.choice(string.ascii_letters + string.digits)
    return ''.join(new_s)

# Поиск длины самой длинной общей подпоследовательности
def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

# Тест 1: Анализ коллизий
def test_collisions():
    differences = [1, 2, 4, 8, 16]
    results = {}
    for diff in differences:
        max_seq_lengths = []
        for _ in range(1000):
            base = generate_string(128)
            modified = modify_string(base, diff)
            hash1 = hashlib.md5(base.encode()).hexdigest()
            hash2 = hashlib.md5(modified.encode()).hexdigest()
            max_seq = longest_common_subsequence(hash1, hash2)
            max_seq_lengths.append(max_seq)
        results[diff] = max(max_seq_lengths)
    return results

# Тест 2: Поиск одинаковых хешей
def generate_hashes(n):
    hashes = set()
    collisions = 0
    for _ in range(n):
        s = generate_string(256)
        h = hashlib.md5(s.encode()).hexdigest()
        if h in hashes:
            collisions += 1
        else:
            hashes.add(h)
    return collisions

def test_hash_collisions():
    ns = [10**i for i in range(2, 7)]
    results = {}
    for n in ns:
        collisions = generate_hashes(n)
        results[n] = collisions
    return results

# Тест 3: Анализ времени вычисления
def measure_hash_time(length, num_trials=1000):
    total_time = 0
    for _ in range(num_trials):
        s = generate_string(length)
        start = timeit.default_timer()
        hashlib.md5(s.encode()).hexdigest()
        end = timeit.default_timer()
        total_time += end - start
    return total_time / num_trials

def test_hash_time():
    lengths = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    results = {}
    for length in lengths:
        avg_time = measure_hash_time(length)
        results[length] = avg_time
    return results

# Построение графиков
def plot_results(collision_results, time_results):
    # График для теста 1
    plt.figure()
    plt.plot(list(collision_results.keys()), list(collision_results.values()), marker='o')
    plt.xlabel('Количество отличий')
    plt.ylabel('Максимальная длина одинаковой последовательности')
    plt.title('Анализ коллизий MD5')
    plt.grid(True)
    plt.savefig('collision_analysis.png')

    # График для теста 3
    plt.figure()
    plt.plot(list(time_results.keys()), list(time_results.values()), marker='o')
    plt.xlabel('Длина строки')
    plt.ylabel('Среднее время вычисления (с)')
    plt.title('Время вычисления хеша MD5')
    plt.grid(True)
    plt.savefig('hash_time_analysis.png')

# Выполнение тестов
if __name__ == "__main__":
    # Тест 1
    collision_results = test_collisions()
    print("Тест 1: Максимальная длина одинаковых последовательностей в хешах:")
    for diff, max_len in collision_results.items():
        print(f"Отличий: {diff}, Макс. длина: {max_len}")

    # Тест 2
    hash_collision_results = test_hash_collisions()
    print("\nТест 2: Количество коллизий:")
    print("| N генераций | Количество одинаковых хешей |")
    print("|-------------|-----------------------------|")
    for n, collisions in hash_collision_results.items():
        print(f"| {n:<11} | {collisions:<27} |")

    # Тест 3
    hash_time_results = test_hash_time()
    print("\nТест 3: Среднее время вычисления хеша:")
    for length, avg_time in hash_time_results.items():
        print(f"Длина строки: {length}, Среднее время: {avg_time:.6f} сек")

    # Построение графиков
    plot_results(collision_results, hash_time_results)
    print("\nГрафики сохранены как 'collision_analysis.png' и 'hash_time_analysis.png'")