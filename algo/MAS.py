from random import random, randint, shuffle
from math import sqrt, sin, cos
import json
import sys
from collections import defaultdict



NUMBER_ACTIVE_CARS = int(3271000 * 0.235 * 0.3)

STATIONS = None
VERTEXES = None
GRAPH = None
CARS = None
VERTEX_DICT = dict()

class Vertex:
    def __init__(self, id, is_station, location):
        self.id = id
        self.is_station = is_station
        self.location = location
        self.sold_gasoline = 0
        self.number_visited = 0
        self.number_stopped = 0
        self.number_cars = 0


    def get_id(self):
        return self.id


    def get_is_station(self):
        return self.is_station


    def get_location(self):
        return self.location


class Car:
    def __init__(self, capacity, spending, vertex, velocity_coeff):
        self.capacity = capacity
        self.current_capacity = capacity * max(0.2, random())
        self.spending = spending
        self.vertex = vertex
        self.velocity_coeff = velocity_coeff
        self.local_time = 0
        self.time_attend = 0
        self.active = False


    def get_vertex(self):
        return self.vertex


    def get_capacity(self):
        return self.capacity


    def get_spending(self):
        return self.spending


    def get_velocity_coeff(self):
        return self.velocity_coeff


    def _possibility_refuel(self, percentage_fuel):
        return (1 - (1 - percentage_fuel) ** 4)


    def next_direction(self, neighbours):
        if not self.active:
            if random() > 0.99:
                self.active = True
                if self.current_capacity < self.capacity * 0.2:
                    self.current_capacity = self.capacity * min(random(), 0.3)
        if not self.active:
            pass
        if self.time_attend <= self.local_time:
            non_stations = []
            for neighbour in neighbours:
                if neighbour.is_station:
                    dist = sqrt((self.vertex.location[0] - neighbour.location[0]) ** 2
                                + (self.vertex.location[1] - neighbour.location[1]) ** 2)
                    if self.current_capacity > self.spending * dist:
                        p_refuel = self._possibility_refuel(float(self.current_capacity) / float(self.capacity))
                        if random() < p_refuel:
                            self.time_attend = dist * self.velocity_coeff + randint(1, 5) * randint(1, 5) * randint(0, 5)
                            self.vertex.number_cars -= 1
                            neighbour.number_cars += 1
                            neighbour.sold_gasoline += (self.capacity - self.current_capacity)
                            self.current_capacity = self.capacity
                            self.vertex = neighbour
                            self.vertex.number_visited += 1
                            self.vertex.number_stopped += 1
                            if random() > 0.4:
                                self.active = False
                else:
                    non_stations.append(neighbour)
            non_stations = neighbours
            if len(non_stations) == 0:
                self.active = False
            shuffle(non_stations)
            good_pos = 0
            for neighbour in non_stations:
                dist = sqrt((self.vertex.location[0] - neighbour.location[0]) ** 2
                                + (self.vertex.location[1] - neighbour.location[1]) ** 2)
                if self.current_capacity > self.spending * dist:
                    self.current_capacity -= self.spending * dist
                    self.vertex.number_cars -= 1
                    neighbour.number_cars += 1
                    self.vertex = neighbour
                    self.vertex.number_visited += 1
                    if random() > 0.95:
                        self.active = False
        else:
            pass
        self.local_time += 1


def load_stations(path):
    with open(path) as f:
        data = json.load(f)
    return [[int(i[0] * 78700), int(i[1] * 111130)] for i in data['stations']] # тупой перевод в прямоугольные координаты


def build_vertexes():
    global GRAPH
    GRAPH = defaultdict()
    vertexes = []
    counter = 0
    for i in STATIONS:
        vertexes.append(Vertex(0, True, i))
        VERTEX_DICT[vertexes[-1]] = counter
        counter += 1
    with open('roads.txt', 'r') as f:
        x = f.readlines()
        for j in x:
            w = j.split(' ')
            for i in range(0, len(w), 2):
                if i + 1 >= len(w):# and w[i + 1] != '\n' and w[i] != '\n':
                    break
                vtx = Vertex(0, False, [int(float((w[i + 1])) * 78700), int(float(w[i])) * 111130])
                if vtx not in VERTEX_DICT.keys():
                    vertexes.append(vtx)
                    VERTEX_DICT[vtx] = counter
                    counter += 1
                if i >= 2:
                    vtx2 = Vertex(0, False, [int(float(w[i - 1])) * 78700, int(float(w[i - 2])) * 111130])
                    if vtx not in GRAPH.keys():
                        GRAPH[vtx] = []
                    GRAPH[vtx].append(vtx2)
                    if vtx2 not in GRAPH.keys():
                        GRAPH[vtx2] = []
                    GRAPH[vtx2].append(vtx)
                    GRAPH[vtx].append(vtx2)
    """for i in vertexes:
        print(str(i.get_location()) + str(i.get_is_station()))"""

    for i in range(0, len(STATIONS)):
        for j in range(len(STATIONS), len(vertexes)):
            if vertexes[i] not in GRAPH.keys():
                GRAPH[vertexes[i]] = []
            if vertexes[j] not in GRAPH.keys():
                GRAPH[vertexes[j]] = []
            GRAPH[vertexes[i]].append(vertexes[j])
            GRAPH[vertexes[j]].append(vertexes[i])
    return vertexes


def build_cars():
    return [Car(100 * max(0.6, random()), 0.000000002 * max(0.3, random()), VERTEXES[randint(0, len(VERTEXES) - 1)], 0.9 + random() * 0.1) for i in range(NUMBER_ACTIVE_CARS)]


def export_data():
    data = dict()
    data['stations'] = []
    for station in VERTEXES:
        if station.is_station:
            st = dict()
            st['loc'] = station.location
            st['number_visitors'] = station.number_visited
            st['number_stopped'] = station.number_stopped
            st['sold_gasoline'] = station.sold_gasoline
            data['stations'].append(st)
    json_object = json.dumps(data, indent=4)
    with open("stats.json", "w") as outfile:
        outfile.write(json_object)


def main():
    #if len(sys.argv) != 2:
    #    print('invalid number of arguments')
    #    raise 1
    global STATIONS, VERTEXES, GRAPH, CARS
    STATIONS = load_stations('stations.json')#load_stations(sys.argv[1])
    VERTEXES = build_vertexes()
    CARS = build_cars()

    for i in range(1440):
        print(i)
        for j in range(len(CARS)):
            CARS[j].next_direction(GRAPH[CARS[j].get_vertex()])
        print('progress: ' + str(i + 1) + '/1440')

    for i in VERTEXES:
        if i.get_is_station():
            print(i.location, i.number_visited, i.number_stopped, i.sold_gasoline)

    export_data()


if __name__ == '__main__':
    main()