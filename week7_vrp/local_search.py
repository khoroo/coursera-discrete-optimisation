import numpy as np
from numba import njit


@njit
def init_sol(demands, locations, v_count, v_capacity):
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


def main():
    demands = np.array([0, 3, 3, 3, 3])
    locations = np.array([[0, 0], [0, 10], [-10, 10], [0, -10], [10, -10]])
    v_count = 4
    v_capacity = 10
    s0 = init_sol(demands, locations, v_count, v_capacity)
    s_format = sol_format(s0, v_count)
    print(s_format)


if __name__ == "__main__":
    main()
