import heapq
import math
import numpy
import queue

import random
Matrix_dim = int(input("Enter Dimension of the Matrix: "))
probablity = float(input("Enter Probablity: "))

dfs_row = queue.LifoQueue()
dfs_column = queue.LifoQueue()


class block:
    def __init__(self, position, g, h):
        self.parent = None
        self.position = position
        self.g = g
        self.h = h
        self.f = self.g+self.h

    def __lt__(self, other):
        return self.f < other.f


def dfs(dim, arraytp):
    i, j = 0, 0
    wall_counter = 0
    dfs_column.put(0)
    counter_step = 0
    dfs_row.put(0)
    arraytp[0, 0] = 3
    # if arraytp[0, 1] == 1:  # initialize the priority queue by storing values of of rows and column no blocked by wall
    #    dfs_row.put(0)
    #    dfs_column.put(1)
    # if arraytp[1, 0] == 1:
    #    dfs_row.put(1)
    #    dfs_column.put(0)
    # we only go back to prev node when e find that 3 sides are locked
    while not dfs_row.empty():  # we need a check to see if last coordinate int the queue to see that we donot go back to the same path
        counter_step = counter_step+1
        if wall_counter == 4:
            arraytp[dfs_row.get(), dfs_column.get()] = 0
            if(dfs_column.qsize() == 0):
                continue
            temp_row = dfs_row.get()
            temp_col = dfs_column.get()
            i = temp_row
            j = temp_col
            dfs_row.put(i)
            dfs_column.put(j)
        wall_counter = 0
        # needs to complete the stack error where the queue is not getting empty and problems in last index
        # needed modification nned to see prev state visited to avoid infinite loop check in the if condiotion before transition if the prev state is not the same as current state
        temp_var2 = dfs_column.get()
        temp_var1 = dfs_row.get()
        # i = temp_var1
        # j = temp_var2
        if temp_var1 == dim-1 and temp_var2 == dim-1:
            print(dfs_row.qsize())
            return "Yes! Successful"
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

    return "path not found"


def check_dimensions(row, col, dim):
    if row >= 0 and col >= 0:
        if row < dim and col < dim:
            return True
    return False


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
            open_list.append(node)

        if check_dimensions(row, col+1, dim) and maze[row, col+1] == 1:
            h = math.sqrt(
                (dim-1 - row)**2+(dim-1-col+1)**2)
            node = block([row, col+1], current_node.g+1, h)
            node.parent = current_node
            open_list.append(node)

        if check_dimensions(row, col-1, dim) and maze[row, col-1] == 1:
            h = math.sqrt(
                (dim-1 - row)**2+(dim-1-col-1)**2)
            node = block([row, col-1], current_node.g+1, h)
            node.parent = current_node
            open_list.append(node)

        if check_dimensions(row-1, col, dim) and maze[row-1, col] == 1:
            h = math.sqrt(
                (dim-1 - row-1)**2+(dim-1-col)**2)
            node = block([row-1, col], current_node.g+1, h)
            node.parent = current_node
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
   #str = dfs(Matrix_dim, maze2)
    print(maze)
    print(len(a_star(maze, 0, 0, Matrix_dim))+1)


'''
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
