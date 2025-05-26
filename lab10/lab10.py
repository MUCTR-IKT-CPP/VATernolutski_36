import random
import itertools

# Все возможные комбинации из трёх цифр 0 и 1
combinations = list(itertools.product([0, 1], repeat=3))

# Функция для симуляции одной игры
def simulate_game(A, B, num_flips=100):
    # Генерируем случайную строку из 0 и 1
    flips = [random.randint(0, 1) for _ in range(num_flips)]
    # Преобразуем комбинации в строки
    A_str = ''.join(map(str, A))
    B_str = ''.join(map(str, B))
    # Проверяем последние три символа
    for i in range(2, num_flips):
        current = ''.join(map(str, flips[i-2:i+1]))
        if current == A_str:
            return 'A'
        elif current == B_str:
            return 'B'
    return 'None'  # Редкий случай, если ни одна комбинация не найдена

# Оценка вероятности победы A над B
def estimate_probability(A, B, num_simulations=10000):
    wins_A = 0
    for _ in range(num_simulations):
        winner = simulate_game(A, B)
        if winner == 'A':
            wins_A += 1
    return wins_A / num_simulations

# Построение таблицы вероятностей
def build_probability_table():
    table = {}
    for B in combinations:
        table[B] = {}
        for A in combinations:
            prob = estimate_probability(A, B)
            table[B][A] = prob
    return table

# Вывод таблицы
def print_table(table):
    print("Таблица вероятностей победы игрока A:")
    print("B \\ A", end='\t')
    for A in combinations:
        print(''.join(map(str, A)), end='\t')
    print()
    for B in combinations:
        print(''.join(map(str, B)), end='\t')
        for A in combinations:
            print(f"{table[B][A]:.4f}", end='\t')
        print()

# Средний шанс выигрыша
def calculate_average_probabilities(table):
    total_prob_A = 0
    num_pairs = 0
    for B in table:
        for A in table[B]:
            total_prob_A += table[B][A]
            num_pairs += 1
    avg_prob_A = total_prob_A / num_pairs
    avg_prob_B = 1 - avg_prob_A  # В каждой игре кто-то побеждает
    return avg_prob_A, avg_prob_B

# Основная функция
def main():
    table = build_probability_table()
    print_table(table)
    avg_prob_A, avg_prob_B = calculate_average_probabilities(table)
    print(f"\nСредний шанс выигрыша игрока A: {avg_prob_A:.4f}")
    print(f"Средний шанс выигрыша игрока B: {avg_prob_B:.4f}")

if __name__ == "__main__":
    main()