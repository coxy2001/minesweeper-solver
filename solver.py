import numpy as np

from game import MinesweeperBoard, MinesweeperCell


class MinesweeperSolver:
    def __init__(self):
        self.game = MinesweeperBoard()

    def find_moves(self):
        grid = self.game.get_grid()
        safe = []
        mines = []
        # Basic
        # Rule 1: If the number equals the number of mines, they are all safe
        for cell in grid.flat:
            if cell.value in range(1, 9):
                if cell.value == type_count(cell, grid, "F"):
                    for neighbour in neighbours(cell, grid):
                        if neighbour.value == "C" and neighbour not in safe:
                            safe.append(neighbour)

        # Rule 2: If the number equals the number of covered cells, they are all mines
        for cell in grid.flat:
            if cell.value in range(1, 9):
                if cell.value - type_count(cell, grid, "F") == type_count(
                    cell, grid, "C"
                ):
                    for neighbour in neighbours(cell, grid):
                        if neighbour.value == "C" and neighbour not in mines:
                            mines.append(neighbour)

        # Groups

        # Subgroups

        return safe, mines


def in_grid(x, y, grid: np.ndarray):
    return x >= 0 and y >= 0 and x < grid.shape[0] and y < grid.shape[1]


def neighbours(cell: MinesweeperCell, grid: np.ndarray):
    cells = []
    for x in (cell.x - 1, cell.x, cell.x + 1):
        for y in (cell.y - 1, cell.y, cell.y + 1):
            if in_grid(x, y, grid) and cell != grid[x, y]:
                cells.append(grid[x, y])
    return cells


def type_count(cell, grid, cell_type):
    count = 0
    for neighbour in neighbours(cell, grid):
        if neighbour.value == cell_type:
            count += 1
    return count


if __name__ == "__main__":
    solver = MinesweeperSolver()
    safe, mines = solver.find_moves()

    print("Safe:")
    for cell in safe:
        print(cell)

    print("Mines:")
    for cell in mines:
        print(cell)
