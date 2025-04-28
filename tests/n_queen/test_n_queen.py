import pytest

from simulation.heuristics.n_queens import Chessboard, Solver, SolverStatus


def test_test():
    assert True


def test_unsolvable_board():
    max_steps = 10

    board = Chessboard.from_random_permutation(3)
    solver = Solver(board, max_steps)
    with pytest.raises(RuntimeError, match="Failed to solve the board") as _e:
        solver.solve()
    assert solver.status == SolverStatus.REACHED_MAX_NUMBER_OF_STEPS

    board = Chessboard.from_random_permutation(3)
    solver = Solver(board, max_steps)
    with pytest.raises(RuntimeError, match="Failed to solve the board"):
        solver.solve()
    assert solver.status == SolverStatus.REACHED_MAX_NUMBER_OF_STEPS


def test_8_queens():
    board = Chessboard.from_random_permutation(8)
    solver = Solver(board)
    solver.solve()
    assert solver.status == SolverStatus.SOLVED
