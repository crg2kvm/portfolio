from queue import PriorityQueue




def isGood(matrix,row,col):
    curr = matrix[row][col]
    good = []
    if curr < matrix[row-1][col]:
        good.append((row-1,col))
    else:
        good.append((-1,-1))
    if curr < matrix[row+1][col]:
        good.append((row+1,col))
    else:
        good.append((-1,-1))
    if curr < matrix[row][col-1]:
        good.append((row,col-1))
    else:
        good.append((-1,-1))
    if curr < matrix[row][col+1]:
        good.append((row,col+1))
    else:
        good.append((-1,-1))
    return good

def longestPath(matrix,row, col):
    u = 1
    d = 1
    l = 1
    r = 1
    dummy = isGood(matrix,row,col)
    if len(dummy) == 0:
        return 1
    if dummy[0][0] != -1:
        u = 1 + longestPath(matrix, dummy[0][0], dummy[0][1])
    if dummy[1][0] != -1:
        d = 1 + longestPath(matrix, dummy[1][0], dummy[1][1])
    if dummy[2][0] != -1:
        l = 1 + longestPath(matrix, dummy[2][0], dummy[2][1])
    if dummy[3][0] != -1:
        r = 1 + longestPath(matrix, dummy[3][0], dummy[3][1])
    return max(u, d, l, r)


def drainage(n):
    z = 0
    output = []
    while z < n:
        splitter = input().split()
        name = splitter[0]
        rows = int(splitter[1])
        cols = int(splitter[2])

        matrix = []
        matrix.append([-1] * (cols+2))
        for i in range(rows):
            row = input().split()
            temp = []
            temp.append(-1)
            for j in range(len(row)):
                temp.append(int(row[j]))
            temp.append(-1)
            matrix.append(temp)
        matrix.append([-1] * (cols+2))
        pq = PriorityQueue()
        for i in range(rows):
            for j in range(cols):
                pq.put(-longestPath(matrix, i + 1, j + 1))
        output.append((name, -pq.get()))
        z+=1
    return output

x = int(input())
answer = drainage(x)
for i in range(len(answer)):
    print(answer[i][0]+":  ",answer[i][1])