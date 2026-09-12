import os
from typing import List, Optional, Set
import pygame
from py_point.object import Object
from py_point.me import Me
from py_point.lava import Lava
from py_point.ltexture import LTexture

# Base project path for asset resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_path(relative_path: str) -> str:
    """Resolve asset paths relative to the project root directory."""
    path = os.path.join(BASE_DIR, relative_path)
    if not os.path.exists(path):
        # Fallback to direct relative path
        return relative_path
    return path


class RenderWindow:
    """Window management and rendering pipeline matching C++ RenderWindow."""

    def __init__(self, title: str, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.title: str = title

        pygame.display.set_caption(title)
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))
        self._texture_cache = {}

        # Preload sprites
        self.ghost_tex = self.load_texture("texture/Ghost1.png")
        self.spider_tex = self.load_texture("texture/Spider2.png")
        self.gold_tex = self.load_texture("texture/Gold_1.png")

    def load_texture(self, file_path: str) -> Optional[pygame.Surface]:
        """Load image texture from file into Pygame surface with alpha support."""
        if file_path in self._texture_cache:
            return self._texture_cache[file_path]

        resolved = resolve_path(file_path)
        try:
            surface = pygame.image.load(resolved).convert_alpha()
            self._texture_cache[file_path] = surface
            return surface
        except Exception as e:
            print(f"Failed to load texture '{file_path}'. Error: {e}")
            return None

    def clear(self) -> None:
        """Clear screen buffer."""
        self.screen.fill((0, 0, 0))

    def render(self, texture: Optional[pygame.Surface]) -> None:
        """Draw background texture across full window."""
        if texture is not None:
            scaled = pygame.transform.scale(texture, (self.width, self.height))
            self.screen.blit(scaled, (0, 0))

    def display(self) -> None:
        """Present renderer to screen."""
        pygame.display.flip()

    def draw_object(self, obj: Me) -> None:
        """Draw player character (Ghost) at position (x-10, y-10, 32, 32)."""
        if obj is None:
            return
        pos = obj.get_posn()
        dest_rect = pygame.Rect(int(pos.x - 10), int(pos.y - 10), 32, 32)
        if self.ghost_tex is not None:
            scaled = pygame.transform.scale(self.ghost_tex, (32, 32))
            self.screen.blit(scaled, dest_rect)

    def draw_enemy_object(self, enemy_list: List[Object]) -> None:
        """Draw enemy spiders at positions (x-10, y-10, len, len)."""
        if self.spider_tex is None:
            return
        for enemy in enemy_list:
            if enemy is None:
                continue
            pos = enemy.get_posn()
            length = int(enemy.get_len())
            dest_rect = pygame.Rect(int(pos.x - 10), int(pos.y - 10), length, length)
            scaled = pygame.transform.scale(self.spider_tex, (length, length))
            self.screen.blit(scaled, dest_rect)

    def draw_frend_object(self, frend_list: List[Object]) -> None:
        """Draw pumpkins/gold friends at positions (x-10, y-10, len, len)."""
        if self.gold_tex is None:
            return
        for frend in frend_list:
            if frend is None:
                continue
            pos = frend.get_posn()
            length = int(frend.get_len())
            dest_rect = pygame.Rect(int(pos.x - 10), int(pos.y - 10), length, length)
            scaled = pygame.transform.scale(self.gold_tex, (length, length))
            self.screen.blit(scaled, dest_rect)

    def draw_line(self, o1: Me, o2: Object) -> None:
        """Draw cyan rope line from player to attached object."""
        if o1 is None or o2 is None:
            return
        p1 = (int(o1.get_posn().x), int(o1.get_posn().y))
        p2 = (int(o2.get_posn().x), int(o2.get_posn().y))
        pygame.draw.line(self.screen, (0, 255, 255, 255), p1, p2, 1)

    def draw_lava(self, lava: Lava) -> None:
        """Draw gradient lava layers starting at lava position."""
        if lava is None:
            return
        pos_x = lava.get_posn_x()
        pos_y = lava.get_posn_y()
        width = lava.get_width()
        length = lava.get_length()

        for i in range(40):
            rect = pygame.Rect(int(pos_x), int(pos_y + i * 5), int(width), int(length))
            r = max(0, 150 - 3 * i)
            color = (r, 35, 35)
            pygame.draw.rect(self.screen, color, rect)

    def main_menu(
        self,
        text_texture1: LTexture,
        text_texture2: LTexture,
        text_texture3: LTexture,
    ) -> None:
        """Prepare Main Menu text textures."""
        color1 = (210, 105, 30, 255)
        color2 = (0, 255, 0, 255)
        color3 = (178, 34, 34, 255)

        font_path = resolve_path("font/halloween.otf")
        try:
            font1 = pygame.font.Font(font_path, 52)
            font2 = pygame.font.Font(font_path, 38)
        except Exception:
            font1 = pygame.font.SysFont(None, 52)
            font2 = pygame.font.SysFont(None, 38)

        text_texture1.load_from_rendered_text(" POINT ", color1, font1)
        text_texture2.load_from_rendered_text("PLAY", color2, font2)
        text_texture3.load_from_rendered_text("EXIT", color3, font2)

    def score_menu(
        self,
        total_score: int,
        text_texture1: LTexture,
        text_texture2: LTexture,
    ) -> None:
        """Prepare HUD score text textures."""
        color = (255, 255, 0, 255)
        font_path = resolve_path("font/halloween.otf")
        try:
            font = pygame.font.Font(font_path, 26)
        except Exception:
            font = pygame.font.SysFont(None, 26)

        str1 = str(total_score)
        str2 = str(total_score // 100)
        text_texture1.load_from_rendered_text("Score : " + str1, color, font)
        text_texture2.load_from_rendered_text("Kills : " + str2, color, font)

    def end_menu(
        self,
        total_score: int,
        score_set: Set[int],
        text_texture: LTexture,
        text_texture1: LTexture,
        text_texture2: LTexture,
        text_texture3: LTexture,
        text_texture4: LTexture,
        text_texture5: LTexture,
        text_texture6: LTexture,
        text_texture61: LTexture,
        text_texture62: LTexture,
        text_texture63: LTexture,
    ) -> None:
        """Prepare Game Over End Menu text textures."""
        color = (189, 183, 107, 255)
        color1 = (255, 102, 0, 255)
        color2 = (153, 204, 0, 255)
        color3 = (155, 255, 204, 255)
        color4 = (178, 34, 34, 255)

        font_path = resolve_path("font/halloween.otf")
        try:
            font = pygame.font.Font(font_path, 40)
            font1 = pygame.font.Font(font_path, 52)
            font2 = pygame.font.Font(font_path, 24)
            font3 = pygame.font.Font(font_path, 36)
        except Exception:
            font = pygame.font.SysFont(None, 40)
            font1 = pygame.font.SysFont(None, 52)
            font2 = pygame.font.SysFont(None, 24)
            font3 = pygame.font.SysFont(None, 36)

        # Reverse sorted score list matching set<int>::reverse_iterator
        score_list = sorted(list(score_set), reverse=True)
        score_strings = [str(s) for s in score_list]
        while len(score_strings) < 3:
            score_strings.append("0")

        str1 = str(total_score // 100)
        str2 = str(total_score)

        text_texture1.load_from_rendered_text("lmao ded", color1, font1)
        text_texture.load_from_rendered_text("f", color, font)
        text_texture2.load_from_rendered_text("Kills " + str1, color2, font2)
        text_texture3.load_from_rendered_text("Score " + str2, color2, font2)
        text_texture6.load_from_rendered_text("LeaderBoard", color2, font2)
        text_texture61.load_from_rendered_text("1. " + score_strings[0], color1, font2)
        text_texture62.load_from_rendered_text("2. " + score_strings[1], color1, font2)
        text_texture63.load_from_rendered_text("3. " + score_strings[2], color1, font2)
        text_texture4.load_from_rendered_text("RETRY", color3, font3)
        text_texture5.load_from_rendered_text("EXIT", color4, font3)

    def clean_up(self) -> None:
        """Clean up display surface."""
        pass
