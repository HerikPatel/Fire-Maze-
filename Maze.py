import random
import queue
import numpy
import time
import math
dfs_row = queue.LifoQueue()  # This is to store row in the queue
dfs_column = queue.LifoQueue()  # This is to store Column in the queue

Matrix_dim = int(input("Enter Dimension of the Matrix: "))
probablity = float(input("Enter Probablity: "))


def makemaaze():            # This function uses user input of dimension and probablity and returns a maze in form of matrix

    matrix = []
    for i in range(Matrix_dim):
        c = []
        for j in range(Matrix_dim):
            if i == 0 and j == 0:
                c.append(1)
            elif i == Matrix_dim-1 and j == Matrix_dim-1:
                c.append(1)
            elif(random.randint(0, 10) < probablity*10):
                c.append(0)
            else:
                c.append(1)
        matrix.append(c)
    return numpy.array(matrix)


# Checks if the dimension of the next move are valid or invalid
def check_dimensions(row, col, dim):
    if row >= 0 and col >= 0:
        if row < dim and col < dim:
            return True
    return False


def dfs(dim, arraytp):
    i = 0
    j = 0
    wall_counter = 0
    dfs_column.put(0)
    dfs_row.put(0)
    arraytp[0, 0] = 3
    while not dfs_row.empty():  # The loop will run till there are elements in queue, empty queue suggest no possible solution of maze
        if wall_counter == 4:  # Value 4 means we have exhasuted all possible unexplored paths for particular cell and we remove this cell from the queue
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
        temp_var2 = dfs_column.get()
        temp_var1 = dfs_row.get()
        if temp_var1 == dim-1 and temp_var2 == dim-1:
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

    return "path not found"


def Euclidean_distance(i, j, dim):
    distance = math.sqrt((dim-1 - i)**2+(dim-1-j)**2)
    return distance


def Heuristic(i, j, dim, arraytp):
    row, col = -1, -1
    current_distance, distance = 0.0, 0.0
    if check_dimensions(i, j+1, dim) and arraytp[i, j+1] == 1:
        distance = Euclidean_distance(i, j+1, dim)
        if current_distance == 0.0:
            current_distance = distance
            row = i
            col = j+1

        elif current_distance > distance:
            current_distance = distance
            row = i
            col = j+1
    if check_dimensions(i+1, j, dim) and arraytp[i+1, j] == 1:
        distance = Euclidean_distance(i+1, j, dim)
        if current_distance == 0.0:
            current_distance = distance
            row = i+1
            col = j

        elif current_distance > distance:
            current_distance = distance
            row = i+1
            col = j
    if check_dimensions(i, j-1, dim) and arraytp[i, j-1] == 1:
        distance = Euclidean_distance(i, j-1, dim)
        if current_distance == 0.0:
            current_distance = distance
            row = i
            col = j-1

        elif current_distance > distance:
            current_distance = distance
            row = i
            col = j-1
    if check_dimensions(i-1, j, dim) and arraytp[i-1, j] == 1:
        distance = Euclidean_distance(i-1, j, dim)
        if current_distance == 0.0:
            current_distance = distance
            row = i-1
            col = j

        elif current_distance > distance:
            current_distance = distance
            row = i-1
            col = j

    return row, col


def A_star(dim, arraytp):
    A_row = queue.LifoQueue()
    A_column = queue.LifoQueue()
    i, j = 0, 0
    A_column.put(0)
    A_row.put(0)
    arraytp[0, 0] = 3
    while not A_row.empty():  # The loop will run till there are elements in queue, empty queue suggest no possible solution of maze
        i, j = Heuristic(i, j, dim, arraytp)
        if i == -1:  # pop the element from the queue no viable path
            arraytp[A_row.get(), A_column.get()] = 0
            if(A_row.qsize() == 0):
                continue
            temp_row = A_row.get()
            temp_col = A_column.get()
            i = temp_row
            j = temp_col
            A_row.put(i)
            A_column.put(j)
        else:
            A_row.put(i)
            A_column.put(j)
            arraytp[i, j] = 3

        temp_var1 = A_row.get()
        temp_var2 = A_column.get()
        if temp_var1 == dim-1 and temp_var2 == dim-1:
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
            toReturn = []
            toReturn.append([current[0], current[1]])
            curIndex = findIndex(current[0], current[1], len(maze))
            backtrackCurrent = parentTracker[curIndex]["previous"]
            while True:
                toReturn.insert(0, backtrackCurrent)
                if backtrackCurrent == first:
                    break
                backtrackCurrent = parentTracker[findIndex(backtrackCurrent[0], backtrackCurrent[1], len(maze))][
                    "previous"]

            return toReturn

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


start, end = 0.0, 0.0
while True:
    mazedfs = makemaaze()
    print("Maze made")
    start = time.time()
    str = A_star(Matrix_dim, mazedfs)
    print(str)
    end = time.time()
    print(end-start)


'''

maze_dfs = makemaaze()
print("Maze made")
start = time.time()
tp = dfs(Matrix_dim, maze_dfs)
end = time.time()

print(end-start)
print(tp)
'''
