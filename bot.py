import pyautogui

from solver import MinesweeperSolver
from game import MinesweeperCell


pyautogui.PAUSE = 0.01


def flag_cells(cells: set[MinesweeperCell]):
    for cell in cells:
        pyautogui.rightClick(cell.screen_x, cell.screen_y)


def click_cells(cells: set[MinesweeperCell]):
    for cell in cells:
        pyautogui.leftClick(cell.screen_x, cell.screen_y)


if __name__ == "__main__":
    solver = MinesweeperSolver()
    stop = input("Stop the bot after each turn (y,n): ")
    rule = input("Enter rule: ") if stop == "n" else ""

    for i in range(50):
        if stop == "n":
            safe, mines = solver.find_moves(rule=rule)
        else:
            safe, mines = solver.find_moves(rule=input("Enter rule: "))
        if not safe and not mines:
            break
        click_cells(safe)
        flag_cells(mines)
