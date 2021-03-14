#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = defaultdict(list)
    for i in range(1, edge_count + 1):
        line = lines[i]
        u, v = map(int, line.split())
        edges[u].append(v)
        edges[v].append(u)

    colors = [None for _ in range(node_count)]
    # straight forward greedy algorithm
    # first node has color 0
    upperbound = set(range(node_count))

    # sort by degree decending
    node_order = sorted(edges.keys(), key=lambda x: len(edges[x]), reverse=True)

    colors[node_order[0]] = 0
    for i in node_order[1:]:
        neighbours = {colors[j] for j in edges[i] if colors[j] != None}
        lowest_available = min(upperbound - neighbours)
        colors[i] = lowest_available


    # prepare the solution in the specified output format
    colors_count = len(set(colors))
    output_data = str(colors_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, colors))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

