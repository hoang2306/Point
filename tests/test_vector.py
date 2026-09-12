import math
import pytest
from py_point.vector import Vector, VectorAlgebra

def test_vector_creation_and_operators():
    v1 = Vector(3.0, 4.0)
    v2 = Vector(1.0, 2.0)

    v_add = v1 + v2
    assert v_add.x == 4.0
    assert v_add.y == 6.0

    v_sub = v1 - v2
    assert v_sub.x == 2.0
    assert v_sub.y == 2.0

    v_mul = v1 * 2.0
    assert v_mul.x == 6.0
    assert v_mul.y == 8.0

    v_rmul = 3.0 * v2
    assert v_rmul.x == 3.0
    assert v_rmul.y == 6.0

def test_vector_algebra():
    v1 = Vector(3.0, 4.0)
    v2 = Vector(1.0, 0.0)

    assert VectorAlgebra.length(v1) == pytest.approx(5.0)
    assert VectorAlgebra.dot(v1, v2) == pytest.approx(3.0)
    assert VectorAlgebra.cross(v1, v2) == pytest.approx(-4.0)

    unit_v1 = VectorAlgebra.unit(v1)
    assert unit_v1.x == pytest.approx(0.6)
    assert unit_v1.y == pytest.approx(0.8)

def test_vector_rotation():
    hinge = Vector(0.0, 0.0)
    obj = Vector(1.0, 0.0)
    rotated = VectorAlgebra.rotate(obj, hinge, math.pi / 2)
    assert rotated.x == pytest.approx(0.0, abs=1e-5)
    assert rotated.y == pytest.approx(1.0, abs=1e-5)
