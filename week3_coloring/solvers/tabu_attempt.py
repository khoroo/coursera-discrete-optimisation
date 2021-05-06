#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from numba import njit
import sys
from collections import deque

@njit
def tabu(N, E, edges, init_sol):
    it = 0
    max_its = 10000
    
    while it < max_its:
        it += 1
    
    return sol

def solve_it(input_data):
    lines = input_data.split('\n')
    
    N, E = map(int, lines[0].split())
    edges = np.empty((E, 2), dtype=np.uint8)

    for i, l in enumerate(lines[1:-1]):
        edges[i] = tuple(map(int, l.split()))


    rng = np.random.default_rng()
    n_colors = 10
    init_sol = rng.integers(n_colors, size=N)
    
    sol = tabu(N, E, edges, init_sol)

    print(adj)
    output_data = None

    
    return output_data



if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

