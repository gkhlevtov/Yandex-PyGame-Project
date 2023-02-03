import sys

import pygame
from pygame import mixer

import menu as menu
from globals import Button
from globals import fps, \
    click_sound, button_sound, \
    display_width, display_height, \
    w_percent, h_percent
from globals import load_image, RunWindow, read_data


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    pygame.display.set_caption('Настройки игры')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    cursor_img = load_image("arrow.png")
    cursor_img = pygame.transform.scale(cursor_img, (36 * display_width // 1920, 63 * display_height // 1080))

    cursor_img_rect = cursor_img.get_rect()

    background_image = load_image('background_big.jpg')
    scaled_background = pygame.transform.scale(background_image, (display_width, display_height))

    buttons = pygame.sprite.Group()
    button_sizes = (w_percent * 15, h_percent * 10)

    button_x = w_percent * 4
    button_y = h_percent * 15
    go_back_button = Button((button_x, button_y), button_sizes[0], button_sizes[1], (255, 173, 64), 'Назад',
                            h_percent * 7,
                            (0, 0, 0))

    go_back_button.set_func(RunWindow(menu).run)
    buttons.add(go_back_button)

    clock = pygame.time.Clock()

    running = True
    use_custom_cursor = read_data('settings_values.txt')[1]

    while running:
        screen.blit(scaled_background, (0, 0))

        if use_custom_cursor == '1':
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

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

        if pygame.mouse.get_focused() and use_custom_cursor == '1':
            cursor_img_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
