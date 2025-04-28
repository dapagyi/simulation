import random
from enum import Enum, auto


class Chessboard:
    def __init__(self, queen_positions_per_row: list[int]):
        self.queen_positions_per_row = queen_positions_per_row
        self.size = len(queen_positions_per_row)

    @classmethod
    def from_random_permutation(cls, number_of_queens: int, seed: int = 42) -> "Chessboard":
        random.seed(seed)
        queen_positions_per_row = list(range(number_of_queens))
        random.shuffle(queen_positions_per_row)
        return cls(queen_positions_per_row)

    def __repr__(self) -> str:
        board_str = ""
        for i in range(self.size):
            row = ["Q" if j == self.queen_positions_per_row[i] else "." for j in range(self.size)]
            board_str += " ".join(row) + "\n"
        return board_str.strip()


class SolverStatus(Enum):
    UNSOLVED = auto()
    SOLVED = auto()
    REACHED_MAX_NUMBER_OF_STEPS = auto()


class Solver:
    def __init__(self, board: Chessboard, max_steps: int = 100):
        self.board = board
        self.max_steps = max_steps
        self.current_step = 0
        self.row_conflicts = [0] * board.size
        self.diag1_conflicts = [0] * (2 * board.size - 1)  # Top-left to bottom-right diagonals
        self.diag2_conflicts = [0] * (2 * board.size - 1)  # Top-right to bottom-left diagonals
        self._initialize_conflicts()

    def _initialize_conflicts(self) -> None:
        for row, col in enumerate(self.board.queen_positions_per_row):
            self.row_conflicts[col] += 1
            self.diag1_conflicts[row - col + self.board.size - 1] += 1
            self.diag2_conflicts[row + col] += 1

    def _update_conflicts(self, row: int, old_col: int, new_col: int) -> None:
        self.row_conflicts[old_col] -= 1
        self.diag1_conflicts[row - old_col + self.board.size - 1] -= 1
        self.diag2_conflicts[row + old_col] -= 1

        self.row_conflicts[new_col] += 1
        self.diag1_conflicts[row - new_col + self.board.size - 1] += 1
        self.diag2_conflicts[row + new_col] += 1

    def _count_conflicts_for_position(self, row: int, col: int) -> int:
        return (
            self.row_conflicts[col]
            + self.diag1_conflicts[row - col + self.board.size - 1]
            + self.diag2_conflicts[row + col]
            - 3  # Exclude the queen itself
        )

    def _has_conflicts(self) -> bool:
        return any(
            self._count_conflicts_for_position(row, col) > 0
            for row, col in enumerate(self.board.queen_positions_per_row)
        )

    def solve(self) -> None:
        while self.current_step < self.max_steps and self._has_conflicts():
            self.current_step += 1
            max_conflict_queens = self._find_max_conflict_queens()
            queen_to_move = random.choice(max_conflict_queens)  # noqa: S311
            min_conflict_positions = self._find_min_conflict_positions(queen_to_move)
            new_position = random.choice(min_conflict_positions)  # noqa: S311

            old_position = self.board.queen_positions_per_row[queen_to_move]
            self.board.queen_positions_per_row[queen_to_move] = new_position
            self._update_conflicts(queen_to_move, old_position, new_position)

        if self._has_conflicts():
            self.status = SolverStatus.REACHED_MAX_NUMBER_OF_STEPS
            raise RuntimeError("Failed to solve the board within the maximum number of steps.")  # noqa: TRY003

        self.status = SolverStatus.SOLVED

    def _find_max_conflict_queens(self) -> list[int]:
        max_conflicts = -1
        max_conflict_queens = []
        for row, col in enumerate(self.board.queen_positions_per_row):
            conflicts = self._count_conflicts_for_position(row, col)
            if conflicts > max_conflicts:
                max_conflicts = conflicts
                max_conflict_queens = [row]
            elif conflicts == max_conflicts:
                max_conflict_queens.append(row)
        return max_conflict_queens

    def _find_min_conflict_positions(self, queen_index: int) -> list[int]:
        size = self.board.size
        min_conflicts = float("inf")
        min_conflict_positions = []

        for col in range(size):
            if col == self.board.queen_positions_per_row[queen_index]:
                continue
            conflicts = self._count_conflicts_for_position(queen_index, col)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_positions = [col]
            elif conflicts == min_conflicts:
                min_conflict_positions.append(col)

        return min_conflict_positions


def main() -> None:
    board = Chessboard.from_random_permutation(64)
    solver = Solver(board, max_steps=100)
    solver.solve()
    print(f"Solved board in {solver.current_step} steps.")
    # print(solver.board)


if __name__ == "__main__":
    main()
