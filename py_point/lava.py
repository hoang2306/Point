class Lava:
    """Lava hazard rising from the bottom of the screen."""

    def __init__(self, x: float, y: float, len_val: float, wid_val: float) -> None:
        self._length: int = int(len_val)
        self._width: int = int(wid_val)
        self._pos_x: float = float(x)
        self._pos_y: float = float(y)
        self._vel_x: float = 0.0
        self._vel_y: float = 0.0
        self._accln_x: float = 0.0
        self._accln_y: float = 0.0

    def update_posn(self, delta_time: float = 1.0) -> None:
        self._vel_x += self._accln_x * delta_time
        self._pos_x += self._vel_x * delta_time
        self._vel_y += self._accln_y * delta_time
        self._pos_y += self._vel_y * delta_time

    # Getters
    def get_posn_x(self) -> float:
        return self._pos_x

    def get_posn_y(self) -> float:
        return self._pos_y

    def get_vel_x(self) -> float:
        return self._vel_x

    def get_vel_y(self) -> float:
        return self._vel_y

    def get_accln_x(self) -> float:
        return self._accln_x

    def get_accln_y(self) -> float:
        return self._accln_y

    def get_width(self) -> float:
        return float(self._width)

    def get_length(self) -> float:
        return float(self._length)

    # Setters
    def set_acc_x(self, acc: float) -> None:
        self._accln_x = float(acc)

    def set_acc_y(self, acc: float) -> None:
        self._accln_y = float(acc)

    def set_posn_x(self, x: float) -> None:
        self._pos_x = float(x)

    def set_posn_y(self, y: float) -> None:
        self._pos_y = float(y)

    def set_vel_x(self, x: float) -> None:
        self._vel_x = float(x)

    def set_vel_y(self, y: float) -> None:
        self._vel_y = float(y)
