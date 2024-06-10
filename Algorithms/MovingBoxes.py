from queue import PriorityQueue
import math
def cost(items, carryon, single, half):
    price = 0
    while items > carryon:
        half_price = half / math.ceil(items/2)
        single_price = single
        if half_price <= single_price and math.ceil(items/2) >= carryon:
            price += half
            items -= math.ceil(items/2)
        else:
            price += single
            items -= 1
        #print(items)
    return price

count = 0
z = int(input())
while count < z:
    pq = PriorityQueue()
    count += 1
    splitter = input().split()
    items = int(splitter[0])
    carryon = int(splitter[1])
    companies = int(splitter[2])
    for i in range(companies):
        splitter = input().split()
        pq.put((cost(items,carryon,int(splitter[1]),int(splitter[2])),splitter[0]))
    print("Case " + str(count))
    for i in range(companies):
        x, y = pq.get()
        print(str(y) + " " + str(x))