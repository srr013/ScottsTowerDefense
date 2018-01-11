import Queue


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = Queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def get_path(map, start, goal):
    came_from, cost_so_far = a_star_search(map, start, goal)
    goal = goal
    #draw_grid(map, width=3, point_to=came_from, start=start, goal=goal)
    #draw_grid(map, width=1, number=cost_so_far, start=start, goal=goal)
    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            return "Path Blocked"
    path.append(start) # optional
    path.reverse() # optional
    return path


class MapGrid():
    def __init__(self, width, height, border):
        self.width = width - (border*2)
        self.height = height - (border*2)
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)] #, (x + 1,y + 1), (x + 1, y - 1), (x - 1,y - 1), (x - 1, y + 1)
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

class GridWithWeights(MapGrid):
    def __init__(self, width, height, border):
        MapGrid.__init__(self,width, height, border)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = ">"
        if x2 == x1 - 1: r = "<"
        if y2 == y1 + 1: r = "v"
        if y2 == y1 - 1: r = "^"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r

def draw_grid(graph, width=1, **style):
    for y in range(graph.height):
        xlist = list()
        for x in range(graph.width):
            xlist.append("%%-%ds" % width % draw_tile(graph, (x, y), style, width))
        print xlist
