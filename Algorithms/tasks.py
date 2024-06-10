number = input()
tasks = ''
i = 0


while number[i] != " ":
        tasks += number[i]
        i += 1
dependencies = number[len(tasks)+1:len(number)]

tasks = int(tasks)
dependencies = int(dependencies)
i = 0
nodeDict = dict()
connectDict = dict()

for i in range(tasks):
    dummy = input()
    nodeDict[dummy] = 0
    connectDict[dummy] = []

for i in range(dependencies):
    x = input()
    l = x.split(" ")
    nodeDict[l[1]] += 1
    connectDict[l[0]].insert(0, l[1])


queue = []
for i in nodeDict:
    if nodeDict[i] == 0:
        queue.append(i)

output = []
count = 0

while len(queue) != 0:
    temp = queue.pop(0)
    for i in connectDict[temp]:
        nodeDict[i] -= 1
        if nodeDict[i] == 0:
            queue.append(i)
    output.append(temp)
    count += 1
output2 = ''
for i in output:
    output2 += ''.join(i) + " "
if count == tasks:
    print(output2)
else:
    print("IMPOSSIBLE")













