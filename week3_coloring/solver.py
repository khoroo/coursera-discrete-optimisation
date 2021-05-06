#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from numba import njit
import sys
from collections import defaultdict

def welsh_powell(N, nodes):
    nodes_set = set(i for i in range(N))
    nodes_degree = {n: len(nodes[n]) for n in range(N)}
    output = {}
    col_neighs = set()
    col = 0
    while len(output) < N:
        seen = set(output.keys())
        pos = nodes_set - seen - col_neighs
        if len(pos) == 0:
            col_neighs = set()
            col += 1
            continue
        big_pos = max(pos, key=nodes_degree.__getitem__)
        output[big_pos] = col
        col_neighs = col_neighs.union(nodes[big_pos])
    n_cols = col + 1
    return n_cols, output

def solve_it(input_data):
    lines = input_data.split('\n')
    parse = lambda x: map(int, x.split())
    N, E = parse(lines[0])
    nodes = defaultdict(set)
    for l in lines[1:-1]:
        x, y = parse(l)
        nodes[x].add(y)
        nodes[y].add(x)

    n_cols, output = welsh_powell(N, nodes)
    out_node_coloring = ' '.join(str(output[i]) for i in range(N))
    output_data = f'{n_cols} 0\n{out_node_coloring}'

    
    return output_data



if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

