import pytest
from py_point.event_manager import EventManager

def test_event_manager_menu_clicks():
    em = EventManager()
    scr_width = 1280
    text_width = 100

    # Exit button in main menu at Y=600, height 38
    # Center X = (1280 - 100) // 2 = 590, range 590..690
    assert em.exit_mouse_click(640, 610, 600, text_width, scr_width) is False # Click inside EXIT -> exit game
    assert em.exit_mouse_click(100, 100, 600, text_width, scr_width) is True  # Click outside -> keep running

    # Play button in main menu Y range 350..388
    assert em.play_mouse_click(640, 360, text_width, scr_width) is True # Click inside PLAY -> start main game
    assert em.play_mouse_click(100, 100, text_width, scr_width) is False # Click outside -> no state change

    # Retry button in end menu Y range 400..436
    assert em.retry_mouse_click(640, 410, text_width, scr_width) is False # Click RETRY -> retry game (end_menu=False)
    assert em.retry_mouse_click(100, 100, text_width, scr_width) is True
