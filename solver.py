import z3
import os
import sys
from itertools import combinations, product


class SolverError(Exception):
    pass


def print_model(model, field):
    for t in range(len(field)):
        print(f"State {t}:")
        for x in range(len(field[0])):
            row = []
            for y in range(len(field[0][0])):
                row.append('*' if model[field[t][x][y]] else '.')
            print(' '.join(row))
        if t != len(field)-1:
            print()


def create_field(size_x, size_y, transitions):
    field = []
    for t in range(transitions):
        row = [[z3.Bool(f"{x}.{y};t{t}") for y in range(size_y)] for x in range(size_x)]
        field.append(row)
    return field


def parse_input(filename):
    size_x, size_y, transitions = 0, 0, 0
    state = []
    with open(filename, 'r') as f:
        sizes = f.readline()
        size_x, size_y, transitions = sizes.split(' ')
        size_x = int(size_x)
        size_y = int(size_y)
        transitions = int(transitions)
        line = f.readline()
        while line:
            values = line.strip().split(' ')
            if len(values) != size_y:
                raise ValueError(f"Incorrect field size (y = {len(values)} expected = {size_y})")
            values = [v == '*' for v in values]
            state.append(values)
            line = f.readline()
    if len(state) != size_x:
        raise ValueError(f"Incorrect field size (x = {len(state)} expected = {size_x})")
    return size_x, size_y, transitions, state


def get_initial_state_constraints(field, initial_state):
    constraints = []
    for x in range(len(initial_state)):
        for y in range(len(initial_state[0])):
            constraints.append((field[0][x][y] == initial_state[x][y]))
    return constraints


def get_neighbors(field, x, y):
    result = []
    for x_, y_ in product(range(x-1, x+2), range(y-1, y+2)):
        if x_ == x and y_ == y:
            continue
        if x_ in range(0, len(field)) and y_ in range(0, len(field[0])):
            result.append(field[x_][y_])
    return result


def get_gol_rules_constraints(field, transition_num):
    assert(transition_num > 0)
    constraints = []
    t = transition_num
    for x in range(len(field[0])):
        for y in range(len(field[0][0])):
            cell = field[t][x][y]
            prev_cell = field[t-1][x][y]
            prev_neighbours = get_neighbors(field[t-1], x, y)
            # There is a better way based a binary tree approach. It takes
            # advantage of the fact that many intermediate calculations can
            # be shared.
            # See: TAOCP vol. 4 sec. 7.2.2.2.
            constraints.append(
                    cell == z3.And(
                        z3.AtLeast(prev_cell, *prev_neighbours, 3),
                        z3.AtMost(*prev_neighbours, 3)))
    return constraints


def solve_forward(field, initial_state):
    solver = z3.Solver()
    solver.add(z3.And(get_initial_state_constraints(field, initial_state)))
    for t in range(1, len(field)):
        solver.add(get_gol_rules_constraints(field, t))
    result = solver.check()
    if result == z3.sat:
        m = solver.model()
        print_model(m, field)
    return field


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <field>")
        sys.exit(1)
    x, y, transitions, initial_state = parse_input(sys.argv[1])
    field = create_field(x, y, transitions)
    solve_forward(field, initial_state)
