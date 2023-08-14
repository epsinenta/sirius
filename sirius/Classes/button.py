""" Модули для визуализации """
import pygame
from pygame import Surface
from utils import is_over

class Button:
    """ Класс кнопки """

    def __init__(self, x_coordinate: int, y_coordinate: int, width: int, height: int,
                 text: str, screen: Surface):
        """Инициализация кнопки
        :param x_coordinate: Положение кнопки на экране по оси x
        :type x_coordinate: int
        :param y_coordinate: Положение кнопки на экране по оси y
        :type y_coordinate: int
        :param width: Ширина кнопки
        :type width: int
        :param height: Высота кнопки
        :type height: int
        :param text: Текст кнопки
        :type text: str
        :param screen: Поверхность, на которой будет происходить отрисовка
        :type screen: Surface
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.color = (60, 63, 65)
        self.color_over = (40, 43, 45)
        self.outline = (60, 63, 65)
        self.text_color = (175, 177, 179)
        self.text = text
        self.screen = screen

    def draw(self):
        """ Метод отрисовки кнопки на экране """
        if is_over(self, pygame.mouse.get_pos()):
            color = self.color_over
            outline = self.outline
            if self.color == self.outline:
                outline = color
        else:
            outline = self.outline
            color = self.color

        pygame.draw.rect(self.screen, outline, (self.x_coordinate - 2,
                                                self.y_coordinate - 2,
                                                self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.screen, color, (self.x_coordinate, self.y_coordinate,
                                              self.width, self.height), 0)

        pygame.font.init()
        font = pygame.font.SysFont(None, 20)
        render_line = font.render(self.text, True, self.text_color)
        self.screen.blit(
            render_line,
            (
                self.x_coordinate + (self.width / 2 - render_line.get_width() / 2),
                self.y_coordinate + (self.height / 2 - render_line.get_height() / 2)
            )
        )
