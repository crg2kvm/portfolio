from queue import PriorityQueue


def bfs(source, sink, graph, path):
    visited = [0] * len(graph)
    visited[source] = 1
    queue = []
    queue.append(source)
    while len(queue) != 0:
        curr = queue.pop()
        for i in range(len(graph[curr])):
            if visited[i] == 0 and graph[curr][i] > 0:
                visited[i] = 1
                path[i] = curr
                queue.append(i)

    if visited[sink] == 1:
        return True
    return False


def findMinFlow(path, matrix, source, sink):
    min_flow = float("inf")
    while sink != source:
        min_flow = min(min_flow, matrix[path[sink]][sink])
        sink = path[sink]
    return min_flow


def adjustMatrix(matrix, min_flow, path, sink, source):
    while sink != source:
        row = path[sink]
        matrix[row][sink] -= min_flow
        matrix[sink][row] += min_flow
        sink = row
    return matrix


def algo(matrix, source, sink):
    path = [-1] * len(matrix)
    flow = 0
    #print(path)
    while bfs(source, sink, matrix, path):
        #print(path)
        minflow = findMinFlow(path,matrix,source,sink)
        #print( minflow)
        flow += minflow
        matrix = adjustMatrix(matrix,minflow,path,sink,source)
        path = [-1] * len(matrix)
    return flow

r = -1
c = -1
n = -1
splitter = input().split()
r = int(splitter[0])
c = int(splitter[1])
n = int(splitter[2])
while n != 0 or c != 0 or r != 0:
    students = 0
    students_list = {}
    students_names = []
    class_list = []
    for i in range(r):
        temp = input().split()
        if temp[0] not in students_list:
           students_names.append(temp[0])
           students_list[temp[0]] = [temp[1]]
           students += 1
        else:
           students_list[temp[0]].append(temp[1])
        if temp[1] not in class_list:
           class_list.append(temp[1])
    matrix = []
    zero = [0] * (c + students + 2)
    for i in range(c + students + 2):
        matrix.append([])
        matrix[i].extend(zero)
    for i in range(c):
        temp = input().split()
        if temp[0] not in class_list:
            class_list.append(temp[0])
        x = class_list.index(temp[0])
        matrix[x+1+students][len(matrix)-1] = int(temp[1])
    for i in range(students):
        matrix[0][i+1] = n
        for classes in students_list[students_names[i]]:
            x = class_list.index(classes)
            matrix[i+1][x+1+students] = 1

    x = algo(matrix,0,len(matrix)-1)
    if n == 0:
        print("No")
    elif r == 0:
        print("Yes")
    elif x == students * n:
       print("Yes")
    else:
       print("No")
    input()
    splitter = input().split()
    r = int(splitter[0])
    c = int(splitter[1])
    n = int(splitter[2])