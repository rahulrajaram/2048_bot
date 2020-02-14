import copy

from selenium.webdriver.common.keys import Keys


class Tile:
    def __init__(
            self,
            element=None,
            row=None,
            column=None,
            value=None
    ):
        if element:
            class_name = element.get_attribute('class').split(' ')
            tile_position_attribute = [c for c in element.get_attribute('class').split(' ') if 'tile-position' in c][0]
            self.column, self.row = [int(n) - 1 for n in tile_position_attribute.split('-')[-2:]]
            self.value = int(element.text or 0)
        elif row and column and value:
            self.column, self.row, self.value = column, row, value

    def __str__(self):
        return f'{self.row}, {self.column} -> {self.value}'


class Matrix:
    def __init__(
            self,
            from_browser=True,
            matrix=None,
            browser=None
    ):
        if from_browser and browser:
            tiles = browser.find_elements_by_class_name('tile')
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
        scores = dict()
        scores['l'] = self.on_left()
        scores['r'] = self.on_right()
        scores['u'] = self.on_up()
        scores['d'] = self.on_down()
        # print(scores)
        return max(scores, key=scores.get)

    def _handle_altered_row(
            self,
            matrix,
            reverse=False,
            action_code=None
    ):
        altered_matrix = []
        score_increment = 0
        for row in matrix:
            altered_row = copy.copy(row)
            altered_row = [e for e in altered_row if e != 0]
            if reverse:
                altered_row.reverse()
            removed = []
            skip_next = False
            for i in range(len(altered_row) - 1):
                if altered_row[i] == altered_row[i + 1] and not skip_next:
                    score_increment += altered_row[i + 1] * 2
                    altered_row[i + 1] = altered_row[i + 1] * 2
                    removed.append(i)
                    skip_next = True
                else:
                    skip_next = False
            for i in removed:
                altered_row[i] = 0 
            altered_row = [e for e in altered_row if e != 0]
            for i in range(4 - len(altered_row)):
                altered_row.append(0)
            if reverse:
                altered_row.reverse()
            altered_matrix.append(altered_row)
        if altered_matrix == matrix and score_increment == 0:
            score_increment = -1
        return score_increment

    def on_right(self):
        return self._handle_altered_row(self.matrix, reverse=True, action_code='right')
    
    def on_left(self):
        return self._handle_altered_row(self.matrix, action_code='left')

    def on_up(self):
        return self._handle_altered_row(self.inverted_matrix, action_code='up')

    def on_down(self):
        return self._handle_altered_row(self.inverted_matrix, reverse=True, action_code='down')


class GameContainer:
    def __init__(self, browser):
        self.matrix = Matrix(browser=browser)

    def next_move(self):
        next_state = self.matrix.optimal_next_state()
        if next_state == 'u':
            return Keys.ARROW_UP
        if next_state == 'd':
            return Keys.ARROW_DOWN
        if next_state == 'l':
            return Keys.ARROW_LEFT
        if next_state == 'r':
            return Keys.ARROW_RIGHT
