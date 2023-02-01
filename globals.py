import csv
import os
import sys

import matplotlib.pyplot
import pygame
import pygame.mixer as mixer

pygame.init()
mixer.init()


class RunWindow:
    """Класс запуска нового окна."""

    def __init__(self, window):
        self.window = window

    def run(self):
        self.window.main()
        pygame.quit()
        sys.exit()


class Button(pygame.sprite.Sprite):
    """Класс кнопки."""

    def __init__(self, position, width, height, color, text, text_size, text_color):
        super().__init__()
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.width = width
        self.height = height
        self.default_color = color
        self.focused_color = (color[0] - 40, color[1] - 40, color[2] - 40)
        self.color = self.default_color
        self.func = None
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        font = pygame.font.Font('fonts/Intro.otf', text_size)
        self.text_line = text
        self.txt = font.render(text, True, text_color)
        self.text_rect = self.txt.get_rect(center=(width // 2, height // 2))
        self.text_rect.center = self.image.get_rect().center
        self.image.blit(self.txt, self.text_rect)

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        self.image.fill(self.color)
        self.image.blit(self.txt, self.text_rect)

    def set_color(self, state):
        if state:
            self.color = self.focused_color
        else:
            self.color = self.default_color

    def set_text(self, text):
        self.text_line = text
        font = pygame.font.Font(None, self.text_size)
        self.txt = font.render(text, True, self.text_color)
        self.text_rect = self.txt.get_rect(center=(self.width // 2, self.height // 2))

    def get_text(self):
        return self.text_line

    def set_func(self, func):
        self.func = func

    def check_mouse_position(self, mouse_pos):
        return self.rect.x <= mouse_pos[0] < self.rect.x + self.width and \
            self.rect.y <= mouse_pos[1] < self.rect.y + self.height

    def action(self, *x):
        try:
            self.func(*x)
        except Exception as error:
            print("No function now", error)


def load_image(filename, color_key=None):
    """Функция загрузки изображения в pygame."""

    fullname = os.path.join('images', filename)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def get_max_score_row():
    """Функция получения строки с лучшим счётом."""
    rows = []
    with open('data.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            rows.append(row)
        rows = rows[1:]

    return sorted(rows, key=lambda x: -int(x[1]))[0]


def make_graph(table_name='data.csv', file_name='graph.png'):
    """Функция создания графика очков."""
    fig, ax = matplotlib.pyplot.subplots(figsize=(40, 30))

    rows = []
    with open(table_name, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for index, row in enumerate(reader):
            rows.append(row)

    rows = rows[1:]
    if len(rows) > 15:
        rows = rows[-15:]

    x = [f'{row[0]} {row[3]}' for row in rows]
    y = [int(row[1]) for row in rows]

    ax.bar(x, y, color='orange')
    ax.set_facecolor('gray')

    ax.set_xlabel('Номер игры, дата', color='white', fontsize=70)
    ax.set_ylabel('Очки', color='white', fontsize=70)

    matplotlib.pyplot.xticks(rotation=30, ha='right', color='white', fontsize=40)
    matplotlib.pyplot.yticks(color='white', fontsize=50)
    matplotlib.pyplot.grid(color='black', linestyle=':', linewidth=5)

    fig.set_facecolor('forestgreen')

    fig.savefig(f'images/{file_name}', transparent=True)


click_sound = mixer.Sound('sounds/click.mp3')
button_sound = mixer.Sound('sounds/button.mp3')

display_info = pygame.display.Info()
display_width, display_height = display_info.current_w, display_info.current_h

w_percent = display_width // 100
h_percent = display_height // 100

card_size = 225 * display_width // 1920, 315 * display_height // 1080

use_custom_cursor = True
fps = 60

# Полная колода карт
full_deck = (
    [14, 'C', 'card_40.png'], [14, 'D', 'card_27.png'], [14, 'H', 'card_01.png'], [14, 'S', 'card_14.png'],
    [13, 'C', 'card_52.png'], [13, 'D', 'card_39.png'], [13, 'H', 'card_13.png'], [13, 'S', 'card_26.png'],
    [12, 'C', 'card_51.png'], [12, 'D', 'card_38.png'], [12, 'H', 'card_12.png'], [12, 'S', 'card_25.png'],
    [11, 'C', 'card_50.png'], [11, 'D', 'card_37.png'], [11, 'H', 'card_11.png'], [11, 'S', 'card_24.png'],
    [10, 'C', 'card_49.png'], [10, 'D', 'card_36.png'], [10, 'H', 'card_10.png'], [10, 'S', 'card_23.png'],
    [9, 'C', 'card_48.png'], [9, 'D', 'card_35.png'], [9, 'H', 'card_09.png'], [9, 'S', 'card_22.png'],
    [8, 'C', 'card_47.png'], [8, 'D', 'card_34.png'], [8, 'H', 'card_08.png'], [8, 'S', 'card_21.png'],
    [7, 'C', 'card_46.png'], [7, 'D', 'card_33.png'], [7, 'H', 'card_07.png'], [7, 'S', 'card_20.png'],
    [6, 'C', 'card_45.png'], [6, 'D', 'card_32.png'], [6, 'H', 'card_06.png'], [6, 'S', 'card_19.png'],
    [5, 'C', 'card_44.png'], [5, 'D', 'card_31.png'], [5, 'H', 'card_05.png'], [5, 'S', 'card_18.png'],
    [4, 'C', 'card_43.png'], [4, 'D', 'card_30.png'], [4, 'H', 'card_04.png'], [4, 'S', 'card_17.png'],
    [3, 'C', 'card_42.png'], [3, 'D', 'card_29.png'], [3, 'H', 'card_03.png'], [3, 'S', 'card_16.png'],
    [2, 'C', 'card_41.png'], [2, 'D', 'card_28.png'], [2, 'H', 'card_02.png'], [2, 'S', 'card_15.png']
)
