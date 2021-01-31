import random
import queue
import numpy
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


def dfs(dim):
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


arraytp = makemaaze()
tp = dfs(Matrix_dim)
print(tp)
