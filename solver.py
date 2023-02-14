import numpy as np

from game import MinesweeperBoard, MinesweeperCell


class MinesweeperSolver:
    def __init__(self):
        self.game = MinesweeperBoard()

    def find_moves(self, rule=""):
        grid = self.game.get_grid()
        numbers: list[MinesweeperCell] = [
            cell for cell in grid.flat if cell.value in range(1, 9)
        ]
        groups: list[MinesweeperGroup] = []
        group_hashes = []
        safe = []
        mines = []

        for cell in numbers:
            covered_neighbors = covered(cell, grid)
            flag_count = flags(cell, grid)

            # Basic Rule 1: If the number equals the number of mines, they are all safe
            if cell.value == flag_count:
                safe.extend(covered_neighbors)
            # Basic Rule 2: If the number equals the number of covered cells, they are all mines
            elif cell.value - flag_count == len(covered_neighbors):
                mines.extend(covered_neighbors)
            # Create group
            elif covered_neighbors:
                group = MinesweeperGroup(
                    set(covered_neighbors), cell.value - flag_count
                )
                if hash(group) not in group_hashes:
                    groups.append(group)
                    group_hashes.append(hash(group))

        if rule == "basic":
            return set(safe), set(mines)

        # Groups
        for a in groups:
            for b in groups:
                if a is not b and a.cells.issubset(b.cells):
                    # If they have the same number of mines, the difference is safe
                    if b.mines == a.mines:
                        safe.extend(list(b.cells - a.cells))

                    # If the difference in cells is the same as the difference in mines, the difference is mines
                    if len(b.cells - a.cells) == b.mines - a.mines:
                        mines.extend(list(b.cells - a.cells))

                    # If B has more mines, create a new group that contains, B-A cells and B-A mines
                    if b.mines > a.mines:
                        group = MinesweeperGroup(b.cells - a.cells, b.mines - a.mines)
                        if hash(group) not in group_hashes:
                            groups.append(group)
                            group_hashes.append(hash(group))

        if rule == "groups":
            return set(safe), set(mines)

        return set(safe), set(mines)


class MinesweeperGroup:
    def __init__(self, cells: set[MinesweeperCell], mines: int):
        self.cells = cells
        self.mines = mines

    def __str__(self) -> str:
        return f"Cells:{len(self.cells)} Mines:{self.mines}"

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.cells, key=lambda x: str(x))))


def in_grid(x, y, grid: np.ndarray):
    return x >= 0 and y >= 0 and x < grid.shape[0] and y < grid.shape[1]


def neighbours(cell: MinesweeperCell, grid: np.ndarray):
    cells = []
    for x in (cell.x - 1, cell.x, cell.x + 1):
        for y in (cell.y - 1, cell.y, cell.y + 1):
            if in_grid(x, y, grid) and cell != grid[x, y]:
                cells.append(grid[x, y])
    return cells


def flags(cell: MinesweeperCell, grid: np.ndarray):
    count = 0
    for flag in neighbours(cell, grid):
        if flag.value == "F":
            count += 1
    return count


def covered(cell: MinesweeperCell, grid: np.ndarray):
    return [cover for cover in neighbours(cell, grid) if cover.value == "C"]


if __name__ == "__main__":
    solver = MinesweeperSolver()
    safe, mines = solver.find_moves()

    print("Safe:")
    for cell in safe:
        print(cell)

    print("Mines:")
    for cell in mines:
        print(cell)
