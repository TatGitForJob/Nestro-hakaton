# -*- coding: utf-8 -*-
"""MAS_fast.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KEzR2gAMSCKlZ1HV0Tl46xb1ane3Lxq_
"""

from random import random, randint, shuffle
from math import sqrt, sin, cos
import json
import sys

NUMBER_ACTIVE_CARS = 10#int(3271000 * 0.235 * 0.3)

STATIONS = None
VERTEXES = None
GRAPH = None
CARS = None

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
    return [[i[0] * 78.7, i[1] * 111.13] for i in data['stations']] # тупой перевод в прямоугольные координаты


def build_vertexes():
    return [
        Vertex(0, False, [2, 2]),
        Vertex(1, True, [2, 3]),
        Vertex(2, False, [0, 0]),
        Vertex(3, False, [4, 1]),
        Vertex(4, False, [8, 6]),
        Vertex(5, False, [3, 7]),
        Vertex(6, True, [9, 12])
    ]


def build_graph():
    GRAPH = dict()
    GRAPH[VERTEXES[0]] = [VERTEXES[2], VERTEXES[4], VERTEXES[6]]
    GRAPH[VERTEXES[1]] = [VERTEXES[2], VERTEXES[3], VERTEXES[5]]
    GRAPH[VERTEXES[2]] = [VERTEXES[0], VERTEXES[1]]
    GRAPH[VERTEXES[3]] = [VERTEXES[1], VERTEXES[4], VERTEXES[5], VERTEXES[6]]
    GRAPH[VERTEXES[4]] = [VERTEXES[0], VERTEXES[3]]
    GRAPH[VERTEXES[5]] = [VERTEXES[1], VERTEXES[3], VERTEXES[6]]
    GRAPH[VERTEXES[6]] = [VERTEXES[0], VERTEXES[3], VERTEXES[5]]
    return GRAPH


def build_cars():
    return [Car(10, 0.1, VERTEXES[randint(0, 6)], 0.9 + random() * 0.1) for i in range(5)]


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
    if len(sys.argv) != 2:
        print('invalid number of arguments')
        raise 1
    global STATIONS, VERTEXES, GRAPH, CARS
    STATIONS = load_stations(sys.argv[1])
    VERTEXES = build_vertexes()
    GRAPH = build_graph()
    CARS = build_cars()

    for i in range(1440):
        for j in range(len(CARS)):
            CARS[j].next_direction(GRAPH[CARS[j].get_vertex()])

    for i in VERTEXES:
        print(i.location, i.number_visited, i.number_stopped, i.sold_gasoline)
    
    export_data()


if __name__ == '__main__':
    main()