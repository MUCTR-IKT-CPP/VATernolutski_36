#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>

/*
 * Структура для представления строки
 *
 * @param length длина строки.
 * @param data указатель на массив символов строки.
 */
struct String {
    int length;
    char *data;
};

/*
 * Генерация случайной строки длиной length символов
 *
 * @param str указатель на строку, куда будет записана сгенерированная строка.
 * @param length длина генерируемой строки.
 */
void generateRandomString(char *str, int length) {
    for (int i = 0; i < length; ++i) {
        // Генерация случайного числа, которое будет либо строчной буквой (a-z), либо заглавной (A-Z)
        int randomChoice = std::rand() % 2; // 0 для строчной буквы, 1 для заглавной
        if (randomChoice == 0) {
            str[i] = 'a' + std::rand() % 26; // Генерируем строчную букву (a-z)
        } else {
            str[i] = 'A' + std::rand() % 26; // Генерируем заглавную букву (A-Z)
        }
    }
    str[length] = '\0'; // Завершающий символ
}


/*
 * Подсчет количества повторений символа в массиве строк
 *
 * @param array массив строк.
 * @param ch символ, который нужно найти.
 * @return возвращает количество повторений символа.
 */
int countCharacterOccurrences(const std::vector<String> &array, char ch) {
    int count = 0;
    for (const auto &str : array) {
        for (int i = 0; i < str.length; ++i) {
            if (str.data[i] == ch) {
                ++count;
            }
        }
    }
    return count;
}

/*
 * Поиск максимальной повторяющейся последовательности символов в массиве строк
 *
 * @param array массив строк.
 * @return возвращает строку с максимальной последовательностью повторяющихся символов.
 */
std::string findMaxRepeatedSequence(const std::vector<String> &array) {
    std::string maxSequence;
    for (const auto &str : array) {
        std::string currentSequence;
        for (int i = 0; i < str.length - 1; ++i) {
            currentSequence += str.data[i];
            if (str.data[i] != str.data[i + 1]) {
                if (currentSequence.length() > maxSequence.length()) {
                    maxSequence = currentSequence;
                }
                currentSequence = "";
            }
        }
        if (currentSequence.length() > maxSequence.length()) {
            maxSequence = currentSequence;
        }
    }
    return maxSequence;
}

/*
 * Объединение всех строк в массиве в одну строку
 *
 * @param array массив строк.
 * @return возвращает объединённую строку.
 */
std::string concatenateStrings(const std::vector<String> &array) {
    std::string result;
    for (const auto &str : array) {
        result += std::string(str.data);
    }
    return result;
}

/*
 * Подсчет количества вхождений подстроки в массиве строк
 *
 * @param array массив строк.
 * @param substring подстрока, которую нужно найти.
 * @return возвращает количество вхождений подстроки.
 */
int countSubstringOccurrences(const std::vector<String> &array, const std::string &substring) {
    int count = 0;
    for (const auto &str : array) {
        std::string fullStr = std::string(str.data);
        std::size_t pos = fullStr.find(substring);
        while (pos != std::string::npos) {
            ++count;
            pos = fullStr.find(substring, pos + 1);
        }
    }
    return count;
}

int main() {
    std::srand(static_cast<unsigned int>(std::time(0)));

    int N;
    std::cout << "Введите число N: ";
    std::cin >> N;

    // Создание массива строк типа "Строка" и "std::string"
    std::vector<String> customStrings(N);
    std::vector<std::string> stdStrings(N);

    // Генерация случайных строк длиной 50 символов
    for (int i = 0; i < N; ++i) {
        customStrings[i].length = 50;
        customStrings[i].data = new char[51]; // Массив для строки длиной 50 символов
        generateRandomString(customStrings[i].data, 50);
        stdStrings[i] = std::string(customStrings[i].data); // Записываем строку в std::string
    }

    // Пример использования функций
    char symbol;
    std::cout << "Введите символ для поиска его повторений: ";
    std::cin >> symbol;
    int occurrences = countCharacterOccurrences(customStrings, symbol);
    std::cout << "Символ '" << symbol << "' встречается " << occurrences << " раз(а)." << std::endl;

    std::string maxSequence = findMaxRepeatedSequence(customStrings);
    std::cout << "Максимальная повторяющаяся последовательность: " << maxSequence << std::endl;

    std::string concatenated = concatenateStrings(customStrings);
    std::cout << "Объединённая строка: " << concatenated.substr(0, 100) << "..." << std::endl; // выводим первые 100 символов

    std::string substring;
    std::cout << "Введите подстроку для поиска: ";
    std::cin >> substring;
    int substringOccurrences = countSubstringOccurrences(customStrings, substring);
    std::cout << "Подстрока '" << substring << "' встречается " << substringOccurrences << " раз(а)." << std::endl;

    // Очистка динамически выделенной памяти
    for (int i = 0; i < N; ++i) {
        delete[] customStrings[i].data;
    }

    return 0;
}
