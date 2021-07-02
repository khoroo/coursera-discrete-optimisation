#!/usr/bin/python3

import math


def distance(q, p):
    q1, q2 = q
    p1, p2 = p
    return math.sqrt((q1-p1)**2 + (q2-p2)**2)



def main():
    f_locs = [
        (1065.0, 1065.0),
        (1062.0, 1062.0),
        (0.0, 0.0),
    ]
    c_locs = [(1397.0, 1397.0), (1398.0, 1398.0), (1399.0, 1399.0), (586.0, 586.0)]

    d = []
    for f in f_locs:
        row = []
        for c in c_locs:
            val = int(round(distance(c, f), 0))
            row.append(val)
        d.append(row)

    
    for row in d:
       print(row)


if __name__ == "__main__":
    main()
