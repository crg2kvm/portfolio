intersections = int(input())
roads = int(input())
matrix = intersections * []
zero = intersections * [0]
for i in range(intersections):
    matrix.append([])
    matrix[i].extend(zero)

for i in range(roads):
    temp = input()
    temp = temp.split(" ")
    origin = int(temp[0])
    dest = int(temp[1])
    matrix[origin][dest] = 1
    matrix[dest][origin] = 1

bad = int(input())
for i in range(bad):
    temp = int(input())
    for j in range(intersections):
        matrix[temp][j] = 0
        matrix[j][temp] = 0


visited = [False] * intersections
output = []
dummy = ""


def dfs(current, visit, graph, path):
    visit[current] = True
    path += str(current)
    if current == len(graph)-1:
        output.append(path)
    path += "-"
    for itr in range(graph.__len__()):
        if graph[current][itr] == 1 and not visit[itr]:
            dfs(itr, visit, graph, path)
    visit[current] = False


dfs(0, visited, matrix, dummy)

for i in range(len(output)):
    print(output[i])