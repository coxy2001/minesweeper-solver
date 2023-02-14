import numpy as np
import pyautogui

from PIL import ImageGrab
from pyscreeze import center


X_OFFSET = 1920
SAMPLES = {
    "-": "msx-0.png",
    1: "msx-1.png",
    2: "msx-2.png",
    3: "msx-3.png",
    4: "msx-4.png",
    5: "msx-5.png",
    6: "msx-6.png",
    7: "msx-7.png",
    8: "msx-8.png",
    "C": "msx-covered.png",
    "F": "msx-flag.png",
    "M": "msx-mine.png",
    "E": "msx-explosion.png",
}


class MinesweeperCell:
    def __init__(self, x, y, value, screen_x, screen_y):
        self.x = x
        self.y = y
        self.value = value
        self.screen_x = screen_x
        self.screen_y = screen_y

    def __str__(self) -> str:
        return f"({self.x}, {self.y}) {self.value}"


class MinesweeperBoard:
    def __init__(self):
        self.find_game()

    def find_game(self):
        full_screen = ImageGrab.grab(all_screens=True)
        top_left = pyautogui.locate("samples/msx-top_left.png", full_screen)
        bottom_right = pyautogui.locate("samples/msx-bottom_right.png", full_screen)

        if not (top_left and bottom_right):
            raise Exception("Game not found")

        self.left = top_left.left + top_left.width - X_OFFSET
        self.right = bottom_right.left - X_OFFSET
        self.top = top_left.top + top_left.height
        self.bottom = bottom_right.top

    def get_grid(self):
        screen = ImageGrab.grab(
            bbox=(self.left, self.top, self.right, self.bottom),
            all_screens=True,
        )
        grid = np.empty(self.size, dtype=MinesweeperCell)
        for value, sample in SAMPLES.items():
            boxes = pyautogui.locateAll(f"samples/{sample}", screen)
            for box in boxes:
                point = center(box)
                x = point.x // 16
                y = point.y // 16
                grid[x, y] = MinesweeperCell(
                    x, y, value, point.x + self.left, point.y + self.top
                )
        return grid

    @property
    def width(self):
        return (self.right - self.left) // 16

    @property
    def height(self):
        return (self.bottom - self.top) // 16

    @property
    def size(self):
        return (self.width, self.height)


def print_grid(grid: np.ndarray):
    print("-" * (grid.shape[0] * 2))
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x, y].value == "C":
                print(" ", end=" ")
            else:
                print(grid[x, y].value, end=" ")
        print()


if __name__ == "__main__":
    game = MinesweeperBoard()
    print(game.size)
    print_grid(game.get_grid())
