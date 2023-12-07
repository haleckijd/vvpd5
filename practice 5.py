"""Модуль реализует алгоритм Дейкстры"""

import random

import copy


def int_check():
    """
    Проверяет входные данные на целочисленный тип

    Returns:
        var: исло, полученное от пользователя

    Raises:
        ValueError
    """
    var = input()
    try:
        int(var)
    except ValueError:
        print('Ошибка. Некорректный тип данных. Введите число')
        var = int_check()
    return int(var)


def read_and_positive_check():
    """
    Считывает число, и проверяет его на неотрицательность

    Returns:
        var: Целое положительное число
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
    Создает матрицу смежности графа

    Returns:
        (matrix, matrix_1, vertices_number): Кортеж, состоящий из матрицы смежности
         для вывода на экран, матрицы смежности для внутренних вычислений,
        порядка матрицы смежности (количество вершин графа)
    """
    print('Введите количество вершин графа')
    vertices_number = read_and_positive_check()
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
    Выводит матрицу смежности на экран

    Args:
        matrix: Матрица смежности графа
    """
    for i in enumerate(matrix):
        for j in enumerate(matrix):
            print(matrix[i[0]][j[0]],
                  end=' ' * (5 - len(str(matrix[i[0]][j[0]]))))
        print()


def get_start(order):
    """
    Ввод начальной вершины графа для дальнейшего поиска
    оптимального маршрута

    Args:
        order: Порядок матрицы смежности (количество вершин графа)

    Returns:
        start: Стартовая вершина графа

    Examples:
        >> get_start(5)
        >? 4
        4
        >> get_start(5)
        >? r
        Ошибка. Некорректный тип данных. Введите число
        >> get_start(5)
        >?6
        Такой вершины нет. Введите число еще раз
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
    Ввод конечной вершины графа для дальнейшего поиска
    оптимального маршрута

    Args:
        order: Порядок матрицы смежности (количество вершин графа)

    Returns:
        end: Конечная вершина графа
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
    Ищет оптимальный путь с помощью алгоритма Дейкстры

    Args:
        matrix: Матрица смежности графа
        order: Порядок матрицы смежности (количество вершин графа)
        start_vertex: Стартовая вершина
        end_vertex: Конечная вершина

    Returns:
        (length, result): tuple - кортеж, состоящий из длины самого
        оптимального пути из стартовой вершины в конечную и списка состоящего
        из номеров вершин графа, из которого состоит самый оптимальный путь
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
    Реализует меню программы
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
