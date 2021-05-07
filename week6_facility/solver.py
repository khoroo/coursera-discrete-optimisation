#!/usr/bin/python
# -*- coding: utf-8 -*-
from ortools.sat.python import cp_model
from collections import namedtuple
import math

Point = namedtuple("Point", ["x", "y"])
Facility = namedtuple("Facility", ["index", "setup_cost", "capacity", "location"])
Customer = namedtuple("Customer", ["index", "demand", "location"])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split("\n")

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(
            Facility(
                i - 1,
                float(parts[0]),
                int(parts[1]),
                Point(float(parts[2]), float(parts[3])),
            )
        )

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(
            Customer(
                i - 1 - facility_count,
                int(parts[0]),
                Point(float(parts[1]), float(parts[2])),
            )
        )

    # or-tools
    model = cp_model.CpModel()
    # variables
    x = []
    for i in range(customer_count):
        t = []
        for j in range(facility_count):
            t.append(model.NewBoolVar(f"x[{i},{j}]"))
        x.append(t)
    # constraints
    # Each customer is assigned to exactly one facility
    for i in range(customer_count):
        model.Add(sum(x[i][j] for j in range(facility_count)) == 1)
    # facility demand must be less than or equal capacity
    for j in range(facility_count):
        model.Add(
            sum(customers[i].demand * x[i][j] for i in range(customer_count))
            <= facilities[j].capacity
        )
    # objective
    objective_terms = []
    # distance
    for i in range(customer_count):
        for j in range(facility_count):
            objective_terms.append(
                x[i][j] * int(length(facilities[j].location, customers[i].location))
            )
    # setup
    for j in range(facility_count):
        objective_terms.append(
            min(sum(x[i][j] for i in range(customer_count)), 1)
            * int(facilities[j].setup_cost)
        )

    model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = {}
        for i in range(customer_count):
            for j in range(facility_count):
                if solver.BooleanValue(x[i][j]):
                    solution[i] = j
    else:
        raise ValueError("no solution found")

    obj = sum(facilities[j].setup_cost for j in set(solution.values()))
    obj += sum(
        length(customers[i].location, facilities[j].location)
        for i, j in solution.items()
    )

    # prepare the solution in the specified output format
    output_data = "%.2f" % obj + " " + str(0) + "\n"
    output_data += " ".join(map(str, [solution[i] for i in range(customer_count)]))

    return output_data


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
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)"
        )
