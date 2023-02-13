import pyautogui

import numpy as np
from PIL import ImageGrab
from pyscreeze import center


X_OFFSET = 1920
SAMPLES = {
    "0": "msx-0.png",
    "1": "msx-1.png",
    "2": "msx-2.png",
    "3": "msx-3.png",
    "4": "msx-4.png",
    "5": "msx-5.png",
    "6": "msx-6.png",
    "7": "msx-7.png",
    "8": "msx-8.png",
    "C": "msx-covered.png",
    "F": "msx-flag.png",
    "M": "msx-mine.png",
    "E": "msx-explosion.png",
}


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
        grid = np.empty(self.size, dtype=str)
        for value, sample in SAMPLES.items():
            boxes = pyautogui.locateAll(f"samples/{sample}", screen)
            for box in boxes:
                point = center(box)
                x = point.x // 16
                y = point.y // 16
                grid[y, x] = value
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


def print_grid(grid):
    print("-" * (grid.shape[0] * 2 + 3))
    print(str(grid).replace("C", " ").replace("'", ""))


if __name__ == "__main__":
    game = MinesweeperBoard()
    print(game.size)
    print_grid(game.get_grid())
