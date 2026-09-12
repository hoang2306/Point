from typing import List, Optional
import pygame
from py_point.object import Object
from py_point.me import Me
from py_point.rope import Rope

class EventManager:
    """Handles UI mouse hit testing and in-game mouse input matching C++ EventManager."""

    def exit_mouse_click(self, x: int, y: int, text_y: int, text_width: int, scr_width: int) -> bool:
        """Check if mouse click hits EXIT button. Returns False to exit game loop, True to continue."""
        min_x = (scr_width - text_width) // 2
        max_x = (scr_width + text_width) // 2
        if min_x <= x <= max_x and text_y <= y <= text_y + 38:
            return False
        return True

    def play_mouse_click(self, x: int, y: int, text_width: int, scr_width: int) -> bool:
        """Check if mouse click hits PLAY button in Main Menu. Returns True to start game."""
        min_x = (scr_width - text_width) // 2
        max_x = (scr_width + text_width) // 2
        if min_x <= x <= max_x and 349 < y <= 388:
            return True
        return False

    def retry_mouse_click(self, x: int, y: int, text_width: int, scr_width: int) -> bool:
        """Check if mouse click hits RETRY button in End Menu. Returns False to restart game."""
        min_x = (scr_width - text_width) // 2
        max_x = (scr_width + text_width) // 2
        if min_x <= x <= max_x and 399 < y <= 436:
            return False
        return True

    def mouse_click(
        self,
        event_type: int,
        button: int,
        mouse_x: int,
        mouse_y: int,
        a_rope: Rope,
        main_object: Me,
        enemy_list: List[Object],
        frend_list: List[Object],
    ) -> bool:
        """Handle gameplay mouse button events for rope attachment/release."""
        if event_type == pygame.MOUSEBUTTONDOWN and button == 1:
            a_rope.set_target(mouse_x, mouse_y, main_object, enemy_list, frend_list)
            return True
        elif event_type == pygame.MOUSEBUTTONUP:
            return False
        return False
