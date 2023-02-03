import sys

import pygame
from pygame import mixer

import menu as menu
from globals import Button
from globals import fps, \
    click_sound, button_sound, \
    display_width, display_height, \
    w_percent, h_percent
from globals import load_image, make_plot, get_max_score_row, RunWindow, read_data


def show_text(row, screen_size, screen):
    """Функция вывода подписей на экран"""
    screen_width, screen_height = screen_size
    w_percent, h_percent = screen_width // 100, screen_height // 100

    font1 = pygame.font.Font('fonts/Intro_Inline.otf', screen_height // 100 * 7)
    font2 = pygame.font.Font('fonts/Intro.otf', screen_height // 100 * 6)

    text1 = font1.render(f'Статистика за последние 15 игр', True, (250, 150, 0))
    text1_x = screen_width // 2 - text1.get_width() // 2
    text1_y = 3 * h_percent

    text2 = font2.render(f'Лучший счёт: {row[1]} очков в игре №{row[0]}', True, (250, 150, 0))
    text2_x = screen_width // 2 - text2.get_width() // 2
    text2_y = 95 * h_percent

    screen.blit(text1, (text1_x, text1_y))
    screen.blit(text2, (text2_x, text2_y))


def main():
    """Основная функция программы."""

    pygame.init()
    mixer.init()

    pygame.display.set_caption('Статистика игр')

    size = (display_width, display_height)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    make_plot()

    plot_img = load_image("plot.png")
    plot_img = pygame.transform.scale(plot_img, (1200 * display_width // 1920, 900 * display_height // 1080))
    plot_rect = plot_img.get_rect()
    plot_x = display_width // 2 - plot_rect.width // 2
    plot_y = w_percent

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

    go_back_button.set_func(RunWindow(menu).run)
    buttons.add(go_back_button)

    clock = pygame.time.Clock()

    running = True
    use_custom_cursor = read_data('settings_values.txt')[1]

    while running:
        screen.blit(scaled_background, (0, 0))
        screen.blit(plot_img, (plot_x, plot_y))

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

        show_text(get_max_score_row(), screen_size=size, screen=screen)

        buttons.update()
        buttons.draw(screen)

        if pygame.mouse.get_focused() and use_custom_cursor == '1':
            cursor_img_rect.center = pygame.mouse.get_pos()
            screen.blit(cursor_img, cursor_img_rect)

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
