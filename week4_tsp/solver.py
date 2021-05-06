#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from functools import cache
from numba import njit

def compute_euclidean_distance_matrix(locations):
    X = np.array(locations)
    dist_sq = np.sum((X[:, np.newaxis, :] - X[np.newaxis, :, :]) ** 2, axis = -1)
    return (dist_sq * 10000).astype(np.int64)

def solve_it(input_data):
    lines = input_data.split('\n')
    nodecount = int(lines[0])
    parse = lambda x: map(float, x.split())
    data = {}
    data['locations'] = []
    data['num_vehicles'] = 1
    data['depot'] = 0
    for l in lines[1:-1]:
        data['locations'].append(tuple(parse(l)))


    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 600

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    
    plan_output = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        plan_output.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))

    obj = 0
    for p1, p2 in zip(plan_output[:-1], plan_output[1:]):
        x1, y1 = data['locations'][p1]
        x2, y2 = data['locations'][p2]
        obj += math.sqrt((x1-x2)**2 + (y1-y2)**2)

    output_data = '%.2f' % obj + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, plan_output))

    return output_data

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
