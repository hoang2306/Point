from typing import Optional, Tuple
import pygame

class LTexture:
    """Helper class for loading and rendering text textures using Pygame TTF Font."""

    def __init__(self) -> None:
        self._texture: Optional[pygame.Surface] = None
        self._width: int = 0
        self._height: int = 0

    def load_from_rendered_text(
        self,
        texture_text: str,
        text_color: Tuple[int, int, int, int],
        font: Optional[pygame.font.Font],
    ) -> bool:
        """Create Pygame surface from text string and TTF font."""
        self.free()
        if font is None:
            return False

        color_rgb = (text_color[0], text_color[1], text_color[2])
        try:
            self._texture = font.render(texture_text, True, color_rgb)
            if self._texture is not None:
                self._width = self._texture.get_width()
                self._height = self._texture.get_height()
                return True
        except Exception as e:
            print(f"Unable to render text surface! Error: {e}")

        return False

    def free(self) -> None:
        """Free text surface resources."""
        self._texture = None
        self._width = 0
        self._height = 0

    def render(self, x: int, y: int, screen: pygame.Surface) -> None:
        """Render text texture onto screen at specified position."""
        if self._texture is not None and screen is not None:
            screen.blit(self._texture, (x, y))

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height
