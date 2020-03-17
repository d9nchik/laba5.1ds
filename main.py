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
            temp = (line[:len(line)] + line[len(line) + 1:]).split()
            for x in range(len(temp)):
                temp[x] = int(temp[x])
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


def dijkstra_algorithm(adjacency_matrix, height):
    matrix_of_unvisited = copy.deepcopy(adjacency_matrix)
    visited = []
    unvisited = [Heights(height, 0, None)]
    while len(unvisited) > 0:
        position_of_minimum = find_minimum_weight(unvisited)
        visited.append(unvisited[position_of_minimum])
        close_height(matrix_of_unvisited, visited[-1].position)
        del unvisited[position_of_minimum]
        neighbours = find_neighbours(matrix_of_unvisited, visited[-1].position)
        for x in neighbours:
            position_of_neighbour = position_in_array(unvisited, x)
            if position_of_neighbour == -1:
                unvisited.append(
                    Heights(x, matrix_of_unvisited[visited[-1].position][x] + visited[-1].weight, visited[-1].position))
            elif unvisited[position_of_neighbour].weight > matrix_of_unvisited[visited[-1].position][
                x] + visited[-1].weight:
                unvisited[position_of_neighbour].weight = matrix_of_unvisited[visited[-1].position][
                                                              x] + visited[-1].weight
                unvisited[position_of_neighbour].father = visited[-1].position
    return visited


def show_path(dijkstra_data, size):
    for x in range(size):
        path = [Heights(None, None, x)]
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
        close_height(matrix_of_unvisited, visited[-1].position)
        del unvisited[position_of_minimum]
        neighbours = find_neighbours(matrix_of_unvisited, visited[-1].position)
        for x in neighbours:
            position_of_neighbour = position_in_array(unvisited, x)
            if position_of_neighbour == -1:
                unvisited.append(
                    Heights(x, matrix_of_unvisited[visited[-1].position][x] + visited[-1].weight, visited[-1].position))
            elif unvisited[position_of_neighbour].weight > matrix_of_unvisited[visited[-1].position][
                x] + visited[-1].weight:
                unvisited[position_of_neighbour].weight = matrix_of_unvisited[visited[-1].position][
                                                              x] + visited[-1].weight
                unvisited[position_of_neighbour].father = visited[-1].position
    return visited


def show_path_dijkstra_single(dijkstra_data):
    path = [Heights(None, None, dijkstra_data[-1].position)]
    for y in range(len(dijkstra_data) - 1, 0, -1):
        if path[-1].father == dijkstra_data[y].position:
            path.append(dijkstra_data[y])
    del path[0]
    if len(path) != 0:
        path.reverse()
        for z in range(0, len(path)):
            print(path[z].father + 1, end=" - > ")
        print("%s Шлях = %s" % (path[-1].position + 1, path[-1].weight))


matrix_of_adjacency = create_adjacency_matrix(get_data())

print(
    "Визначити найкоротший маршрут між двома вершинами та його довжину(1) чи Визначити найкоротшу відстань від "
    "заданої вершини до всіх інших вершин(2)")
choice = int(input("Варіант: "))
if choice == 1:
    heightStart = int(input("Введіть вершину початку: "))-1
    heightFinish = int(input("Введіть вершину кінця: "))-1
    show_path_dijkstra_single(dijkstra_algorithm_single(matrix_of_adjacency, heightStart, heightFinish))
elif choice == 2:
    heightStart = int(input("Введіть вершину початку: "))
    show_path(dijkstra_algorithm(matrix_of_adjacency, heightStart - 1), len(matrix_of_adjacency))
else:
    print("Неправильні дані!")
