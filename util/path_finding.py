import math

#using bfs to find the shortest path between two points
def find_path(start, end, map_arr):
    seen = set()
    prev = {}
    q = [[start.x // 32, start.y // 32]]
    end = [end.x // 32, end.y // 32]
    path = []

    while len(q):
        curr = q.pop(0)
        seen.add(tuple(curr))
        if curr == end:
            while tuple(curr) in prev:
                path.append(curr)
                curr = prev[tuple(curr)]
            path.reverse()
            return path
        neighbours = get_neighbours(curr, map_arr)
        for neighbour in neighbours:
            if tuple(neighbour) not in seen:
                q.append(neighbour)
                prev[tuple(neighbour)] = curr


def all_neighbours_seen(neighbours, seen):
    for neighbour in neighbours:
        if neighbour not in seen:
            return False
    return True


def get_neighbours(curr, map_arr):
    neighbours = []
    x = curr[0]
    y = curr[1]

    if x - 1 >= 0:
        neighbours.append([x - 1, y])
    if x + 1 < len(map_arr):
        neighbours.append([x + 1, y])
    if y - 1 >= 0:
        neighbours.append([x, y - 1])
    if y + 1 < len(map_arr[0]):
        neighbours.append([x, y + 1])

    return neighbours

def get_distance(start: tuple, end: tuple):
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)

