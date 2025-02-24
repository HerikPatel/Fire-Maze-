import heapq
import random
import queue
import numpy
import time
import math
import turtle
from collections import deque

Matrix_dim = int(input("Enter Dimension of the Matrix: "))
probablity = float(input("Enter Probablity: "))
flammability_rate = float(input("Enter flammability rate: "))


class block:
    def __init__(self, position, g, h):
        self.parent = None
        self.position = position
        self.g = g
        self.h = h
        self.fire_distance = 0
        self.f = self.g+self.h - self.fire_distance

    def __lt__(self, other):
        return self.f < other.f


def makemaaze():            # This function uses user input of dimension and probablity and returns a maze in form of matrix

    matrix = []
    # matrix2 = []
    for i in range(Matrix_dim):
        c = []
        # c2 = []
        for j in range(Matrix_dim):
            if i == 0 and j == 0:
                c.append(1)
                # c2.append(1)
            elif i == Matrix_dim-1 and j == Matrix_dim-1:
                c.append(1)
                # c2.append(1)
            elif(random.randint(0, 10) < probablity*10):
                c.append(0)
                # c2.append(0)
            else:
                c.append(1)
                # c2.append(1)
        matrix.append(c)
        # matrix2.append(c2)
    return numpy.array(matrix)  # , numpy.array(matrix2)


# Checks if the dimension of the next move are valid or invalid
def check_dimensions(row, col, dim):
    if row >= 0 and col >= 0:
        if row < dim and col < dim:
            return True
    return False


def dfs(dim, arraytp, i, j, goal_row, goal_col):
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
        if temp_var1 == goal_row and temp_var2 == goal_col:
            # print(counter_step)
            # print(dfs_row.qsize())
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


def check_dup_openlist(current_node, node, open_list):
    for x in open_list:
        if x.position == node.position:
            if x.f > node.f:
                x = node

            return open_list, False
    return open_list, True


def heuristic_1(dim, row, col):
    h = math.sqrt((dim-row)**2+(dim-col)**2)
    return h

# use the latest fire cell added to get ditacne from the fire cell


def heuristic_2(row, col, new_burningcell_list):
    # add fire distance and return value of h which is minimum
    # One problem is that we determine which is lowest f in priority queue so we need to change that and see which element will pop
    # or we can add a dist_fire in block class which would basically be used to determine as a tie breaker between
    # we can pop last three elements to see if the algorithm performs better or not
    # best idea is to make copy of ASTAR AND work on it rather than changing prev a star
    # for idea of where exactly fire is you can take newly added list and take out an average
    row_sum, col_sum, counter = 0, 0, 0
    for i in new_burningcell_list:
        row_sum = row_sum+i[0]
        col_sum = col_sum+i[1]
        counter = counter+1
    if counter != 0:
        row_sum = row_sum/counter
        col_sum = col_sum/counter

    f = math.sqrt((row_sum-row)**2+(col_sum-col)**2)
    return f


# use arguments to determine which heuristic to use


def a_star(maze, row, col, dim, new_burningcell_list, fire_check):
    open_list = []
    close_list = []
    path = []
    start_row = row
    start_col = col
    h = heuristic_1(dim-1, row, col)
    node = block([row, col], 0, h)
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
            while (row != start_row or col != start_col):
                current_node = current_node.parent
                row = current_node.position[0]
                col = current_node.position[1]
                path.append([row, col])

            path.reverse()
            return path
        if check_dimensions(row+1, col, dim) and maze[row+1, col] == 1:
            h = heuristic_1(dim-1, row+1, col)
            node = block([row+1, col], current_node.g+1, h)
            node.parent = current_node
            if fire_check:
                node.fire_distance = heuristic_2(
                    row+1, col, new_burningcell_list)
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row, col+1, dim) and maze[row, col+1] == 1:
            h = heuristic_1(dim-1, row, col+1)
            node = block([row, col+1], current_node.g+1, h)
            node.parent = current_node
            if fire_check:
                node.fire_distance = heuristic_2(
                    row, col+1, new_burningcell_list)
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row, col-1, dim) and maze[row, col-1] == 1:
            h = heuristic_1(dim-1, row, col-1)
            node = block([row, col-1], current_node.g+1, h)
            node.parent = current_node
            if fire_check:
                node.fire_distance = heuristic_2(
                    row, col-1, new_burningcell_list)
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        if check_dimensions(row-1, col, dim) and maze[row-1, col] == 1:
            h = heuristic_1(dim-1, row-1, col)
            node = block([row-1, col], current_node.g+1, h)
            node.parent = current_node
            if fire_check:
                node.fire_distance = heuristic_2(
                    row-1, col, new_burningcell_list)
            open_list, bol = check_dup_openlist(current_node, node, open_list)
            if bol:
                open_list.append(node)

        close_list.append(current_node)
    return path


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


def check_burning_neighbour(row, col, maze, dim):  # 5 represent fire
    burning_block = 0
    if check_dimensions(row, col+1, dim) and maze[row][col+1] == 5:
        burning_block = burning_block+1
    if check_dimensions(row+1, col, dim) and maze[row+1][col] == 5:
        burning_block = burning_block+1
    if check_dimensions(row, col-1, dim) and maze[row][col-1] == 5:
        burning_block = burning_block+1
    if check_dimensions(row-1, col, dim) and maze[row-1][col] == 5:
        burning_block = burning_block+1
    return burning_block


def spread_fire(dim, fire_list, flammability_rate, maze):
    tempfire_list = []
    for x in fire_list:
        row = x[0]
        col = x[1]
        # checking to see if open path which is 1 here
        if check_dimensions(row, col+1, dim) and maze[row][col+1] == 1:
            k = check_burning_neighbour(row, col+1, maze, dim)
            tp = pow((1-flammability_rate), k)
            tp = 1-tp
            if(random.randint(0, 10) <= tp*10):
                maze[row][col+1] = 5
                tempfire_list.append([row, col+1])
        if check_dimensions(row+1, col, dim) and maze[row+1][col] == 1:
            k = check_burning_neighbour(row+1, col, maze, dim)
            tp = pow((1-flammability_rate), k)
            tp = 1-tp
            if(random.randint(0, 10) <= tp*10):
                maze[row+1][col] = 5
                tempfire_list.append([row+1, col])
        if check_dimensions(row, col-1, dim) and maze[row][col-1] == 1:
            k = check_burning_neighbour(row, col-1, maze, dim)
            tp = pow((1-flammability_rate), k)
            tp = 1-tp
            if(random.randint(0, 10) <= tp*10):
                maze[row][col-1] = 5
                tempfire_list.append([row, col-1])
        if check_dimensions(row-1, col, dim) and maze[row-1][col] == 1:
            k = check_burning_neighbour(row-1, col, maze, dim)
            tp = pow((1-flammability_rate), k)
            tp = 1-tp
            if(random.randint(0, 10) <= tp*10):
                maze[row-1][col] = 5
                tempfire_list.append([row-1, col])

    return tempfire_list


def check_if_reachable(maze, start, end, dim):
    if dfs(dim, maze, start[0], start[1], end[0], end[1]) == "Maze solved":
        return False
    else:
        return True


# open path here=0 5 is fire
def fire_strategy1(dim, maze, flammability_rate, path):
    if len(path) <= 0:
        return 0
    fire_list = []
    fire_row = random.randint(1, dim-1)
    fire_col = random.randint(1, dim-1)
    while True:
        maze2 = numpy.copy(maze)
        if (maze[fire_row][fire_col] != 1 or check_if_reachable(maze2, [0, 0], [fire_row, fire_col], dim)):
            fire_row = random.randint(1, dim-1)
            fire_col = random.randint(1, dim-1)
        else:
            break
    maze[fire_row][fire_col] = 5
    fire_list.append([fire_row, fire_col])
    for x in path:
        new_burningcell_list = spread_fire(
            dim, fire_list, flammability_rate, maze)
        fire_list = new_burningcell_list+fire_list
        try:
            fire_list.index(x)
            return 0
        except:
            continue

    # print(maze)
    # print(maze2)
    # print(path)
    # print("list")
    # print(fire_list)
    # print("New")
    return 1

# new update 3.0 the fire starte is not changing while we are caluclating the current path because we will be using startegy 2
# techquine to do it so that fire is kind of paused while we are caluclating the path so heuristic class can be edited to accomodate
# try block at which fire start outside both of the method
# strategy 3 - when meausring heuristic if diffrece is small and or there is no diffrence we choose the block which
# is more far from the fire take origin of fire as distance metric in heuristic or another approach is to
# compare with latest or closest node of fire


def fire_strategy2(dim, maze, flammability_rate):
    fire_list = []
    fire_row = random.randint(1, dim-1)
    fire_col = random.randint(1, dim-1)
    maze2 = numpy.copy(maze)
    start = []
    path = a_star(maze2, 0, 0, dim, [], False)
    while True:
        maze3 = numpy.copy(maze)
        if (maze[fire_row][fire_col] != 1 or check_if_reachable(maze3, [0, 0], [fire_row, fire_col], dim)):
            fire_row = random.randint(1, dim-1)
            fire_col = random.randint(1, dim-1)
        else:
            break
    maze[fire_row][fire_col] = 5
    fire_list.append([fire_row, fire_col])
    while True:
        if len(path) <= 0:
            return 0
        if len(path) == 1:
            return 1
        start = path[1]
        new_burningcell_list = spread_fire(
            dim, fire_list, flammability_rate, maze)
        fire_list = new_burningcell_list+fire_list
        maze2 = numpy.copy(maze)
        path = a_star(maze2, start[0], start[1], dim, [], False)

        try:
            fire_list.index(start)
            return 0
        except:
            continue

    return 1


def fire_strategy3(dim, maze, flammability_rate):
    fire_list = []
    fire_row = random.randint(1, dim-1)
    fire_col = random.randint(1, dim-1)
    maze2 = numpy.copy(maze)
    start = []
    path = a_star(maze2, 0, 0, dim, [], True)
    while True:
        maze3 = numpy.copy(maze)
        if (maze[fire_row][fire_col] != 1 or check_if_reachable(maze3, [0, 0], [fire_row, fire_col], dim)):
            fire_row = random.randint(1, dim-1)
            fire_col = random.randint(1, dim-1)
        else:
            break
    maze[fire_row][fire_col] = 5
    fire_list.append([fire_row, fire_col])
    while True:
        if len(path) <= 0:
            return 0
        if len(path) == 1:
            return 1
        start = path[1]
        new_burningcell_list = spread_fire(
            dim, fire_list, flammability_rate, maze)
        fire_list = new_burningcell_list+fire_list
        maze2 = numpy.copy(maze)
        path = a_star(maze2, start[0], start[1],
                      dim, new_burningcell_list, True)

        try:
            fire_list.index(start)
            return 0
        except:
            continue

    return 1


ctr, ctr1, ctr2, ctr3 = 0, 0, 0, 0
while ctr != 999:
    ctr = ctr+1
    mazefire = makemaaze()
    mazefire2 = numpy.copy(mazefire)
    mazefire3 = numpy.copy(mazefire)
    mazefire4 = numpy.copy(mazefire)

    path = a_star(mazefire, 0, 0, Matrix_dim, [], False)
    if len(path) < 1:
        ctr = ctr-1
        continue

    strt1 = fire_strategy1(Matrix_dim, mazefire2,
                           flammability_rate, path)
    strt2 = fire_strategy2(Matrix_dim, mazefire3,
                           flammability_rate)
    strt3 = fire_strategy3(Matrix_dim, mazefire4,
                           flammability_rate)

    if strt1 == 1:
        ctr1 = ctr1+1
    if strt2 == 1:
        ctr2 = ctr2+1
    if strt3 == 1:
        ctr3 = ctr3+1


print("strategy 1")
print(ctr1/1000)
print("strategy 2")
print(ctr2/1000)
print("strategy 3")
print(ctr3/1000)
# turtle.mainloop()
