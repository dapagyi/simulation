import pytest

from simulation.heuristics.n_queens import Chessboard, Solver, SolverStatus


def test_test():
    assert True


def test_permutation_initialization():
    board = Chessboard.from_random_permutation(1000)
    assert len(set(board.queen_positions_per_row)) == 1000


def test_unsolvable_board():
    max_steps = 100

    for n in [2, 3]:
        board = Chessboard.from_random_permutation(n)
        solver = Solver(board)
        with pytest.raises(RuntimeError, match="Failed to solve the board"):
            solver.solve()
        assert solver.status == SolverStatus.REACHED_MAX_NUMBER_OF_STEPS
        assert solver.current_step == max_steps


def test_n_queens():
    for n in [4, 8, 16, 32, 64]:
        max_steps = n * 100

        board = Chessboard.from_random_permutation(n)
        solver = Solver(board, max_steps=max_steps)
        assert solver.status == SolverStatus.UNSOLVED
        assert solver.current_step == 0
        solver.solve()

        assert solver.status == SolverStatus.SOLVED
        assert solver.current_step < max_steps
        assert len(set(solver.board.queen_positions_per_row)) == n

        # Test for conflicts
        for row, col in enumerate(solver.board.queen_positions_per_row):
            assert solver._count_conflicts_for_position(row, col) == 0

        # Test conflicts manually
        for i in range(n):
            for j in range(i + 1, n):
                assert solver.board.queen_positions_per_row[i] != solver.board.queen_positions_per_row[j]
                assert abs(i - j) != abs(
                    solver.board.queen_positions_per_row[i] - solver.board.queen_positions_per_row[j]
                )
