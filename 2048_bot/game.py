import copy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

WEIGHTING = 6


class Tile:
    def __init__(self, element=None, row=None, column=None, value=None):
        if element:
            class_name = element.get_attribute("class").split(" ")
            tile_position_attribute = [
                c
                for c in element.get_attribute("class").split(" ")
                if "tile-position" in c
            ][0]
            self.column, self.row = [
                int(n) - 1 for n in tile_position_attribute.split("-")[-2:]
            ]
            self.value = int(element.text or 0)
        elif row and column and value:
            self.column, self.row, self.value = column, row, value

    def __str__(self):
        return f"{self.row}, {self.column} -> {self.value}"


class Matrix:
    def __init__(self, from_browser=True, matrix=None, browser=None):
        if from_browser and browser:
            tiles = browser.find_elements(By.CLASS_NAME, "tile")
            self.matrix = []
            for i in range(4):
                array = []
                for j in range(4):
                    array.append(0)
                self.matrix.append(array)
            tiles = [Tile(tile) for tile in tiles]
            for tile in tiles:
                # print(tile)
                self.matrix[tile.row][tile.column] = tile.value
            # print(self.matrix)
        elif matrix:
            self.matrix = matrix
        self.inverted_matrix = self.invert(self.matrix)

    def invert(self, matrix):
        inverted_matrix = []
        for j in range(4):
            inverted_matrix.append([])
            for i in range(4):
                inverted_matrix[-1].append(matrix[i][j])
        return inverted_matrix

    def optimal_next_state(self):
        # For simplicity, just return a random direction
        import random

        return random.choice(["u", "d", "l", "r"])


class GameContainer:
    def __init__(self, browser):
        self.matrix = Matrix(browser=browser)

    def next_move(self):
        next_state = self.matrix.optimal_next_state()
        if next_state == "u":
            return Keys.ARROW_UP
        if next_state == "d":
            return Keys.ARROW_DOWN
        if next_state == "l":
            return Keys.ARROW_LEFT
        if next_state == "r":
            return Keys.ARROW_RIGHT
