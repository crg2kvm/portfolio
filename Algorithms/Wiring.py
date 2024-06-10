from queue import PriorityQueue
import heapq
class node:
    def __init__(self, name, type):
        self.connections = []
        self.type = type
        self.name = name
        self.known = False
        self.parent = None
        self.whichSwitch = None
        self.group = None


class edge:
    def __init__(self,  node, cost):
        self.node = node
        self.cost = cost
        self.type = None

def preSwitch(node):
    if node.type == "breaker" or node.type == "outlet" or node.type == "box":
        return True
    else: return False

def isSwitch(node):
    if node.type == "switch":
        return True
    else: return False

def postSwitch(node):
    if node.type == "light":
        return True
    else: return False

def isConnectable(node1, node2):
    if preSwitch(node1) and preSwitch(node2):
        return True
    elif preSwitch(node1) and isSwitch(node2):
        return True
    elif preSwitch(node2) and isSwitch(node2):
        return True
    elif postSwitch(node1) and postSwitch(node2):
        if node1.whichSwitch == node2.whichSwitch:
            return True
    elif isSwitch(node1) and postSwitch(node2):
        if node1.name == node2.whichSwitch:
            return True
    elif isSwitch(node2) and postSwitch(node1):
        if node2.name == node1.whichSwitch:
            return True
    else:
        return False

def typeConnect(node1, node2):
    if preSwitch(node1) and preSwitch(node2):
        return "pre"
    elif preSwitch(node1) and postSwitch(node2):
        return "nah"
    elif preSwitch(node2) and postSwitch(node1):
        return "nah"
    elif preSwitch(node1) and isSwitch(node2):
        return "border1"
    elif preSwitch(node2) and isSwitch(node1):
        return "border2"
    elif isConnectable(node1, node2):
        return "post"




start = input().split(" ")
num_nodes = int(start[0])
num_connects = int(start[1])
node_list = []
matrix = []
pre = []
pre_name = []
post = []
post_name = []
node_name = []
boundary = []
switch = []
for i in range(num_nodes):
    splitter = input().split(" ")
    new_node = node(splitter[0], splitter[1])
    if splitter[1] == "switch":
        temp = splitter[0]
        post.append(new_node)
        post_name.append(new_node.name)
    elif splitter[1] == "light":
        new_node.whichSwitch = temp
        post.append(new_node)
        post_name.append(new_node.name)
    elif splitter[1] == "breaker":
        pre.insert(0, new_node)
        pre_name.insert(0, new_node.name)
    else:
        pre.append(new_node)
        pre_name.append(new_node.name)
    node_list.append(new_node)
    node_name.append(new_node.name)
breaker = node("preSwitchNode", "breaker")
for i in range(num_connects):
    splitter = input().split(" ")
    node1 = node_list[node_name.index(splitter[0])]
    node2 = node_list[node_name.index(splitter[1])]
    weight = int(splitter[2])
    temp = typeConnect(node1, node2)
    if temp == "pre":
        node1.connections.append(edge(node2, weight))
        node2.connections.append(edge(node1, weight))
    elif temp == "border1":
        node2.connections.append(edge(breaker, weight))
        breaker.connections.append(edge(node2, weight))
    elif temp == "border2":
        node1.connections.append(edge(breaker, weight))
        breaker.connections.append(edge(node1, weight))
    elif temp == "post":
        node1.connections.append(edge(node2, weight))
        node2.connections.append(edge(node1, weight))


def prims(start, part, name_list):

    pq = PriorityQueue()
    #pq2 = PriorityQueue()
    pq.put((0, start.name))
    parents = []
    cost = 0
    while len(parents) < len(part):
        pq2 = PriorityQueue()
        while not pq.empty():
            weight, node = pq.get()
            pq2.put((weight, node))
        pq = pq2
        weight, node = pq.get()
        while node in parents:
            weight, node = pq.get()
        cost += weight
        node = part[name_list.index(node)]
        node.known = True
        parents.append(node.name)
        for neighbor in node.connections:
            edge = neighbor
            #print("error")
            #print(isConnectable(node, edge.node))
            if edge.node.known is False and isConnectable(node, edge.node):
                pq.put((edge.cost, edge.node.name))
    return cost


pre_weight = prims(pre[0], pre, pre_name)
post.insert(0, breaker)
post_name.insert(0, breaker.name)
post_weight = pre_weight + prims(post[0], post, post_name)
print(post_weight)
