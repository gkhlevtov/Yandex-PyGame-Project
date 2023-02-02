import sys

import pygame
from pygame import mixer

import main as game
import rules
import settings
import statistics
from globals import Button, ImageButton
from globals import fps, use_custom_cursor, \
    click_sound, button_sound, \
    display_width, display_height, \
    w_percent, h_percent
from globals import load_image, RunWindow


def close_game():
    print('Goodbye!')
    pygame.quit()
    sys.exit()


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    mixer.music.load('sounds/background_music_1.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    pygame.display.set_caption('Poker Combos')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    logo_img = load_image("logo.png")
    logo_img = pygame.transform.scale(logo_img, (600 * display_width // 1920, 400 * display_height // 1080))
    logo_img_rect = logo_img.get_rect()
    logo_x = display_width // 2 - logo_img_rect.width // 2
    logo_y = w_percent * 2

    cursor_img = load_image("arrow.png")
    cursor_img = pygame.transform.scale(cursor_img, (36 * display_width // 1920, 63 * display_height // 1080))

    cursor_img_rect = cursor_img.get_rect()

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    buttons = pygame.sprite.Group()
    button_sizes = (w_percent * 30, h_percent * 10)
    buttons_text = ('Играть', 'Статистика', 'Правила', 'Выйти')
    buttons_funcs = (RunWindow(game).run, RunWindow(statistics).run, RunWindow(rules).run, close_game)

    for i in range(4):
        button_x = display_width // 2 - button_sizes[0] // 2
        button_y = display_height // 2 - button_sizes[1] // 2 - 10 * h_percent + 15 * i * h_percent

        button = Button((button_x, button_y), button_sizes[0], button_sizes[1], (255, 173, 64), buttons_text[i],
                        h_percent * 7,
                        (0, 0, 0))

        button.set_func(buttons_funcs[i])
        buttons.add(button)

    settings_button = ImageButton((w_percent * 90, h_percent * 3), w_percent * 7, w_percent * 7, (255, 173, 64),
                                  'Настройки', h_percent * 7, (0, 0, 0), 'settings.png')

    settings_button.set_func(RunWindow(settings).run)

    buttons.add(settings_button)
    clock = pygame.time.Clock()

    running = True

    while running:
        screen.blit(scaled_background, (0, 0))
        screen.blit(logo_img, (logo_x, logo_y))

        if use_custom_cursor:
            pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.check_mouse_position((pos[0], pos[1])):
                        button.set_color(True)
                        break
                    else:
                        button.set_color(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                click_pos = pygame.mouse.get_pos()

                for button in buttons:
                    if button.check_mouse_position(click_pos):
                        button_sound.play()
                        if button.func is None:
                            print('Nothing happened')
                        else:
                            button.action()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        buttons.update()
        buttons.draw(screen)

        if pygame.mouse.get_focused():
            cursor_img_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
