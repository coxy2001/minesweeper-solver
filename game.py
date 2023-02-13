import pyautogui

import numpy as np
from PIL import ImageGrab
from pyscreeze import center
from time import sleep


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
    "covered": "msx-covered.png",
    "flag": "msx-flag.png",
    "mine": "msx-mine.png",
    "explosion": "msx-explosion.png",
}


class MinesweeperPoint:
    def __init__(self, x, y, value):
        self.x = x // 16
        self.y = y // 16
        self.value = value

    @staticmethod
    def create(box, value):
        point = center(box)
        x = point.x
        y = point.y
        return MinesweeperPoint(x, y, value)

    @staticmethod
    def sort_index(point):
        return point.x + (point.y * 500)


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

    def get_points(self) -> list[MinesweeperPoint]:
        screen = ImageGrab.grab(
            bbox=(self.left, self.top, self.right, self.bottom),
            all_screens=True,
        )
        points = []
        for key, sample in SAMPLES.items():
            boxes = pyautogui.locateAll(f"samples/{sample}", screen)
            for box in boxes:
                points.append(MinesweeperPoint.create(box, key))
        return points

    def get_grid(self):
        points = self.get_points()
        points = sorted(points, key=MinesweeperPoint.sort_index)

        grid = []
        row = []
        y = 0
        for point in points:
            if point.y != y:
                grid.append(row)
                row = []
                y = point.y
            row.append(point.value)
        grid.append(row)
        self.grid = grid
        return grid

    def print_grid(self):
        for row in self.grid:
            print(f"| ", end="")
            for item in row:
                if item == "covered":
                    item = " "
                elif item == "flag":
                    item = "F"
                elif item == "mine":
                    item = "M"
                elif item == "explosion":
                    item = "E"
                print(f"{item} | ", end="")
            print()

    def print_header(self):
        print("+---" * game.width + "+")

    @property
    def width(self):
        return (self.right - self.left) // 16

    @property
    def height(self):
        return (self.bottom - self.top) // 16

    @property
    def size(self):
        return f"{self.width} x {self.height}"


if __name__ == "__main__":
    game = MinesweeperBoard()
    print(game.size)

    game.print_header()
    while True:
        game.get_grid()
        game.print_grid()
        game.print_header()
        sleep(1)
