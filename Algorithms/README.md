# Overview
This repository contains Python scripts that implement various algorithms to solve specific problems. Each script demonstrates algorithmic efficiency and optimization for different scenarios.

## Files and Descriptions
### BoardGames

This script constructs an adjacency matrix to represent roads between intersections, removes "bad" roads, and uses Depth First Search (DFS) to find all possible paths from the start to the end intersection. It efficiently marks and unmarks visited nodes to explore all routes, solving the problem of finding viable paths while excluding specific nodes and edges.
### Drainage

This script finds the longest decreasing path in a matrix using a recursive approach. The isGood function determines valid moves based on neighboring cell values. It addresses the problem of finding the longest path where each step is to a lower-valued neighboring cell.
### MovingBoxes

This script calculates the minimum cost to transport items using companies with single-item and bulk discounts. Using a greedy algorithm and priority queue, it efficiently determines the least expensive way to transport items by considering each company's pricing strategy.
### Scheduling

Implementing the Edmonds-Karp algorithm, this script solves the maximum flow problem in a bipartite graph. It finds augmenting paths using BFS and adjusts edge capacities, ensuring every student can attend all desired classes given class capacity constraints.
### Trading

This script uses a divide-and-conquer algorithm to solve the closest pair of points problem. By combining recursive splitting with strip checking, it efficiently finds the minimum distance between any two points in a plane.
### Wiring

Description: Using Prim's algorithm, this script optimizes the layout of an electrical network to minimize connection costs. It finds the minimum spanning tree for connecting nodes representing electrical components, ensuring optimal connections in complex systems.
### Tasks

Description: This script uses topological sort to determine the order of task execution based on dependencies. It efficiently processes tasks using dictionaries to track dependencies and connections, solving the problem of scheduling tasks given a set of dependencies or indicating if a valid order is impossible.
