#include <iostream>
#include <vector>

/*
Заплнение массива числами от 1 до N*N
@param matrix двумерный массив
@param N размер массива
*/

void fillMatrix(std::vector<std::vector<int>>& matrix, int N) {
    int value = 1;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            matrix[i][j] = value++;
        }
    }
}

/*
Ввод массива на экран
@param matrix двумерный массив
@param N размер массива
*/

void printMatrix(const std::vector<std::vector<int>>& matrix, int N) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << std::endl;
    }
}

/*
Переворот массива в обратный порядок
@param matrix двумерный массив
@param N размер массива
*/

void reverseMatrix(std::vector<std::vector<int>>& matrix, int N) {
    int value = N*N;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            matrix[i][j] = value--;
        }
    }
}

/*
Заполнение массива вдоль главной диагонали
@param matrix двумерный массив
@param N размер массива
*/

void fillMainDiagonal(std::vector<std::vector<int>>& matrix, int N) {
    int value = 1;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (i == j) {
                matrix[i][j] = value++;
            } else {
                matrix[i][j] = 0;
            }
        }
    }
}

/*
Заполнение массива вдоль побочной диагонали
@param matrix двумерный массив
@param N размер массива
*/

void fillSecondDiagonal(std::vector<std::vector<int>>& matrix, int N) {
    int value = 1;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (i + j == N - 1) {
                matrix[i][j] = value++;
            } else {
                matrix[i][j] = 0;
            }
        }
    }
}

/*
Заполнение массива по спирали
@param matrix двумерный массив
@param N размер массива
*/

void fillSpiral(std::vector<std::vector<int>>& matrix, int N) {
    int value = 1;
    int top = 0, bottom = N - 1, left = 0, right = N - 1;

    while (value <= N*N) {
        for (int i = left; i <= right; i++){
            matrix[top][i] = value++;
        }
        ++top;
        for (int i = top; i <= bottom; i++) {
            matrix[i][right] = value++;
        }
        --right;

        for (int i = right; i >= left; --i) {
            matrix[bottom][i] = value++;
        }
        ++left;

    }
}

int main() {
    int N;

    // Ввод N 
    std::cout << "Введите размер матрицы N: ";
    std::cin >> N;

    //Создание массива N*N
    std::vector<std::vector<int>> matrix(N, std::vector<int>(N));

    //Заполнение массива
    fillMatrix(matrix, N);

    std::cout << "Исходная матрица:" << std::endl;
    printMatrix(matrix, N);

    int choice;
    std::cout << "Выберите действие: \n"
              << "1 - Обратный порядок\n"
              << "2 - Главная диагональ\n"
              << "3 - Побочная диагональ\n"
              << "4 - Спираль заполнение\n"
              << "Ваш выбор: ";
    std::cin >> choice;

    switch (choice) {
        case 1:
            reverseMatrix(matrix, N);
            std::cout << "Обратный порядок элементов матрицы:" << std::endl;
            break;
        case 2:
            fillMainDiagonal(matrix, N);
            std::cout << "Элементы матирицы вдоль главной диагонали:" << std::endl;
            break;
        case 3:
            fillSecondDiagonal(matrix, N);
            std::cout << "Элементы матрицы вдоль побочный диагонали:" <<std::endl;
            break;
        case 4:
            fillSpiral(matrix, N);
            std::cout << "Спиральное заполнение матрицы:" <<std::endl;
            break;
        default:
            std::cout << "Неправильное значение, попробуйте другое:\n"
                      << "1 - Обратный порядок\n"
                      << "2 - Главная диагональ\n"
                      << "3 - Побочная диагональ\n"
                      << "4 - Спираль заполнение\n";
            return 1;                  
    }

    printMatrix(matrix, N);

    return 0;
}