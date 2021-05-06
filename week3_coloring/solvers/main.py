import numpy as np
from numba import njit


def parse(fpath):
    with open(fpath, 'r') as f:
        N, _ = map(int, f.readline().split())
        arr = np.zeros((N, N), dtype=np.int8)
        line = f.readline()
        while line:
            i, j = map(int, line.split())
            arr[i, j] = 1
            arr[j, i] = 1
            line = f.readline()
    return arr



def main():

    return 1

if __name__ == '__main__':
    main()
