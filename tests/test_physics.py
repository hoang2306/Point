import math
import pytest
from py_point.object import Object, GRAVITY
from py_point.me import Me
from py_point.lava import Lava
from py_point.rope import Rope

def test_object_movement_and_gravity():
    obj = Object(False, 100.0, 100.0, 20.0)
    obj.set_acc_y(-GRAVITY)
    obj.update_posn()
    assert obj.get_vel().Vy == pytest.approx(-0.4)
    assert obj.get_posn().y == pytest.approx(99.6)

def test_lava_movement():
    lava = Lava(0.0, 700.0, 500.0, 1280.0)
    lava.set_acc_y(-GRAVITY)
    lava.update_posn()
    assert lava.get_vel_y() == pytest.approx(-0.4)
    assert lava.get_posn_y() == pytest.approx(699.6)

def test_rope_target_selection():
    hero = Me(600.0, 400.0, 20.0)
    frend1 = Object(False, 650.0, 400.0, 20.0)
    frend2 = Object(False, 800.0, 400.0, 20.0)
    enemy1 = Object(True, 700.0, 400.0, 20.0)

    rope = Rope()
    # Click near frend1
    rope.set_target(652, 401, hero, [enemy1], [frend1, frend2])
    assert rope.get_target() == frend1

def test_rope_calculus_behavior():
    hero = Me(600.0, 400.0, 20.0)
    frend = Object(False, 650.0, 400.0, 20.0)
    enemy = Object(True, 700.0, 400.0, 20.0)
    lava = Lava(0.0, 700.0, 500.0, 1280.0)

    rope = Rope()
    rope.set_target(650, 400, hero, [enemy], [frend])
    is_roped = rope.rope_calculus(True, [enemy], [frend], lava)
    # Accelerations are zeroed when roped
    assert enemy.get_acc().Ax == 0.0
    assert frend.get_acc().Ax == 0.0
    assert lava.get_accln_x() == 0.0
