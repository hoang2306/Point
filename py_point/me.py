import math
from typing import List, Optional
from py_point.object import Vec2, Vel2, Acc2, Object
from py_point.lava import Lava

class Me:
    """Player hero entity (the Ghost character)."""

    def __init__(self, x: float, y: float, len_val: float, vx: float = 0.0, vy: float = 0.0) -> None:
        self._posn = Vec2(x, y)
        self._width: float = 1.5 * len_val
        self._height: float = float(len_val)
        self._velocity = Vel2(vx, vy)
        self._acceleration = Acc2(0.0, 0.0)

    def check_collision(self, enemy_list: List[Object], lava: Lava) -> bool:
        """Check AABB collision against enemies (spiders) or lava."""
        for enemy in enemy_list:
            if enemy is None:
                continue
            e_pos = enemy.get_posn()
            e_len = enemy.get_len()
            if (
                self._posn.x < e_pos.x + e_len
                and self._posn.x + self._width > e_pos.x
                and self._posn.y < e_pos.y + e_len
                and self._posn.y + self._height > e_pos.y
            ):
                return True

        if lava is not None:
            l_pos_y = lava.get_posn_y()
            l_len = lava.get_length()
            if self._posn.y < l_pos_y + l_len and self._posn.y + self._height > l_pos_y:
                return True

        return False

    def check_score_hit(self, frend_list: List[Optional[Object]]) -> int:
        """Check radius collision against pumpkins (friends). Returns index if hit, else -1."""
        for i, frend in enumerate(frend_list):
            if frend is None:
                continue
            r_ideal = self.get_width() + frend.get_len()
            r_ideal_sq = r_ideal * r_ideal
            separation_sq = (self._posn.x - frend.get_posn().x) ** 2 + (self._posn.y - frend.get_posn().y) ** 2
            if separation_sq <= r_ideal_sq:
                return i
        return -1

    # Getters
    def get_posn(self) -> Vec2:
        return self._posn

    def get_vel(self) -> Vel2:
        return self._velocity

    def get_acc(self) -> Acc2:
        return self._acceleration

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    # Setters
    def set_acc_x(self, acc: float) -> None:
        self._acceleration.Ax = float(acc)

    def set_acc_y(self, acc: float) -> None:
        self._acceleration.Ay = float(acc)

    def set_posn_x(self, x: float) -> None:
        self._posn.x = float(x)

    def set_posn_y(self, y: float) -> None:
        self._posn.y = float(y)

    def set_vel_x(self, velx: float) -> None:
        self._velocity.Vx = float(velx)

    def set_vel_y(self, vely: float) -> None:
        self._velocity.Vy = float(vely)
