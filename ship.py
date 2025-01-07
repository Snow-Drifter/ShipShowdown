class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def default_ships() -> list[Ship]:
    return [
        Ship("Patrol Boat", 2),
        Ship("Submarine", 3),
        Ship("Destroyer", 3),
        Ship("Battleship", 4),
        Ship("Carrier", 5),
    ]
