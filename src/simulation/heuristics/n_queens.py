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
        self.status = SolverStatus.UNSOLVED

    @staticmethod
    def _count_queen_conflicts(queen_positions_per_row: list[int]) -> list[int]:
        size = len(queen_positions_per_row)
        conflicts = [0] * size

        for i in range(size):
            for j in range(i + 1, size):
                if queen_positions_per_row[i] == queen_positions_per_row[j] or abs(
                    queen_positions_per_row[i] - queen_positions_per_row[j]
                ) == abs(i - j):
                    conflicts[i] += 1
                    conflicts[j] += 1

        return conflicts

    def _has_conflicts(self) -> bool:
        queen_conflicts = Solver._count_queen_conflicts(self.board.queen_positions_per_row)
        self._queen_conflicts = queen_conflicts
        return any(conflicts > 0 for conflicts in self._queen_conflicts)

    def solve(self) -> None:
        while self.current_step < self.max_steps and self._has_conflicts():
            self.current_step += 1
            max_conflict_queens = self._find_max_conflict_queens()
            queen_to_move = random.choice(max_conflict_queens)  # noqa: S311
            min_conflict_positions = self._find_min_conflict_positions(queen_to_move)
            new_position = random.choice(min_conflict_positions)  # noqa: S311
            self.board.queen_positions_per_row[queen_to_move] = new_position

        if self._has_conflicts():
            self.status = SolverStatus.REACHED_MAX_NUMBER_OF_STEPS
            raise RuntimeError("Failed to solve the board within the maximum number of steps.")  # noqa: TRY003

        self.status = SolverStatus.SOLVED

    def _find_max_conflict_queens(self) -> list[int]:
        max_conflicts = max(self._queen_conflicts)
        max_conflict_queens = [i for i, conflicts in enumerate(self._queen_conflicts) if conflicts == max_conflicts]
        return max_conflict_queens

    def _find_min_conflict_positions(self, queen_index: int) -> list[int]:
        size = self.board.size
        queen_positions_per_row = self.board.queen_positions_per_row
        min_conflicts = float("inf")
        min_conflict_positions = []

        for position in range(size):
            if position == queen_positions_per_row[queen_index]:
                continue
            original_position = queen_positions_per_row[queen_index]
            queen_positions_per_row[queen_index] = position
            conflicts = Solver._count_queen_conflicts(queen_positions_per_row)[queen_index]
            queen_positions_per_row[queen_index] = original_position

            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_positions = [position]
            elif conflicts == min_conflicts:
                min_conflict_positions.append(position)

        return min_conflict_positions


def main() -> None:
    board = Chessboard.from_random_permutation(64)
    solver = Solver(board, max_steps=100)
    solver.solve()
    print(f"Solved board in {solver.current_step} steps.")
    # print(solver.board)


if __name__ == "__main__":
    main()
