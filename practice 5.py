"""Модуль реализует алгоритм Дейкстры"""

import random

import copy


def int_check():
    """
    Функция проверки входных данных на целочисленный тип

    Параметры
    _________
    None

    Возвращаемое значение
    _____________________
    var: int - число, полученное от пользователя

    Исключения
    __________
    ValueError, генерируется в том случае, если от пользователя
    получено не целое число, а например буква, знаки препинания и тп.

    Пример использования
    _____________

    Пример использования:
    ____________________
    При вызове данной функции в ходе выполнения программы, функция потребует у
    пользователя ввести число в консоль, однако, пользователь не обязательно
    введет число, что приведет к исключению.
    Например, при вводе 5, 7, 32, -43 исключения не сгенерируется,
    и функция вернет введенные числа. При вводе rtr, /9, (), _, g сгенерируется
    исключение ValueError, и пользователя попросят ввести число еще раз, до тех
    пор, пока он не введет число.
    """
    var = input()
    try:
        int(var)
    except ValueError:
        print('Ошибка. Некорректный тип данных. Введите число')
        var = int_check()
    return int(var)


def positive_check():
    """
    Функции проверки числа на положительный тип

    Параметры
    _________
    None

    Возвращаемое значение
    _____________________
    var: int - целое положительное число
    """
    var = int_check()
    while True:
        if var < 0:
            print('Ошибка. Число должно быть положительным. '
                  'Введите число еще раз')
            var = int_check()
        else:
            return var


def matrix_generation():
    """
    Функция создания матрицы смежности

    Параметры
    _________
    None

    Возвращаемое значение
    _____________________
    (matrix, matrix_1, vertices_number): tuple - кортеж, состоящий из:
    matrix: list - матрица смежности графа для вывода на экран
    matrix_1: list - матрица смежности графа для внутренних вычислений
    vertices_number: int - порядок матрицы смежности (количество вершин графа)
    """
    print('Введите количество вершин графа')
    vertices_number = positive_check()
    matrix = []
    for i in range(vertices_number):
        matrix.append([random.randint(0, 9)
                       for _ in range(vertices_number)])

    for i in range(vertices_number):
        for j in range(i, vertices_number):
            matrix[i][j] = matrix[j][i] = random.randint(0, 10)
    for i in range(vertices_number):
        for j in range(vertices_number):
            if matrix[i][j] == 0:
                matrix[i][j] = 'INF'

    for i in range(vertices_number):
        matrix[i][i] = 0

    matrix_1 = copy.deepcopy(matrix)
    for i in range(vertices_number):
        for j in range(vertices_number):
            if matrix_1[i][j] == 'INF':
                matrix_1[i][j] = 100000

    return matrix, matrix_1, vertices_number


def print_matrix(matrix):
    """
    Функция вывода матрицы смежности на экран

    Параметры
    _________
    matrix: list - матрица смежности графа

    Возвращаемое значение
    _____________________
    None
    """
    for i in enumerate(matrix):
        for j in enumerate(matrix):
            print(matrix[i[0]][j[0]],
                  end=' ' * (5 - len(str(matrix[i[0]][j[0]]))))
        print()


def get_start(order):
    """
    Функция ввода начальной вершины графа для дальнейшего поиска
    оптимального маршрута

    Параметры
    _________
    order: int - порядок матрицы смежности (количество вершин графа)

    Возвращаемое значение
    ____________________
    start: int - стартовая вершина графа
    """
    print('Введите стартовую вершину, отчёт начинается с нуля')
    while True:
        flag = False
        start = int_check()
        for i in range(0, order):
            if start == i:
                flag = True
        if not flag:
            print('Такой вершины нет. Введите число еще раз')
        else:
            break
    return start


def get_end(order):
    """
    Функция ввода конечной вершины графа для дальнейшего поиска
    оптимального маршрута

    Параметры
    _________
    order: int - порядок матрицы смежности (количество вершин графа)

    Возвращаемое значение
    ____________________
    end: int - конечная вершина графа
    """
    print('Введите стартовую вершину, отчёт начинается с нуля')
    while True:
        flag = False
        end = int_check()
        for i in range(0, order):
            if end == i:
                flag = True
        if not flag:
            print('Такой вершины нет. Введите число еще раз')
        else:
            break
    return end


def dijkstra_algorithm(matrix, order, start_vertex, end_vertex):
    """
    Функция поиска оптимального пути с помощью алгоритма Дейкстры

    Параметры
    _________
    matrix: list - матрица смежности графа
    order: int - порядок матрицы смежности (количество вершин графа)
    start_vertex: int - стартовая вершина
    end_vertex: int - конечная вершина

    Возвращаемое значение
    _____________________
    (length, result): tuple - кортеж, состоящий из:
    length: int - длина самого оптимального пути из стартовой вершины в
    конечную
    result: list - список, состоящий из номеров вершин графа, из которого
    состоит самый оптимальный путь
    """
    inf = 100000
    dist = [inf] * order
    dist[start_vertex] = 0
    used = [False] * order
    min_dist = 0
    min_vertex = start_vertex
    way = []
    for i in range(order):
        way.append([])
    while min_dist < inf:
        i = min_vertex
        used[i] = True
        for j in range(order):
            if dist[i] + matrix[i][j] < dist[j]:
                dist[j] = dist[i] + matrix[i][j]
                way[j].append(i)
        min_dist = inf
        for j in range(order):
            if not used[j] and dist[j] < min_dist:
                min_dist = dist[j]
                min_vertex = j
    length = dist[end_vertex]
    for i in range(order):
        way[i].append(i)
    way[0].insert(0, start_vertex)
    result = way[end_vertex]
    if result[0] != start_vertex:
        result.insert(0, start_vertex)
    elif result[0] == result[1] == start_vertex:
        result.pop(0)
    return length, result


def main():
    """
    Функция, реализующая меню программы

    Параметры
    _________
    None

    Возвращаемое значение
    _____________________
    None
    """
    matrix_create = False
    start_create = False
    output_matrix = None
    matrix = None
    order = None
    start_vertex = None
    end_vertex = None

    while True:
        print('Список команд')
        print('\t1. Создать матрицу смежности')
        print('\t2. Вывести матрицу смежности')
        print('\t3. Задать начальную и конечную вершину')
        print('\t4. Найти расстояние между вершинами')
        print('\t5. Закончить выполнение программы\n')
        print('Введите номер команды')
        command_number = int_check()
        if command_number == 1:
            output_matrix, matrix, order = matrix_generation()
            matrix_create = True
        elif command_number == 2 and matrix_create:
            print_matrix(output_matrix)
        elif command_number == 3 and matrix_create:
            start_vertex = get_start(order)
            end_vertex = get_end(order)
            start_create = True
        elif command_number == 4 and matrix_create and start_create:
            answer, way = dijkstra_algorithm(matrix, order,
                                             start_vertex,
                                             end_vertex)
            way = tuple(way)
            print(
                f"Минимальный путь из вершины {start_vertex} до вершины "
                f"{end_vertex} - {answer}")
            print("Путь - ", way)
        elif command_number == 5:
            break
        else:
            print(
                'Такой команды нет или матрица не была создана')


if __name__ == "__main__":
    main()


