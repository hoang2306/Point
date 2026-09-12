import os
import sys
from typing import List, Optional, Set
import pygame

from py_point.render_window import RenderWindow, resolve_path
from py_point.object import Object, GRAVITY
from py_point.me import Me
from py_point.lava import Lava
from py_point.rope import Rope
from py_point.event_manager import EventManager
from py_point.object_manager import ObjectManager
from py_point.ltexture import LTexture

WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 720
SCORE_FILE: str = "ScoreBoard.txt"


def read_scores(filename: str = SCORE_FILE) -> Set[int]:
    """Read scores from file into integer set matching C++ score loading."""
    scores: Set[int] = set()
    resolved = resolve_path(filename)
    if os.path.exists(resolved):
        try:
            with open(resolved, "r", encoding="utf-8") as f:
                for line in f:
                    for token in line.strip().split():
                        try:
                            scores.add(int(token))
                        except ValueError:
                            pass
        except Exception as e:
            print(f"Could not read score file '{filename}': {e}")
    return scores


def save_scores(scores: Set[int], filename: str = SCORE_FILE) -> None:
    """Save score set to file matching C++ score file format."""
    resolved = resolve_path(filename)
    try:
        with open(resolved, "w", encoding="utf-8") as f:
            for s in sorted(scores):
                f.write(f"{s}\n")
    except Exception as e:
        print(f"Could not save score file '{filename}': {e}")


def main() -> int:
    """Main entry point for Point game."""
    pygame.init()
    pygame.font.init()

    # Initialize audio safely
    audio_available = True
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        music_path = resolve_path("sound/happy_fun_bg.mp3")
        sound_path = resolve_path("sound/eat_point.wav")
        blast_path = resolve_path("sound/dead.wav")

        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)

        sound_eat = pygame.mixer.Sound(sound_path) if os.path.exists(sound_path) else None
        sound_dead = pygame.mixer.Sound(blast_path) if os.path.exists(blast_path) else None
    except Exception as e:
        print(f"Audio device unavailable or initialization error: {e}")
        audio_available = False
        sound_eat = None
        sound_dead = None

    window = RenderWindow("POINT", WINDOW_WIDTH, WINDOW_HEIGHT)
    clock = pygame.time.Clock()

    game_running: bool = True
    main_game: bool = False
    end_menu: bool = False
    high_score: int = 0
    score_set: Set[int] = read_scores()

    gTextTexture = LTexture()
    gTextTexture1 = LTexture()
    gTextTexture2 = LTexture()
    gTextTexture3 = LTexture()
    gTextTexture4 = LTexture()
    gTextTexture5 = LTexture()
    gTextTexture6 = LTexture()
    gTextTexture61 = LTexture()
    gTextTexture62 = LTexture()
    gTextTexture63 = LTexture()
    gTextTexture7 = LTexture()
    gTextTexture8 = LTexture()

    # Setup Main Menu
    window.main_menu(gTextTexture1, gTextTexture2, gTextTexture3)

    # Game State Variables
    main_object: Optional[Me] = None
    enemy_list: List[Object] = []
    frend_list: List[Object] = []
    a_rope: Optional[Rope] = None
    an_event = EventManager()
    lava: Optional[Lava] = None
    om: Optional[ObjectManager] = None
    spawn_counter: int = 0
    roped: bool = False
    total_score: int = 0
    collided: bool = False
    grass_texture = window.load_texture("texture/BLACK.jpg")

    def init_game_session():
        nonlocal main_object, enemy_list, frend_list, a_rope, lava, om, spawn_counter, roped, total_score, collided
        roped = False
        total_score = 0
        collided = False
        enemy_list.clear()
        frend_list.clear()

        main_object = Me(600.0, 400.0, 20.0, 0.0, 0.0)
        a_rope = Rope()
        om = ObjectManager(WINDOW_WIDTH, WINDOW_HEIGHT, main_object)
        spawn_counter = 0

        for _ in range(7):
            om.spawn(enemy_list, frend_list, spawn_counter * WINDOW_WIDTH)
            spawn_counter += 1

        lava = Lava(0.0, 700.0, 500.0, 1280.0)

    while game_running:
        clock.tick(60)  # Limit frame rate to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if not main_game and not end_menu:
                    k1 = gTextTexture3.get_width()
                    k2 = gTextTexture2.get_width()
                    game_running = an_event.exit_mouse_click(mx, my, 600, k1, WINDOW_WIDTH)
                    main_game = an_event.play_mouse_click(mx, my, k2, WINDOW_WIDTH)
                    if main_game:
                        init_game_session()

                elif main_game and not end_menu:
                    if a_rope and main_object:
                        roped = an_event.mouse_click(
                            event.type, event.button, mx, my, a_rope, main_object, enemy_list, frend_list
                        )

                elif not main_game and end_menu:
                    k1 = gTextTexture5.get_width()
                    k2 = gTextTexture4.get_width()
                    game_running = an_event.exit_mouse_click(mx, my, 540, k1, WINDOW_WIDTH)
                    retry_clicked = an_event.retry_mouse_click(mx, my, k2, WINDOW_WIDTH)
                    if not retry_clicked:
                        end_menu = False
                        main_game = True
                        init_game_session()

            elif event.type == pygame.MOUSEBUTTONUP:
                if main_game and not end_menu:
                    if a_rope and main_object:
                        mx, my = pygame.mouse.get_pos()
                        roped = an_event.mouse_click(
                            event.type, event.button, mx, my, a_rope, main_object, enemy_list, frend_list
                        )

        # Rendering & Updates
        if not main_game and not end_menu:
            window.clear()
            gTextTexture1.render((WINDOW_WIDTH - gTextTexture1.get_width()) // 2, 100, window.screen)
            gTextTexture2.render((WINDOW_WIDTH - gTextTexture2.get_width()) // 2, 350, window.screen)
            gTextTexture3.render((WINDOW_WIDTH - gTextTexture3.get_width()) // 2, 600, window.screen)
            window.display()

        elif main_game and not end_menu:
            window.clear()

            if main_object and lava:
                collided = main_object.check_collision(enemy_list, lava)
                scored_idx = main_object.check_score_hit(frend_list)

                if scored_idx != -1:
                    if sound_eat:
                        sound_eat.play()
                    total_score += 100
                    frend_list.pop(scored_idx)

                if not collided:
                    window.render(grass_texture)
                    window.draw_object(main_object)
                    window.draw_enemy_object(enemy_list)
                    window.draw_frend_object(frend_list)
                    window.draw_lava(lava)

                    if roped and a_rope and a_rope.get_target():
                        main_object.set_acc_y(0.0)
                        window.draw_line(main_object, a_rope.get_target())
                        roped = a_rope.rope_calculus(roped, enemy_list, frend_list, lava)

                    if not roped:
                        for enemy in enemy_list:
                            enemy.set_acc_y(-GRAVITY)
                            enemy.set_acc_x(0.0)
                        for frend in frend_list:
                            frend.set_acc_y(-GRAVITY)
                            frend.set_acc_x(0.0)
                        lava.set_acc_x(0.0)
                        lava.set_acc_y(-GRAVITY)

                    for enemy in enemy_list:
                        enemy.update_posn()
                    for frend in frend_list:
                        frend.update_posn()
                    lava.update_posn()

                else:
                    # Collided -> Game Over
                    if sound_dead:
                        sound_dead.play()
                    end_menu = True
                    main_game = False
                    if total_score > high_score:
                        high_score = total_score

                    score_set = read_scores()
                    score_set.add(total_score)
                    if high_score > 0:
                        score_set.add(high_score)
                    save_scores(score_set)

                    window.end_menu(
                        total_score,
                        score_set,
                        gTextTexture,
                        gTextTexture1,
                        gTextTexture2,
                        gTextTexture3,
                        gTextTexture4,
                        gTextTexture5,
                        gTextTexture6,
                        gTextTexture61,
                        gTextTexture62,
                        gTextTexture63,
                    )

            window.score_menu(total_score, gTextTexture7, gTextTexture8)
            gTextTexture7.render(1100, 10, window.screen)
            gTextTexture8.render(30, 10, window.screen)
            window.display()

        elif not main_game and end_menu:
            window.clear()
            gTextTexture.render(755, 98, window.screen)
            gTextTexture1.render((WINDOW_WIDTH - gTextTexture1.get_width()) // 2, 100, window.screen)
            gTextTexture2.render(500, 220, window.screen)
            gTextTexture3.render(500, 280, window.screen)
            gTextTexture6.render(720, 220, window.screen)

            gTextTexture61.render(760, 250, window.screen)
            gTextTexture62.render(760, 280, window.screen)
            gTextTexture63.render(760, 310, window.screen)

            gTextTexture4.render((WINDOW_WIDTH - gTextTexture4.get_width()) // 2, 400, window.screen)
            gTextTexture5.render((WINDOW_WIDTH - gTextTexture5.get_width()) // 2, 540, window.screen)
            window.display()

    # Clean up and shutdown
    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
