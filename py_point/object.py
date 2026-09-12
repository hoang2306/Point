GRAVITY: float = 0.4

class Vec2:
    """Position 2D struct matching C++ Vec2."""
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = float(x)
        self.y: float = float(y)


class Vel2:
    """Velocity 2D struct matching C++ Vel2."""
    def __init__(self, Vx: float = 0.0, Vy: float = 0.0) -> None:
        self.Vx: float = float(Vx)
        self.Vy: float = float(Vy)


class Acc2:
    """Acceleration 2D struct matching C++ Acc2."""
    def __init__(self, Ax: float = 0.0, Ay: float = 0.0) -> None:
        self.Ax: float = float(Ax)
        self.Ay: float = float(Ay)


class Object:
    """Game entity object (friends/pumpkins and evil enemies/spiders)."""

    def __init__(self, evil: bool, x: float, y: float, len_val: float) -> None:
        self._posn = Vec2(x, y)
        self._velocity = Vel2(0.0, 0.0)
        self._acceleration = Acc2(0.0, 0.0)
        self._len: float = float(len_val)
        self._evil: bool = evil

    def update_posn(self, delta_time: float = 1.0) -> None:
        self._velocity.Vx += self._acceleration.Ax * delta_time
        self._posn.x += self._velocity.Vx * delta_time
        self._velocity.Vy += self._acceleration.Ay * delta_time
        self._posn.y += self._velocity.Vy * delta_time

    # Getters
    def get_len(self) -> float:
        return self._len

    def get_posn(self) -> Vec2:
        return self._posn

    def get_vel(self) -> Vel2:
        return self._velocity

    def get_acc(self) -> Acc2:
        return self._acceleration

    def is_evil(self) -> bool:
        return self._evil

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
