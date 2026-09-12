import random
from typing import List
from py_point.object import Object
from py_point.me import Me

class ObjectManager:
    """Spawns game objects (pumpkins and spiders) across level chunks."""

    def __init__(self, window_width: int, window_height: int, main_object: Me) -> None:
        self.window_width: int = window_width
        self.window_height: int = window_height
        self.main_object: Me = main_object

    def spawn(self, enemy_list: List[Object], frend_list: List[Object], bias: int) -> None:
        """Spawn a chunk of objects with specified horizontal bias."""
        # Special 1 (Top section)
        sp1_x = self.window_width / 2.0 + bias
        sp1_y = self.window_height / 4.0
        special1 = Object(False, sp1_x, sp1_y, 20.0)
        frend_list.append(special1)

        min_x1 = int(special1.get_posn().x - self.window_width / 2.0)
        max_x1 = int(special1.get_posn().x + self.window_width / 2.0)
        min_y1 = int(special1.get_posn().y - self.window_height / 4.0)
        max_y1 = int(special1.get_posn().y)

        range_x1 = max(1, max_x1 - min_x1 + 1)
        range_y1 = max(1, max_y1 - min_y1 + 1)

        for _ in range(10):
            rand_x = random.randrange(range_x1) + min_x1
            rand_y = random.randrange(range_y1) + min_y1
            frend_list.append(Object(False, float(rand_x), float(rand_y), 20.0))

        for _ in range(2):
            rand_x = random.randrange(range_x1) + min_x1
            rand_y = random.randrange(range_y1) + min_y1
            enemy_list.append(Object(True, float(rand_x), float(rand_y), 20.0))

        # Special 2 (Middle section)
        sp2_x = self.window_width / 2.0 + bias
        sp2_y = self.window_height / 2.0
        special2 = Object(False, sp2_x, sp2_y, 20.0)
        frend_list.append(special2)

        min_x2 = int(special2.get_posn().x - self.window_width / 2.0)
        max_x2 = int(special2.get_posn().x + self.window_width / 2.0)
        min_y2 = int(special2.get_posn().y - self.window_height / 4.0)
        max_y2 = int(special2.get_posn().y + self.window_height / 4.0)

        range_x2 = max(1, max_x2 - min_x2 + 1)
        range_y2 = max(1, max_y2 - min_y2 + 1)

        for _ in range(45):
            rand_x = random.randrange(range_x2) + min_x2
            rand_y = random.randrange(range_y2) + min_y2
            frend_list.append(Object(False, float(rand_x), float(rand_y), 20.0))

        for _ in range(3):
            rand_x = random.randrange(range_x2) + min_x2
            rand_y = random.randrange(range_y2) + min_y2
            enemy_list.append(Object(True, float(rand_x), float(rand_y), 20.0))

        # Special 3 (Bottom section)
        sp3_x = self.window_width / 2.0 + bias
        sp3_y = 3.0 * self.window_height / 4.0
        special3 = Object(False, sp3_x, sp3_y, 20.0)
        frend_list.append(special3)

        min_x3 = int(special3.get_posn().x - self.window_width / 2.0)
        max_x3 = int(special3.get_posn().x + self.window_width / 2.0)
        min_y3 = int(special3.get_posn().y)
        max_y3 = int(special3.get_posn().y + self.window_height / 4.0)

        range_x3 = max(1, max_x3 - min_x3 + 1)
        range_y3 = max(1, max_y3 - min_y3 + 1)

        for _ in range(10):
            rand_x = random.randrange(range_x3) + min_x3
            rand_y = random.randrange(range_y3) + min_y3
            frend_list.append(Object(False, float(rand_x), float(rand_y), 20.0))

        for _ in range(2):
            rand_x = random.randrange(range_x3) + min_x3
            rand_y = random.randrange(range_y3) + min_y3
            enemy_list.append(Object(True, float(rand_x), float(rand_y), 20.0))
