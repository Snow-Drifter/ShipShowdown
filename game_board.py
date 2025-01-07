from ship import *


class Board:
    def __init__(self):
        self.boats = {}

    def place_ship_horizontally(self, ship: Ship, left_point: tuple[int, int]):
        x, y = left_point
        length = ship.size

        if y < 0 or y >= 10:
            # too high/low
            return False

        if x < 0 or x >= 10 or x + length > 10:
            # too left/right
            return False
        else:
            for i in range(length):
                # check each coordinate boat will be at
                if (x + i, y) in self.boats:
                    # return false if boat already exists in path
                    return False
            return True

    def place_ship_vertically(self, ship: Ship, top_point: tuple[int, int]):
        x, y = top_point
        length = ship.size

        if y < 0 or y >= 10 or y + length > 10:
            # too high/low
            return False

        if x < 0 or x >= 10:
            # too left/right
            return False
        else:
            for i in range(length):
                # check each coordinate boat will be at
                if (x, y + i) in self.boats:
                    # return false if boat already exists in path
                    return False
            return True
