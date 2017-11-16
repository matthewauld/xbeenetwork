import collections
from queue import PriorityQueue


def find_path(grid,start,end):
    search = Queue()
    search.put(start)
    came_from = {}
    came_from[start]= None
    found_end = False
    while not search.empty():
        current = search.get()
        if current == end:
            found_end = True
            break
        neighbors = grid.get_neighbors(current)
        for next_value in neighbors:
            if next_value not in came_from:
                came_from[next_value]= current
                search.put(next_value)
    if found_end == True:
        results = []
        results.append(end)
        while start not in results:
            results.append(came_from[results[-1]])
        return results
    else:
        return None


def a_star(graph, start, end):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()[1]

        if current == end:
            break
        for next in graph.get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                frontier.put((priority, next))
                came_from[next] = current

    results = []
    results.append(end)
    while start not in results:
        results.append(came_from[results[-1]])
    return results




def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


class Queue(object):
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()
