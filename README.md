# gol-solver

A SAT forward solver for John Conway's "Game of Life" based on z3.

## Usage

You will need Python 3. Initialize virtual environment and install the dependencies:

```bash
virtualenv venv --python=/usr/bin/python3
venv/bin/activate
pip3 install -r requirements.txt
```

Then try to run the solver on the examples:

```bash
python3 solver.py examples/field1.txt
python3 solver.py examples/field2.txt
```

## Field format

The first line describes field settings in the following format: `<width> <height> <number of transitions>`.

Subsequent lines describe the field where:
+ `.` is a dead cell
+ `*` is an alive cell

## References

1. [TAOCP 4A](https://www.amazon.com/Art-Computer-Programming-Combinatorial-Algorithms/dp/0201038048) describes the basic idea behind solving of the Game of Life in chapter 7.2.2.2.
2. [flopp/gol-sat](https://github.com/flopp/gol-sat) – the implementation of the similar solver using C++ and MiniSAT
