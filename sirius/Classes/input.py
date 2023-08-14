""" Модули для визуализации поля ввода """
import pygame
from pygame import Surface

class Input:
    """ Класс поля ввода """

    def __init__(self, x_coordinate: int, y_coordinate: int, width: int, height: int,
                 outline: tuple, screen: Surface, description: str = ''):
        """Инициализация поля ввода
        :param x_coordinate: Положение поля на экране по оси x
        :type x_coordinate: int
        :param y_coordinate: Положение поля на экране по оси y
        :type y_coordinate: int
        :param width: Ширина поля ввода
        :type width: int
        :param height: Высота поля ввода
        :type height: int
        :param outline: Цвет обводки поля
        :type outline: COLOR
        :param screen: Поверхность, на которой будет происходить отрисовка
        :type screen: Surface
        :param description: Объяснение поля
        :type description: str
        """
        pygame.font.init()
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.text = ''
        self.outline = (60, 63, 65)
        self.font = pygame.font.SysFont(None,
                                        int(30))
        self.pressed = False
        self.pressed_time = 0
        self.screen = screen
        self.description = description

    def draw(self):
        """Метод отрисовки поля ввода на экране """
        if self.outline:
            pygame.draw.rect(self.screen, self.outline, (self.x_coordinate - 2,
                                                         self.y_coordinate - 2,
                                                         self.width + 4, self.height + 4),
                             0)

        color = (60, 63, 65)
        pygame.draw.rect(self.screen, color, (self.x_coordinate, self.y_coordinate,
                                              self.width, self.height), 0)

        result = ''
        if self.text != "":
            result = self.text
            render_line = self.font.render(result, True, (175, 177, 179))
            while render_line.get_width() > self.width * 0.9:
                result = f'...{result[4:]}'
                render_line = self.font.render(result, True, (175, 177, 179))

        elif not self.pressed and self.text == '':
            result = self.description

        if self.pressed:
            self.pressed_time += 1
            if self.pressed_time % 80 < 40:
                result += '|'
            else:
                result += ' '
        if self.text != '' or self.pressed:
            color = (175, 177, 179)
        else:
            color = (175, 177, 179)
        render_line = self.font.render(result, True, color)
        self.screen.blit(
            render_line,
            (
                self.x_coordinate + (self.width / 2 - render_line.get_width() / 2),
                self.y_coordinate + (self.height / 2 - render_line.get_height() / 2)
            )
        )
