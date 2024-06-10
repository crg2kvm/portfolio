import math
import sys
from queue import PriorityQueue


def distance(p1,p2):
    x = pow((p1[0] - p2[0]),2)
    y = pow((p1[1] - p2[1]),2)
    z = pow(x+y, 1/2)
    return z

def bruteForce(points):
    min = float("inf")
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                if distance(points[i], points[j]) <= min:
                    min = distance(points[i],points[j])
    return min

def selectStrip(full, median, delta):
    strip = []
    for i in range(len(full)):
        if abs(full[i][0] - median[0]) <= delta:
            strip.append(full[i])
    return strip



def recurDistance(points):
    if len(points) <= 3:
        return bruteForce(points)
    median = int(len(points)/2)
    left = points[:median]
    right = points[median:]
    leftDist = recurDistance(left)
    rightDist = recurDistance(right)
    full = left + right
    strip = selectStrip(full, points[median], min(leftDist,rightDist))
    strip.sort(key = lambda point : point[1])
    x = stripMath(strip, min(leftDist,rightDist))
    return min(x, leftDist, rightDist)

def stripMath(strip, delta):
    min = delta
    for i in range(len(strip)):
        j = i + 1
        while j < i + 7 and j < len(strip):
            #j = i+1
            min = distance(strip[i],strip[j])
            j += 1
    return min




splitter = input()
splitter = splitter.split()
data = []
while splitter[0] != "0":
    data = []
    for i in range(int(splitter[0])):
        coords = input()
        coords = coords.split()
        temp = (float(coords[0]), float(coords[1]))
        data.append(temp)
    data.sort(key = lambda point : point[0])

    delta = recurDistance(data)
    if delta > 10000:
        delta = "infinity"
    else:
        delta = round(delta, 4)
        delta = "{:.4f}".format(delta)
    print(delta)
    splitter = input()
    splitter = splitter.split()
