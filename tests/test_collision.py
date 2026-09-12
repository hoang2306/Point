import pytest
from py_point.object import Object
from py_point.me import Me
from py_point.lava import Lava

def test_player_enemy_collision():
    hero = Me(600.0, 400.0, 20.0) # width = 30, height = 20, rect = (600, 400) to (630, 420)
    lava = Lava(0.0, 700.0, 500.0, 1280.0) # Y: 700 to 1200

    # Enemy overlapping hero
    enemy_touching = Object(True, 610.0, 405.0, 20.0)
    assert hero.check_collision([enemy_touching], lava) is True

    # Enemy far away
    enemy_far = Object(True, 100.0, 100.0, 20.0)
    assert hero.check_collision([enemy_far], lava) is False

def test_player_lava_collision():
    hero_high = Me(600.0, 400.0, 20.0)
    lava = Lava(0.0, 410.0, 500.0, 1280.0) # Lava top boundary at Y=410, hero Y range = 400..420
    assert hero_high.check_collision([], lava) is True

def test_score_hit():
    hero = Me(600.0, 400.0, 20.0)
    pumpkin1 = Object(False, 610.0, 405.0, 20.0) # close to hero
    pumpkin2 = Object(False, 1000.0, 1000.0, 20.0) # far

    hit_idx = hero.check_score_hit([pumpkin2, pumpkin1])
    assert hit_idx == 1
