import heapq as hq
import numpy as np
import math

def dist(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def findNeighbours(point, m):
    neighbours = []
    for x in [-1, 0 ,1]:
        for y in [-1, 0, 1]:
            if (x,y) != (0, 0):
                neighbour = (point[0] + x, point[1] + y)
                if (neighbour[0] >= 0 and neighbour[0] < m.width
                and neighbour[1] >= 0 and neighbour[1] < m.height):
                    if m.get(neighbour[0], neighbour[1]) == 1:
                        neighbours.append(neighbour)
    return neighbours

def reconstructPath(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path

def astar(start, goal, m, mode):

    openSet = []
    visited = set()
    cameFrom = {}

    gScore = np.full((m.width, m.height), np.inf)
    gScore[start] = 0
    fScore = np.full((m.width, m.height), np.inf)
    fScore[start] = dist(start, goal)
    hq.heappush(openSet, (fScore, start))

    while len(openSet) > 0:
        _, current = hq.heappop(openSet)
        # print(m)

        if current == goal:
            print('Finished!')
            path = reconstructPath(cameFrom, current)
            return path

        neighbours = findNeighbours(current, m)

        for neighbour in neighbours:
            tentative_gScore = gScore[current] + dist(current, neighbour)
            if tentative_gScore < gScore[neighbour]:
                cameFrom[neighbour] = current

                gScore[neighbour] = tentative_gScore
                # print(gScore[neighbour])

                if mode == 'astar':
                    fScore[neighbour] = gScore[neighbour]  + dist(neighbour, goal)
                elif mode =='dijkstra':
                    fScore[neighbour] = gScore[neighbour]

                if neighbour not in m.special:
                    m.special[neighbour] = '_'
                if neighbour not in visited:
                    visited.add(neighbour)
                    hq.heappush(openSet, (fScore[neighbour], neighbour))

    # in case point is unreachable
    return None
