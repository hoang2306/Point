import math
from typing import Optional

class Vector:
    """2D Vector representation matching C++ struct Vector."""

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = float(x)
        self.y: float = float(y)

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)


class VectorAlgebra:
    """Algebraic operations on Vector instances matching C++ VectorAlgebra class."""

    @staticmethod
    def add(a: Vector, b: Vector) -> Vector:
        return Vector(a.x + b.x, a.y + b.y)

    @staticmethod
    def sub(a: Vector, b: Vector) -> Vector:
        return Vector(a.x - b.x, a.y - b.y)

    @staticmethod
    def scalar_mul(a: float, b: Vector) -> Vector:
        return Vector(a * b.x, a * b.y)

    @staticmethod
    def dot(a: Vector, b: Vector) -> float:
        return a.x * b.x + a.y * b.y

    @staticmethod
    def cross(a: Vector, b: Vector) -> float:
        return a.x * b.y - a.y * b.x

    @staticmethod
    def length(a: Vector) -> float:
        return math.hypot(a.x, a.y)

    @staticmethod
    def unit(a: Vector) -> Vector:
        len_a = VectorAlgebra.length(a)
        if len_a == 0.0:
            return Vector(0.0, 0.0)
        return Vector(a.x / len_a, a.y / len_a)

    @staticmethod
    def cos_v(a: Vector, b: Vector) -> float:
        len_prod = VectorAlgebra.length(a) * VectorAlgebra.length(b)
        if len_prod == 0.0:
            return 0.0
        return VectorAlgebra.dot(a, b) / len_prod

    @staticmethod
    def sin_v(a: Vector, b: Vector) -> float:
        len_prod = VectorAlgebra.length(a) * VectorAlgebra.length(b)
        if len_prod == 0.0:
            return 0.0
        return VectorAlgebra.cross(a, b) / len_prod

    @staticmethod
    def tan_v(a: Vector, b: Vector) -> float:
        dot_val = VectorAlgebra.dot(a, b)
        if dot_val == 0.0:
            return 0.0
        return VectorAlgebra.cross(a, b) / dot_val

    @staticmethod
    def rotate(obj: Vector, hinge: Vector, theta: float) -> Vector:
        dx = obj.x - hinge.x
        dy = obj.y - hinge.y
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        rx = dx * cos_t - dy * sin_t
        ry = dx * sin_t + dy * cos_t
        return Vector(hinge.x + rx, hinge.y + ry)

    @staticmethod
    def reduce(obj: Vector, hinge: Vector, delta: float) -> None:
        direction = VectorAlgebra.sub(obj, hinge)
        u = VectorAlgebra.unit(direction)
        obj.x -= u.x * delta
        obj.y -= u.y * delta
