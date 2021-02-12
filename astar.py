import heapq
import math
import numpy
import queue
import time
import random
Matrix_dim = int(input("Enter Dimension of the Matrix: "))
probablity = float(input("Enter Probablity: "))

dfs_row = queue.LifoQueue()
dfs_column = queue.LifoQueue()


def dfs(dim, arraytp, i, j):
    dfs_row = queue.LifoQueue()  # This is to store row in the queue
    dfs_column = queue.LifoQueue()  # This is to store Column in the queue
    counter_step = 0
    wall_counter = 0
    dfs_column.put(j)
    dfs_row.put(i)
    arraytp[i, j] = 3
    while not dfs_row.empty():  # The loop will run till there are elements in queue, empty queue suggest no possible solution of maze
        counter_step = counter_step+1
        if wall_counter == 4:  # Value 4 means we have exhasuted all possible unexplored paths for particular cell and we remove this cell from the queue
            arraytp[dfs_row.get(), dfs_column.get()] = 0
            if(dfs_column.qsize() == 0):
                continue
            temp_row = dfs_row.get()
            temp_col = dfs_column.get()
            i, j = temp_row, temp_col
            dfs_row.put(i)
            dfs_column.put(j)
        wall_counter = 0
        temp_var2 = dfs_column.get()
        temp_var1 = dfs_row.get()
        if temp_var1 == dim-1 and temp_var2 == dim-1:
            print(dfs_row.qsize())
            return "Maze solved"
        else:
            dfs_row.put(temp_var1)
            dfs_column.put(temp_var2)

        if check_dimensions(i+1, j, dim) and arraytp[i+1, j] == 1:
            dfs_row.put(i+1)
            dfs_column.put(j)
            arraytp[i+1, j] = 3
            i = i+1
            continue

        else:
            wall_counter = wall_counter+1

        if check_dimensions(i, j+1, dim) and arraytp[i, j+1] == 1:
            dfs_row.put(i)
            dfs_column.put(j+1)
            arraytp[i, j+1] = 3
            j = j+1
            continue

        else:
            wall_counter = wall_counter+1

        if check_dimensions(i, j-1, dim) and arraytp[i, j-1] == 1:
            dfs_row.put(i)
            dfs_column.put(j-1)
            arraytp[i, j-1] = 3
            j = j-1
            continue
        else:
            wall_counter = wall_counter+1

        if check_dimensions(i-1, j, dim) and arraytp[i-1, j] == 1:
            dfs_row.put(i-1)
            dfs_column.put(j)
            arraytp[i-1, j] = 3
            i = i-1
            continue
        else:
            wall_counter = wall_counter+1
    # print(counter_step)
    return "path not found"


class block:
    def __init__(self, position, g, h):
        self.parent = None
        self.position = position
        self.g = g
        self.h = h
        self.f = self.g+self.h

    def __lt__(self, other):
        return self.f < other.f


def check_dimensions(row, col, dim):
    if row >= 0 and col >= 0:
        if row < dim and col < dim:
            return True
    return False


def check_dup_openlist(current_node, node, open_list):
    for x in open_list:
        if x.position == node.position:
            if x.f > node.f:
                x = node

            return open_list, False
    return open_list, True


def a_star(maze, row, col, dim):
    open_list = []
    close_list = []
    path = []
    h = math.sqrt((dim-1)**2+(dim-1)**2)
    node = block([0, 0], 0, h)
    open_list.append(node)
    heapq.heapify(open_list)
    while len(open_list) > 0:
        heapq.heapify(open_list)
        current_node = heapq.heappop(open_list)
        row = current_node.position[0]
        col = current_node.position[1]
        maze[row][col] = 3
        # print(row, col)
        if row == dim-1 and col == dim-1:
            row = current_node.position[0]
            col = current_node.position[1]
            path.append([row, col])
            while (row != 0 and col != 0):
                current_node = current_node.parent
                row = current_node.position[0]
                col = current_node.position[1]
                path.append([row, col])

            return path
        if check_dimensions(row+1, col, dim) and maze[row+1, col] == 1:
            h = math.sqrt(
                (dim-1 - row+1)**2+(dim-1-col)**2)
            node = block([row+1, col], current_node.g+1, h)
            node.parent = current_node
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row, col+1, dim) and maze[row, col+1] == 1:
            h = math.sqrt(
                (dim-1 - row)**2+(dim-1-col+1)**2)
            node = block([row, col+1], current_node.g+1, h)
            node.parent = current_node
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row, col-1, dim) and maze[row, col-1] == 1:
            h = math.sqrt(
                (dim-1 - row)**2+(dim-1-col-1)**2)
            node = block([row, col-1], current_node.g+1, h)
            node.parent = current_node
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row-1, col, dim) and maze[row-1, col] == 1:
            h = math.sqrt(
                (dim-1 - row-1)**2+(dim-1-col)**2)
            node = block([row-1, col], current_node.g+1, h)
            node.parent = current_node
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        close_list.append(current_node)
    return path


def makemaaze():

    matrix = []
    temp_ctr = 0
    for i in range(Matrix_dim):
        c = []
        for j in range(Matrix_dim):
            if i == 0 and j == 0:
                c.append(1)
            elif i == Matrix_dim-1 and j == Matrix_dim-1:
                c.append(1)
            elif(random.randint(0, 10) < probablity*10):
                temp_ctr = temp_ctr+1  # remove this
                c.append(0)
            else:
                c.append(1)
        matrix.append(c)
    return numpy.array(matrix)


while True:
    maze = makemaaze()
    maze2 = numpy.copy(maze)
    print("Dfs")
    str = dfs(Matrix_dim, maze2, 0, 0)
   # print(maze)
    print("A Star")
    start = time.time()
    print(maze)
    print(len(a_star(maze, 0, 0, Matrix_dim))+1)
    end = time.time()

'''


maze2 = numpy.array(maze)
print(len(a_star(maze2, 0, 0, 20))+1)

tp = block([3, 2], 13, 2)

path = []
path.append(tp)
tp = block([31, 22], 4, 2)
path.append(tp)
heapq.heapify(path)
tpp = heapq.heappop(path)
print(tpp.g)
print(tpp.h)
'''
''' Backup Astar
def Euclidean_distance(i, j, dim):
    distance = math.sqrt((dim-1 - i)**2+(dim-1-j)**2)
    return distance


def Heuristic(i, j, dim, arraytp, current_cost):
    row, col = -1, -1
    prev_cost = current_cost.get()
    current_cost.put(prev_cost)
    current_distance, distance = 0.0, 0.0
    if check_dimensions(i, j+1, dim) and arraytp[i, j+1] == 1:
        distance = Euclidean_distance(i, j+1, dim)
        distance = distance+prev_cost+1
        if current_distance == 0.0:
            current_distance = distance
            row, col = i, j+1

        elif current_distance > distance:
            current_distance = distance
            row, col = i, j+1

    if check_dimensions(i+1, j, dim) and arraytp[i+1, j] == 1:
        distance = Euclidean_distance(i+1, j, dim)
        distance = distance+prev_cost+1
        if current_distance == 0.0:
            current_distance = distance
            row, col = i+1, j

        elif current_distance > distance:
            current_distance = distance
            row, col = i+1, j

    if check_dimensions(i, j-1, dim) and arraytp[i, j-1] == 1:
        distance = Euclidean_distance(i, j-1, dim)
        distance = distance+prev_cost+1
        if current_distance == 0.0:
            current_distance = distance
            row, col = i, j-1

        elif current_distance > distance:
            current_distance = distance
            row, col = i, j-1

    if check_dimensions(i-1, j, dim) and arraytp[i-1, j] == 1:
        distance = Euclidean_distance(i-1, j, dim)
        distance = distance+prev_cost+1
        if current_distance == 0.0:
            current_distance = distance
            row, col = i-1, j

        elif current_distance > distance:
            current_distance = distance
            row, col = i-1, j

    return row, col


def A_star(dim, arraytp, i, j):  # arraytp is the mzae
    nodes_visited = 0
    current_cost = queue.LifoQueue()
    current_cost.put(0)
    A_row, A_column = queue.LifoQueue(), queue.LifoQueue()
    A_column.put(j)
    A_row.put(i)
    arraytp[i, j] = 3
    while not A_row.empty():  # The loop will run till there are elements in queue, empty queue suggest no possible solution of maze
        i, j = Heuristic(i, j, dim, arraytp, current_cost)
        if i == -1:  # pop the element from the queue no viable path
            arraytp[A_row.get(), A_column.get()] = 0
            if(A_row.qsize() == 0):
                continue
            temp_row = A_row.get()
            temp_col = A_column.get()
            current_cost.get()
            i, j = temp_row, temp_col
            A_row.put(i)
            A_column.put(j)
            # current_cost.put(temp_cost)
        else:
            temp_cost = current_cost.get()
            current_cost.put(temp_cost)
            current_cost.put(temp_cost+1)
            A_row.put(i)
            A_column.put(j)
            arraytp[i, j] = 3
            nodes_visited = nodes_visited+1

        temp_var1 = A_row.get()
        temp_var2 = A_column.get()
        if temp_var1 == dim-1 and temp_var2 == dim-1:
            print(nodes_visited)
            return "Maze solved"
        else:
            A_row.put(temp_var1)
            A_column.put(temp_var2)

    return "path not found"
'''
