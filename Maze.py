import random
import queue
import numpy
import time
import math
from collections import deque

Matrix_dim = int(input("Enter Dimension of the Matrix: "))
probablity = float(input("Enter Probablity: "))


def makemaaze():            # This function uses user input of dimension and probablity and returns a maze in form of matrix

    matrix = []
    matrix2 = []
    for i in range(Matrix_dim):
        c = []
        c2 = []
        for j in range(Matrix_dim):
            if i == 0 and j == 0:
                c.append(0)
                c2.append(1)
            elif i == Matrix_dim-1 and j == Matrix_dim-1:
                c.append(0)
                c2.append(1)
            elif(random.randint(0, 10) < probablity*10):
                c.append(1)
                c2.append(0)
            else:
                c.append(0)
                c2.append(1)
        matrix.append(c)
        matrix2.append(c2)
    return numpy.array(matrix), numpy.array(matrix2)


# Checks if the dimension of the next move are valid or invalid
def check_dimensions(row, col, dim):
    if row >= 0 and col >= 0:
        if row < dim and col < dim:
            return True
    return False


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
            # print(counter_step)
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


def bfs(maze, start, second):
    fringe = deque()  # queue for BFS
    first = [start[0], start[1]]
    fringe.append(first)
    visited = []
    parentTracker = []
    for i in range(len(maze)):
        for j in range(len(maze)):
            toAdd = {}
            toAdd["previous"] = []
            parentTracker.append(toAdd)

    parentTracker[0]["previous"] = start
    # process thru fringe
    while fringe:
        current = fringe.popleft()  # pop leftmost = oldest one gets popped
        if current[0] == second[0] and current[1] == second[1]:
            path = []
            path.append([current[0], current[1]])
            curIndex = findIndex(current[0], current[1], len(maze))
            backtrackCurrent = parentTracker[curIndex]["previous"]
            while True:
                path.insert(0, backtrackCurrent)
                if backtrackCurrent == first:
                    break
                backtrackCurrent = parentTracker[findIndex(backtrackCurrent[0], backtrackCurrent[1], len(maze))][
                    "previous"]

            return path

        else:
            if current not in visited:  # check node, if not already visited then work thru its children if they're valid
                currentFirst = current[0]
                currentSecond = current[1]
                if currentFirst - 1 >= 0 and currentFirst - 1 < len(
                        maze) and currentSecond >= 0 and currentSecond < len(maze):  # up
                    if maze[currentFirst - 1][currentSecond] == 0:
                        temp = []
                        temp.append(currentFirst - 1)
                        temp.append(currentSecond)
                        fringe.append(temp)
                        parentTracker[findIndex(currentFirst - 1, currentSecond, len(maze))]["previous"] = [
                            currentFirst, currentSecond]
                if currentFirst >= 0 and currentFirst < len(
                        maze) and currentSecond - 1 >= 0 and currentSecond - 1 < len(maze):  # left
                    if maze[currentFirst][currentSecond - 1] == 0:
                        temp = []
                        temp.append(currentFirst)
                        temp.append(currentSecond - 1)
                        fringe.append(temp)
                        parentTracker[findIndex(currentFirst, currentSecond - 1, len(maze))]["previous"] = [
                            currentFirst, currentSecond]
                if currentFirst + 1 >= 0 and currentFirst + 1 < len(
                        maze) and currentSecond >= 0 and currentSecond < len(maze):  # down
                    if maze[currentFirst + 1][currentSecond] == 0:
                        temp = []
                        temp.append(currentFirst + 1)
                        temp.append(currentSecond)
                        fringe.append(temp)
                        parentTracker[findIndex(currentFirst + 1, currentSecond, len(maze))]["previous"] = [
                            currentFirst, currentSecond]
                if currentFirst >= 0 and currentFirst < len(
                        maze) and currentSecond + 1 >= 0 and currentSecond + 1 < len(maze):  # right
                    if maze[currentFirst][currentSecond + 1] == 0:
                        temp = []
                        temp.append(currentFirst)
                        temp.append(currentSecond + 1)
                        fringe.append(temp)
                        parentTracker[findIndex(currentFirst, currentSecond + 1, len(maze))]["previous"] = [
                            currentFirst, currentSecond]
                # after done, add node to visited
                visited.append([currentFirst, currentSecond])
                maze[currentFirst][currentSecond] = 3

    return ["No path"]


def findIndex(row, column, dim):
    return row * dim + column


ctr2 = 0
while False:
    if ctr2 == 99:
        break
    ctr2 = ctr2+1
    mazedfs = makemaaze()
    maze2 = mazedfs
    print("Maze made")
    start = time.time()
    #str2 = dfs(Matrix_dim, mazedfs, 0, 0)
    str = A_star(Matrix_dim, maze2, 0, 0)
    print("A*-"+str)
    # print("dfs-"+str2)
   # str = dfs(Matrix_dim, mazedfs, 0, 0)
    end = time.time()
    # print(end-start)

while True:
    mazedbfs, mazedfs = makemaaze()
    start = time.time()
    str3 = bfs(mazedbfs, [0, 0], [Matrix_dim-1, Matrix_dim-1])
    end = time.time()
    print(len(str3))
    print(end-start)
    print("end")
