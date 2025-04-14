import random


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
        board_str += f"Queens: {self.queen_positions_per_row}\n"
        return board_str.strip()


class Solver:
    def __init__(self, board: Chessboard, max_steps: int = 100):
        self.board = board
        self.max_steps = max_steps
        self.current_step = 0

    @staticmethod
    def _count_queen_conflicts(queen_positions_per_row: list[int]) -> list[int]:
        size = len(queen_positions_per_row)
        conflicts = [0] * size

        for i in range(size):
            for j in range(i + 1, size):
                if queen_positions_per_row[i] == queen_positions_per_row[j]:
                    conflicts[i] += 1
                    conflicts[j] += 1
                if abs(queen_positions_per_row[i] - queen_positions_per_row[j]) == abs(i - j):
                    conflicts[i] += 1
                    conflicts[j] += 1

        return conflicts

    def _has_conflicts(self) -> bool:
        queen_conflicts = Solver._count_queen_conflicts(self.board.queen_positions_per_row)
        self._queen_conflicts = queen_conflicts
        return any(conflicts > 0 for conflicts in self._queen_conflicts)

    def solve(self) -> None:
        while self.current_step < self.max_steps and self._has_conflicts():
            print(f"Step {self.current_step}:\n{self.board}")
            print(f"Queen conflicts: {self._queen_conflicts}")
            self.current_step += 1
            max_conflict_queen = self._find_max_conflict_queen()
            min_conflict_position = self._find_min_conflict_position(max_conflict_queen)
            print(
                f"Moving queen {max_conflict_queen} from position {self.board.queen_positions_per_row[max_conflict_queen]} to position {min_conflict_position}"
            )
            self.board.queen_positions_per_row[max_conflict_queen] = min_conflict_position
            print()

        if self._has_conflicts():
            raise RuntimeError("Failed to solve the board within the maximum number of steps.")  # noqa: TRY003

    def _find_max_conflict_queen(self) -> int:
        max_conflict_queen = self._queen_conflicts.index(max(self._queen_conflicts))
        return max_conflict_queen

    def _find_min_conflict_position(self, queen_index: int) -> int:
        size = self.board.size
        queen_positions_per_row = self.board.queen_positions_per_row
        min_conflict_position = queen_positions_per_row[queen_index]
        min_conflicts = float("inf")

        for position in range(size):
            if position == queen_positions_per_row[queen_index]:
                continue
            queen_positions_per_row[queen_index] = position
            conflicts = Solver._count_queen_conflicts(queen_positions_per_row)[queen_index]
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_position = position

        queen_positions_per_row[queen_index] = min_conflict_position
        return min_conflict_position


def main() -> None:
    board = Chessboard.from_random_permutation(6)
    solver = Solver(board, max_steps=10)
    solver.solve()
    print("Solved board:")
    print(solver.board)


if __name__ == "__main__":
    main()
