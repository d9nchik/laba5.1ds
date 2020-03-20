import copy


class Heights:
    def __init__(self, position, weight, father):
        self.position = position
        self.weight = weight
        self.father = father


def get_data():
    e_data = []
    with open("input.txt") as iFile:
        while True:
            line = iFile.readline()
            if not line:
                break
            temp = list(map(int, (line[:len(line)] + line[len(line) + 1:]).split()))
            e_data.append(temp)
            print(line, end='')
        print()
    return e_data


def create_adjacency_matrix(e_data):
    matrix = [0] * e_data[0][0]
    for x in range(e_data[0][0]):
        matrix[x] = [0] * e_data[0][0]

    for y in range(1, len(e_data)):
        if e_data[y][2] <= 0:
            print("Для алгоритму Дейкстри ваги не можуть бути від'ємними")
            exit(1)
        matrix[e_data[y][0] - 1][e_data[y][1] - 1] = e_data[y][2]
    return matrix


def find_minimum_weight(unvisited):
    y = 0
    for x in range(len(unvisited)):
        if unvisited[y].weight > unvisited[x].weight:
            y = x
    return y


def close_height(adjacency_matrix, height):
    for x in range(len(adjacency_matrix)):
        adjacency_matrix[x][height] = 0


def find_neighbours(matrix_of_unvisited, height):
    positions_of_neighbour = []
    for x in range(len(matrix_of_unvisited)):
        if matrix_of_unvisited[height][x] != 0:
            positions_of_neighbour.append(x)
    return positions_of_neighbour


def position_in_array(unvisited, searched_position):
    for x in range(len(unvisited)):
        if unvisited[x].position == searched_position:
            return x
    return -1


def dijkstra_algorithm_multiple(adjacency_matrix, height):
    matrix_of_unvisited = copy.deepcopy(adjacency_matrix)
    visited = []
    unvisited = [Heights(height, 0, None)]
    while len(unvisited) > 0:
        position_of_minimum = find_minimum_weight(unvisited)
        visited.append(unvisited[position_of_minimum])
        dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited)
        return visited


def show_path_dijkstra_multiple(dijkstra_data, size):
    for x in range(size):
        path = [Heights(None, None, x)]
        show_path_dijkstra_main_part(dijkstra_data, path)


def show_path_dijkstra_main_part(dijkstra_data, path):
    for y in range(len(dijkstra_data) - 1, 0, -1):
        if path[-1].father == dijkstra_data[y].position:
            path.append(dijkstra_data[y])
    del path[0]
    if len(path) != 0:
        path.reverse()
        for z in range(0, len(path)):
            print(path[z].father + 1, end=" - > ")
        print("%s Шлях = %s" % (path[-1].position + 1, path[-1].weight))


def dijkstra_algorithm_single(adjacency_matrix, height_start, height_finish):
    matrix_of_unvisited = copy.deepcopy(adjacency_matrix)
    visited = []
    unvisited = [Heights(height_start, 0, None)]
    while len(unvisited) > 0:
        position_of_minimum = find_minimum_weight(unvisited)
        visited.append(unvisited[position_of_minimum])
        if height_finish == visited[-1].position:
            break
        dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited)
    return visited


def dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited):
    close_height(matrix_of_unvisited, visited[-1].position)
    del unvisited[position_of_minimum]
    neighbours = find_neighbours(matrix_of_unvisited, visited[-1].position)
    for x in neighbours:
        position_of_neighbour = position_in_array(unvisited, x)
        if position_of_neighbour == -1:
            unvisited.append(
                Heights(x, matrix_of_unvisited[visited[-1].position][x] + visited[-1].weight, visited[-1].position))
        elif unvisited[position_of_neighbour].weight > matrix_of_unvisited[visited[-1].position][x] \
                + visited[-1].weight:
            unvisited[position_of_neighbour].weight = matrix_of_unvisited[visited[-1].position][
                                                          x] + visited[-1].weight
            unvisited[position_of_neighbour].father = visited[-1].position


def show_path_dijkstra_single(dijkstra_data):
    path = [Heights(None, None, dijkstra_data[-1].position)]
    show_path_dijkstra_main_part(dijkstra_data, path)


def create_floyd_distance_matrix(e_data):
    matrix = [0] * e_data[0][0]
    for x in range(e_data[0][0]):
        matrix[x] = [float('inf')] * e_data[0][0]

    for y in range(1, len(e_data)):
        matrix[e_data[y][0] - 1][e_data[y][1] - 1] = e_data[y][2]
    for x in range(len(matrix)):
        matrix[x][x] = 0
    return matrix


def create_floyd_history_matrix(size):
    matrix = [0] * size
    for x in range(size):
        matrix[x] = [x + 1] * size
    for y in range(size):
        matrix[y][y] = 0
    return matrix


def floyd_algorithm(e_data):
    distance_matrix_floyd = create_floyd_distance_matrix(e_data)
    size = len(distance_matrix_floyd)
    history_matrix_floyd = create_floyd_history_matrix(size)
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if distance_matrix_floyd[y][z] > distance_matrix_floyd[y][x] + distance_matrix_floyd[x][z]:
                    distance_matrix_floyd[y][z] = distance_matrix_floyd[y][x] + distance_matrix_floyd[x][z]
                    history_matrix_floyd[y][z] = x + 1
    for i in range(size):
        if history_matrix_floyd[i][i] != 0:
            print("У матриці не можуть бути від'ємні цикли: ")
            exit(2)
    return history_matrix_floyd, distance_matrix_floyd


def show_matrix(matrix):
    for i in matrix:
        for j in i:
            print("%3d" % j, end=" ")
        print()


def show_floyd_path(floyd_history_matrix, start_point, end_point):
    previous_point = float('inf')
    while start_point != previous_point:
        print(start_point, end="->")
        previous_point = start_point
        start_point = floyd_history_matrix[start_point - 1][end_point - 1]
    print(end_point)


print("Виберіть алгоритм Дейкстра(1), Флойда-Уоршела(2)")
choice = int(input("Варіант: "))
if choice == 1:
    matrixOfAdjacency = create_adjacency_matrix(get_data())
    print(
        "Визначити найкоротший маршрут між двома вершинами та його довжину(1) чи Визначити найкоротшу відстань від "
        "заданої вершини до всіх інших вершин(2)")
    choice = int(input("Варіант: "))
    if choice == 1:
        heightStart = int(input("Введіть вершину початку: ")) - 1
        heightFinish = int(input("Введіть вершину кінця: ")) - 1
        show_path_dijkstra_single(dijkstra_algorithm_single(matrixOfAdjacency, heightStart, heightFinish))
    elif choice == 2:
        heightStart = int(input("Введіть вершину початку: "))
        show_path_dijkstra_multiple(dijkstra_algorithm_multiple(matrixOfAdjacency, heightStart - 1),
                                    len(matrixOfAdjacency))
    else:
        print("Неправильні дані!")
elif choice == 2:
    historyMatrix, distanceMatrix = floyd_algorithm(get_data())
    print("Матриця історій: ")
    show_matrix(historyMatrix)
    print("Матриця відстаней: ")
    show_matrix(distanceMatrix)
    choice = input("Бажаєте визначити шлях від довільної до довільної точки(т, н): ")
    if choice != 'н':
        startPoint = int(input("Введіть початкову точку: "))
        endPoint = int(input("Введіть кінцеву точку: "))
        print("Ваш шлях: ")
        show_floyd_path(historyMatrix, startPoint, endPoint)
else:
    print("Неправильний ввід")
