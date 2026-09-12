import os
import tempfile
import pytest
from py_point.main import read_scores, save_scores

def test_scoreboard_read_save():
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write("100\n500\n300\n")
        tmp_path = tmp.name

    try:
        scores = read_scores(tmp_path)
        assert scores == {100, 300, 500}

        scores.add(700)
        save_scores(scores, tmp_path)

        updated = read_scores(tmp_path)
        assert updated == {100, 300, 500, 700}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
