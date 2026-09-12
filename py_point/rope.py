import math
from typing import List, Optional, Tuple
from py_point.object import Vec2, Vel2, Object, GRAVITY
from py_point.me import Me
from py_point.lava import Lava

K: float = 0.0005
ORIGINAL_LEN: float = 0.0

class Rope:
    """Rope physics and target attachment manager."""

    def __init__(self) -> None:
        self._me_node: Optional[Me] = None
        self._other_node: Optional[Object] = None
        self._initial_posn = Vec2(0.0, 0.0)
        self._initial_vel = Vel2(0.0, 0.0)
        self._rope_length: float = 0.0
        self._slack_occurrence = Vec2(0.0, 0.0)

    def set_target(
        self,
        mouse_x: int,
        mouse_y: int,
        hero: Me,
        enemy_list: List[Object],
        frend_list: List[Object],
    ) -> None:
        """Find closest object to mouse click position and attach rope."""
        target_mouse_distance = float("inf")
        selected_node: Optional[Object] = None

        for enemy in enemy_list:
            if enemy is None:
                continue
            pos = enemy.get_posn()
            sep = (mouse_x - pos.x) ** 2 + (mouse_y - pos.y) ** 2
            if sep < target_mouse_distance:
                selected_node = enemy
                target_mouse_distance = sep

        for frend in frend_list:
            if frend is None:
                continue
            pos = frend.get_posn()
            sep = (mouse_x - pos.x) ** 2 + (mouse_y - pos.y) ** 2
            if sep < target_mouse_distance:
                selected_node = frend
                target_mouse_distance = sep

        self._other_node = selected_node
        self._me_node = hero

        if self._other_node is not None and self._me_node is not None:
            self._initial_posn = Vec2(self._other_node.get_posn().x, self._other_node.get_posn().y)
            self._initial_vel = Vel2(self._other_node.get_vel().Vx, self._other_node.get_vel().Vy)
            dx = self._other_node.get_posn().x - self._me_node.get_posn().x
            dy = self._other_node.get_posn().y - self._me_node.get_posn().y
            self._rope_length = math.hypot(dx, dy)

    def give_initial_sep(self) -> float:
        if self._other_node is None or self._me_node is None:
            return 0.0
        dx = self._other_node.get_posn().x - self._me_node.get_posn().x
        dy = self._other_node.get_posn().y - self._me_node.get_posn().y
        return dy * dy + dx * dx

    def rope_calculus(
        self,
        roped: bool,
        enemy_list: List[Object],
        frend_list: List[Object],
        lava: Lava,
    ) -> bool:
        """Calculate swinging physics state every frame while roped."""
        if self._other_node is None or self._me_node is None:
            return False

        dx = self._other_node.get_posn().x - self._me_node.get_posn().x
        dy = self._other_node.get_posn().y - self._me_node.get_posn().y

        counter_clock = True
        if self._initial_posn.x - self._me_node.get_posn().x > 0 and self._initial_vel.Vy > 0:
            counter_clock = False
        if self._initial_posn.x - self._me_node.get_posn().x < 0 and self._initial_vel.Vy < 0:
            counter_clock = False

        xwrt_o = dx
        ywrt_o = dy

        vsqr = (
            self._initial_vel.Vx ** 2
            + self._initial_vel.Vy ** 2
            - 2 * GRAVITY * (self._other_node.get_posn().y - self._initial_posn.y)
        )

        if not roped:
            for it in enemy_list:
                if it:
                    it.set_acc_y(-GRAVITY)
            for it in frend_list:
                if it:
                    it.set_acc_y(-GRAVITY)
            if lava:
                lava.set_acc_y(-GRAVITY)
            return False

        if vsqr <= 0 and roped:
            return False

        vnet = math.sqrt(vsqr)

        # Reset accelerations while roped
        for it in enemy_list:
            if it:
                it.set_acc_x(0.0)
                it.set_acc_y(0.0)
        for it in frend_list:
            if it:
                it.set_acc_x(0.0)
                it.set_acc_y(0.0)
        if lava:
            lava.set_acc_x(0.0)
            lava.set_acc_y(0.0)

        if counter_clock:
            if xwrt_o == 0:
                vel_x = -vnet if ywrt_o < 0 else vnet
                for it in enemy_list:
                    if it:
                        it.set_vel_x(vel_x)
                        it.set_vel_y(0.0)
                for it in frend_list:
                    if it:
                        it.set_vel_x(vel_x)
                        it.set_vel_y(0.0)
                if lava:
                    lava.set_vel_x(0.0)
                    lava.set_vel_y(0.0)
            else:
                theta = math.atan(xwrt_o / ywrt_o)
                sin_t = math.sin(theta)
                cos_t = math.cos(theta)

                if xwrt_o > 0 and ywrt_o < 0:
                    vx, vy = -vnet * cos_t, vnet * sin_t
                elif xwrt_o > 0 and ywrt_o > 0:
                    vx, vy = vnet * cos_t, -vnet * sin_t
                elif xwrt_o < 0 and ywrt_o > 0:
                    vx, vy = vnet * cos_t, -vnet * sin_t
                else:  # xwrt_o < 0 and ywrt_o < 0
                    vx, vy = -vnet * cos_t, vnet * sin_t

                for it in enemy_list:
                    if it:
                        it.set_vel_x(vx)
                        it.set_vel_y(vy)
                for it in frend_list:
                    if it:
                        it.set_vel_x(vx)
                        it.set_vel_y(vy)
                if lava:
                    lava.set_vel_x(0.0)
                    lava.set_vel_y(vy)
        else:
            # Clockwise
            if xwrt_o == 0:
                vel_x = vnet if ywrt_o < 0 else -vnet
                for it in enemy_list:
                    if it:
                        it.set_vel_x(vel_x)
                        it.set_vel_y(0.0)
                for it in frend_list:
                    if it:
                        it.set_vel_x(vel_x)
                        it.set_vel_y(0.0)
                if lava:
                    lava.set_vel_x(0.0)
                    lava.set_vel_y(0.0)
            else:
                theta = math.atan(xwrt_o / ywrt_o)
                sin_t = math.sin(theta)
                cos_t = math.cos(theta)

                if xwrt_o > 0 and ywrt_o < 0:
                    vx, vy = vnet * cos_t, -vnet * sin_t
                elif xwrt_o > 0 and ywrt_o > 0:
                    vx, vy = -vnet * cos_t, vnet * sin_t
                elif xwrt_o < 0 and ywrt_o > 0:
                    vx, vy = -vnet * cos_t, vnet * sin_t
                else:  # xwrt_o < 0 and ywrt_o < 0
                    vx, vy = vnet * cos_t, -vnet * sin_t

                for it in enemy_list:
                    if it:
                        it.set_vel_x(vx)
                        it.set_vel_y(vy)
                for it in frend_list:
                    if it:
                        it.set_vel_x(vx)
                        it.set_vel_y(vy)
                if lava:
                    lava.set_vel_x(0.0)
                    lava.set_vel_y(vy)

        return True

    # Getters and Setters
    def get_target(self) -> Optional[Object]:
        return self._other_node

    def give_me(self) -> Optional[Me]:
        return self._me_node

    def give_other(self) -> Optional[Object]:
        return self._other_node

    def get_slack_occurrence(self) -> Vec2:
        return self._slack_occurrence

    def set_initial_posn(self, posn: Vec2) -> None:
        self._initial_posn = posn

    def set_initial_vel(self, vel: Vel2) -> None:
        self._initial_vel = vel

    def set_rope_length(self, length: float) -> None:
        self._rope_length = float(length)

    def set_slack_occurrence(self, posn: Vec2) -> None:
        self._slack_occurrence = posn
