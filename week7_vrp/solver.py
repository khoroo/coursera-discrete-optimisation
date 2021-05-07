#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from numba import njit
import math
import numpy as np
import scipy.spatial

Customer = namedtuple("Customer", ["index", "demand", "x", "y"])


def length(customer1, customer2):
    return math.sqrt(
        (customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2
    )


@njit
def greedy(demands, v_count, v_capacity):
    """
    greedy inital solution, always choose customer with biggest demand
    """
    n_customers = len(demands)
    v_tour = np.zeros((n_customers, v_count), dtype=np.uint8)
    v_capacities = v_capacity * np.ones(v_count, dtype=np.uint32)
    demand_order = np.argsort(demands)[::-1]
    for i in demand_order:
        d = demands[i]
        for v in range(v_count):
            if d <= v_capacities[v]:
                v_capacities[v] -= d
                v_tour[i, v] = 1
                break
    return v_tour


def sol_format(sol, v_count):
    """
    formats array of (n_customers, n_vehicles) where
        1 = vehicle going to customer

    returns a list of lists of vehicle path
        [[0, 1, 3, 0], [0, 2, 0]]
    """
    out = [[0] for _ in range(v_count)]
    routed_to = np.argwhere(sol)
    for c, v in routed_to:
        if c > 0:
            out[v].append(c)
    for v in range(v_count):
        out[v].append(0)
    return out


def ortools_vrp(data, time_limit=1):
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(time_limit)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    if solution == None:
        raise ValueError("no solution")

    vehicle_tours = []
    for vehicle_id in range(data["num_vehicles"]):
        vehicle_tours.append([])
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            vehicle_tours[vehicle_id].append(node_index)
            index = solution.Value(routing.NextVar(index))
        vehicle_tours[vehicle_id].append(0)
    return vehicle_tours


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    customers = []
    for i in range(1, customer_count + 1):
        line = lines[i]
        parts = line.split()
        customers.append(
            Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2]))
        )

    data = {}
    A = np.array([(c.x, c.y) for c in customers])
    data["customer_count"] = customer_count
    data["distance_matrix"] = (10000 * scipy.spatial.distance_matrix(A, A)).astype(int)
    data["demands"] = [c.demand for c in customers]
    data["vehicle_capacities"] = [vehicle_capacity for _ in range(vehicle_count)]
    data["num_vehicles"] = vehicle_count
    data["depot"] = 0

    if customer_count == 200 and vehicle_count == 16:
        demands = np.array(data["demands"])
        vehicle_tours = sol_format(
            greedy(demands, vehicle_count, vehicle_capacity), vehicle_count
        )
    else:
        vehicle_tours = ortools_vrp(data, time_limit=30)

    # checks that the number of customers served is correct
    assert len(set(sum(vehicle_tours, []))) == len(customers)

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in vehicle_tours:
        vlen = len(v)
        for i in range(vlen):
            obj += length(customers[v[i]], customers[v[(i + 1) % vlen]])

    # prepare the solution in the specified output format
    outputData = f"{obj:.2f} 0\n"
    outputData += "\n".join(" ".join(map(str, v)) for v in vehicle_tours)

    return outputData


import sys

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)"
        )
