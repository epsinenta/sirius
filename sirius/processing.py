""" Модули для обработки запросов """
import subprocess
import webbrowser
from threading import Thread
import pyautogui
from bs4 import BeautifulSoup
import requests
from pycbrf import ExchangeRates
import pygame
import datetime
from pydub import AudioSegment
from pydub.playback import play
from telebot import TeleBot
import pyperclip
import easygui

from Classes.input import Input
from Classes.button import Button
from utils import is_over


def play_song(name):
    """ Функция для проигрывания звуков
    :param name: Название
    :type name: str
    """
    song = AudioSegment.from_wav(f'{name}.wav')
    play(song)


class TelegramBot:
    """ Класс отправки сообщений в телеграмм """

    def __init__(self):
        """ Метод инициализации """
        with open(f'config.txt', 'r') as settings:
            lines = settings.read().split('\n')
            api_key = lines[4]
            self.bot = TeleBot(api_key)
            self.contacts = {
                'мне': 756148309,
                'даше': 919847477,
                'коту': 919847477,
            }

    def run(self, request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        text = ''
        shift = 0
        contact = ''
        for index, word in enumerate(request.split()):
            shift += len(word) + 1
            if 'напиш' in word or 'отправ' in word:
                contact = request.split()[index + 1]
                text = request[shift + len(contact):]
                break
        try:
            self.bot.send_message(self.contacts[contact], text)
            return True
        except KeyError:
            print('Такого контакта нет')


class RunProgram:
    """ Класс запуска приложения"""

    def __init__(self):
        """ Метод инициализации"""
        self.programs = ['steam', 'браузер']
        self.programs_path = {
        }
        for pair in open('apps.txt', 'r').readlines():
            pair = pair[:-1].split(' = ')
            self.programs_path[pair[0]] = pair[1]

    def run(self, request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        for program in self.programs:
            if program not in request:
                continue
            subprocess.Popen(self.programs_path[program])
        return True


class CloseProgram:
    """ Класс закрытия приложения"""

    def __init__(self):
        """ Метод инициализации"""
        self.programs = ['steam', 'браузер']
        self.programs_name = {
        }
        for pair in open('apps.txt', 'r').readlines():
            pair = pair[:-1].split(' = ')
            self.programs_name[pair[0]] = pair[1].split('/')[-1]

    def run(self, request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        for program in self.programs:
            if program in request:
                subprocess.call(["taskkill", "/F", "/IM", f"{self.programs_name[program]}"])
        return True


class Pause:
    """ Класс для ставки видео на паузу"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        settings = open(f'config.txt', 'r')
        lines = settings.read().split('\n')
        coordinates = (lines[2], lines[3])
        settings.close()
        pyautogui.click(int(coordinates[0]), int(coordinates[1]))
        return True


class UpVolume:
    """ Класс увеличения громкости"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
        return True


class DownVolume:
    """ Класс уменьшения громкости"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
        return True


class Sleep:
    """ Класс деактивации бота"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        play_song('finish')
        return False


class GoogleSearch:
    """ Класс поиска информации в гугле"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        search = ''
        shift = 0
        for word in request.split():
            shift += len(word) + 1
            if 'гугл' in word:
                search = request[shift:]
                break
        webbrowser.open(f'https://www.google.com/search?q={search}', new=2)
        return True


class ScreenShot:
    """ Класс создания скриншотов"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        pyautogui.screenshot('ScreenShots/ScreenShot.png')
        return True


class WriteNote:
    """ Класс записи информации в блокнот"""

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        text = ''
        shift = 0
        for word in request.split():
            shift += len(word) + 1
            if 'запи' in word:
                text = request[shift:]
                break
        settings = open(f'config.txt', 'r')
        number = settings.readlines()[1]
        settings.close()
        new_file = open(f"Notes/Notes{number}.txt", "w+")
        new_file.write(text)
        new_file.close()
        settings = open(f'config.txt', 'w')
        settings.write(str(int(number) + 1))
        settings.close()
        return True


class MouseMotion:
    """ Класс движения курсором по экрану """

    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        try:
            pyautogui.moveRel(5, 5, duration=0.25)
            pyautogui.moveRel(-10, -10, duration=0.25)
            pyautogui.moveRel(5, 5, duration=0.25)
        except pyautogui.FailSafeException:
            print('курсор за пределами экрана')
        return True


class Config:
    """ Класс вызова настроек бота"""

    def __init__(self):
        self.pressed = False
        self.height = 550
        self.width = 600
        self.size = (self.width, self.height)
        self.background_color = (43, 43, 43)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('VoiceAssistantConfig')
        self.y_scale = 0
        self.inputs = []
        self.name_input = None
        self.note_input = None
        self.x_click = None
        self.y_click = None
        self.bot_key = None
        self.backspace_pressed = False
        self.ctrl_pressed = False
        self.add_button = None
        self.apps_inputs = []
        self.path_inputs = []
        self.main_inputs = []
        self.slider_y = 0
        self.slider_size = 0
        self.vertical_delta = 0
        self.build(True)

    def build(self, start=False):
        f = open('config.txt', 'r')
        lines = f.readlines()
        f.close()
        f = open('apps.txt', 'r')
        list_apps = f.readlines()
        f.close()
        number = len(self.apps_inputs)
        if start:
            number = len(list_apps)
        self.add_button = Button(250, 330 + number * 50 + self.vertical_delta,
                                 100, 30, 'Добавить', self.screen)
        if not start:
            name_input = Input(350, 77 + self.vertical_delta,
                                    200, 30, (175, 177, 179), self.screen)
            name_input.pressed = self.name_input.pressed
            name_input.text = self.inputs[0].text
            self.name_input = name_input
            note_input = Input(350, 127 + self.vertical_delta,
                                    200, 30, (175, 177, 179), self.screen)
            note_input.pressed = self.note_input.pressed
            note_input.text = self.inputs[1].text
            self.note_input = note_input
            x_click = Input(350, 177 + self.vertical_delta,
                                 87.5, 30, (175, 177, 179), self.screen)
            x_click.pressed = self.x_click.pressed
            x_click.text = self.inputs[2].text
            self.x_click = x_click
            y_click = Input(462.5, 177 + self.vertical_delta,
                                 87.5, 30, (175, 177, 179), self.screen)
            y_click.pressed = self.y_click.pressed
            y_click.text = self.inputs[3].text
            self.y_click = y_click
            bot_key = Input(350, 227 + self.vertical_delta,
                                 200, 30, (175, 177, 179), self.screen)
            bot_key.pressed = self.bot_key.pressed
            bot_key.text = self.inputs[4].text
            self.bot_key = bot_key
            self.inputs = [self.name_input, self.note_input,
                           self.x_click, self.y_click, self.bot_key]
        else:
            self.name_input = Input(350, 77 + self.vertical_delta,
                                    200, 30, (175, 177, 179), self.screen)
            self.name_input.pressed = False
            self.note_input = Input(350, 127 + self.vertical_delta,
                                    200, 30, (175, 177, 179), self.screen)
            self.note_input.pressed = False
            self.x_click = Input(350, 177 + self.vertical_delta,
                                 87.5, 30, (175, 177, 179), self.screen)
            self.x_click.pressed = False
            self.y_click = Input(462.5, 177 + self.vertical_delta,
                                 87.5, 30, (175, 177, 179), self.screen)
            self.y_click.pressed = False
            self.bot_key = Input(350, 227 + self.vertical_delta,
                                 200, 30, (175, 177, 179), self.screen)
            self.bot_key.pressed = False
            self.inputs = [self.name_input, self.note_input,
                           self.x_click, self.y_click, self.bot_key]
            for i in range(len(self.inputs)):
                self.inputs[i].text = lines[i][:-1]
        self.main_inputs = [self.name_input, self.note_input,
                            self.x_click, self.y_click, self.bot_key]

        y_coordinate = 330 + self.vertical_delta
        if not start:
            for inp in self.apps_inputs:
                inp.y_coordinate = y_coordinate
                y_coordinate += 50
                self.inputs.append(inp)
            y_coordinate = 330 + self.vertical_delta
            for inp in self.path_inputs:
                inp.y_coordinate = y_coordinate
                self.inputs.append(inp)
                y_coordinate += 50
        else:
            for string in list_apps:
                string = string[:-1]
                name = string.split(' = ')[0]
                name_input = Input(78, y_coordinate, 200, 30, (175, 177, 179), self.screen)
                name_input.text = name
                self.apps_inputs.append(name_input)
                self.inputs.append(name_input)
                y_coordinate += 50
            y_coordinate = 330 + self.vertical_delta
            for string in list_apps:
                string = string[:-1]
                path = string.split(' = ')[1]
                path_input = Input(322, y_coordinate, 200, 30, (175, 177, 179), self.screen)
                path_input.text = path
                self.path_inputs.append(path_input)
                self.inputs.append(path_input)
                y_coordinate += 50

    def run(self, request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        while self.update():
            self.draw()
        with open('apps.txt', 'w') as file:
            string = ''
            for i in range(len(self.apps_inputs)):
                if self.apps_inputs[i].text and self.path_inputs[i].text:
                    string += self.apps_inputs[i].text + ' = ' + self.path_inputs[i].text + '\n'
            file.write(string)
        with open('config.txt', 'w') as f:
            string = ''
            for inp in self.inputs[:min(len(self.inputs), 5)]:
                string += inp.text + '\n'
            f.write(string)

        return True

    def draw(self):
        self.screen.fill(self.background_color)
        pygame.font.init()
        px = (334 + 50 * len(self.apps_inputs) + 50)
        self.slider_size = self.height * self.height / px
        self.vertical_delta = -self.slider_y * px / self.height
        if px > self.height:
            slider = pygame.Surface((10, self.slider_size), pygame.SRCALPHA)
            if not (self.pressed or self.slider_is_over()):
                slider.fill((60, 63, 65))
            else:
                slider.fill((70, 73, 75))
            self.screen.blit(slider, (self.width - 10, self.slider_y))
        else:
            self.slider_y = 0
            self.vertical_delta = 0
        self.build()
        font = pygame.font.SysFont(None, 40)
        render_line = font.render('Основные настройки', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                600 / 2 - render_line.get_width() / 2,
                10 + self.vertical_delta
            )
        )
        font = pygame.font.SysFont(None, 30)
        render_line = font.render('Имя:', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                50,
                80 + self.vertical_delta
            )
        )
        render_line = font.render('Следущий номер заметки:', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                50,
                131 + self.vertical_delta
            )
        )
        render_line = font.render('Координата паузы:', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                50,
                182 + self.vertical_delta
            )
        )
        render_line = font.render('ApiKey TelegramBot:', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                50,
                233 + self.vertical_delta
            )
        )
        font = pygame.font.SysFont(None, 40)
        render_line = font.render('Приложения', True, (175, 177, 179))
        self.screen.blit(
            render_line,
            (
                600 / 2 - render_line.get_width() / 2,
                283 + self.vertical_delta
            )
        )
        for widget_input in self.inputs:
            widget_input.draw()
        for widget_input in self.path_inputs:
            widget_input.draw()
        for widget_input in self.apps_inputs:
            widget_input.draw()
        x = 48
        y = 334 + self.vertical_delta
        for i in range(len(self.apps_inputs)):
            close = pygame.image.load('close.png')
            close = pygame.transform.scale(
                close, (20, 20))
            close.set_colorkey((255, 255, 255))
            self.screen.blit(close, (x + 2, y))
            folder = pygame.image.load('folder.png')
            folder = pygame.transform.scale(
                folder, (20, 20))
            folder.set_colorkey((255, 255, 255))
            self.screen.blit(folder, (x + 482, y))
            y += 50

        self.add_button.draw()
        pygame.display.flip()

    def slider_is_over(self):
        pos = pygame.mouse.get_pos()
        if self.width - 10 < pos[0] < self.width:
            return True
        return False

    def update(self):
        for inp in self.inputs:
            if inp.pressed and self.backspace_pressed:
                if inp.text:
                    inp.text = inp.text[:-1]
                    pygame.time.wait(200)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
            if event.type == pygame.MOUSEMOTION:
                if self.pressed:
                    if 0 <= self.slider_y <= self.height - self.slider_size:
                        new_pos = pygame.mouse.get_pos()
                        self.slider_y = new_pos[1] - self.slider_size / 2
                        self.slider_y = min(max(self.slider_y, 0), self.height - self.slider_size)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.slider_is_over():
                        if 0 <= self.slider_y <= self.height - self.slider_size:
                            new_pos = pygame.mouse.get_pos()
                            self.slider_y = new_pos[1] - self.slider_size / 2
                            self.pressed = True
                            self.slider_y = min(max(self.slider_y, 0),
                                                self.height - self.slider_size)
                if event.button == 4:
                    self.slider_y -= self.slider_size / 10
                    self.slider_y = min(max(self.slider_y, 0), self.height - self.slider_size)
                if event.button == 5:
                    self.slider_y += self.slider_size / 10
                    self.slider_y = min(max(self.slider_y, 0), self.height - self.slider_size)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = 48
                    y = 334 + self.vertical_delta
                    for i in range(len(self.apps_inputs)):
                        pos = pygame.mouse.get_pos()
                        if x + 2 < pos[0] < x + 22:
                            if y < pos[1] < y + 20:
                                last1 = self.apps_inputs[i]
                                last2 = self.path_inputs[i]
                                self.apps_inputs.pop(i)
                                self.path_inputs.pop(i)
                                self.inputs.remove(last1)
                                self.inputs.remove(last2)
                                self.add_button.y_coordinate -= 50
                                for inp in self.apps_inputs[i:]:
                                    inp.y_coordinate -= 50
                                for inp in self.path_inputs[i:]:
                                    inp.y_coordinate -= 50
                        y += 50
                    x = 530
                    y = 334 + self.vertical_delta
                    for inp in self.path_inputs:
                        pos = pygame.mouse.get_pos()
                        if x < pos[0] < x + 20:
                            if y < pos[1] < y + 20:
                                inp.text = easygui.fileopenbox()
                        y += 50
                    if is_over(self.add_button, pygame.mouse.get_pos()):
                        self.add_button.y_coordinate += 50
                        if len(self.apps_inputs):
                            last_input = self.apps_inputs[-1]
                            new_name_input = Input(last_input.x_coordinate,
                                                   last_input.y_coordinate + 50,
                                                   200, 30, (175, 177, 179), self.screen)
                            self.apps_inputs.append(new_name_input)
                            self.inputs.append(new_name_input)
                            last_input = self.path_inputs[-1]
                            new_path_input = Input(last_input.x_coordinate, last_input.y_coordinate,
                                                   200, 30, (175, 177, 179), self.screen)
                            new_path_input.text = ''
                            new_path_input.y_coordinate += 50
                            self.path_inputs.append(new_path_input)
                            self.inputs.append(new_path_input)
                        else:
                            new_name_input = Input(78, 330 + self.vertical_delta,
                                                   200, 30, (175, 177, 179), self.screen)
                            self.apps_inputs.append(new_name_input)
                            self.inputs.append(new_name_input)
                            new_path_input = Input(322, 330 + self.vertical_delta,
                                                   200, 30, (175, 177, 179), self.screen)
                            self.path_inputs.append(new_path_input)
                            self.inputs.append(new_path_input)
                        return True
                    for inp in self.inputs:
                        inp.pressed = False
                        if is_over(inp, pygame.mouse.get_pos()):
                            inp.pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False
                if pygame.key.name(event.key) == 'left ctrl':
                    self.ctrl_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for inp in self.inputs:
                        if inp.pressed:
                            inp.pressed = False
                            return True
                    return False
                for inp in self.inputs:
                    if inp.pressed:
                        if event.key == pygame.K_BACKSPACE:
                            self.backspace_pressed = True
                        elif pygame.key.name(event.key) == 'left ctrl':
                            self.ctrl_pressed = True
                        else:
                            if self.ctrl_pressed:
                                if event.key == pygame.K_v or event.key == pygame.K_М:
                                    inp.text += pyperclip.paste()
                            else:
                                inp.text += event.unicode
        return True


class AddToDo:
    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        text = ''
        shift = 0
        for word in request.split():
            shift += len(word) + 1
            if 'задач' in word:
                text = request[shift:]
                break
        with open('todo.txt', 'a') as f:
            f.write(text + '\n')


class ToDoList:
    @staticmethod
    def run(request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request + ":")
        with open('todo.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                print(line[:-1])


class ExcRates:
    def __init__(self):
        self.rates_name = {
            'доллар': 'USD',
            'евро': "EUR"
        }
        date = datetime.datetime.now()
        self.rates = ExchangeRates(str(date).split()[0], locale_en=True)

    def run(self, request: str = '') -> bool:
        """ Метод исполнения класса
        :param request: Текст запроса
        :type request: str:
        :return bool: True - если все прошло успешно, иначе - False
        """
        print(request)
        for name in self.rates_name.keys():
            if name in request:
                rate = str(self.rates[self.rates_name[name]]).split(', ')[4].split("('")[1].split("'")[0]
                rub, kop = rate.split('.')
                kop = int(kop) // 100
                print(f'{rub} руб. {kop} коп.')


class Process:
    """ Класс обработки запроса"""

    def __init__(self, request):
        """Метод инициализации класса
        :param request: Текст запроса
        :type request: str:
        """
        self.request = request
        self.handlers = {
            'откр': RunProgram(),
            'закр': CloseProgram(),
            'пауз': Pause(),
            'гром': UpVolume,
            'тиш': DownVolume,
            'спать': Sleep,
            'гугл': GoogleSearch,
            'скрин': ScreenShot,
            'запи': WriteNote,
            'напиш': TelegramBot(),
            'отправ': TelegramBot(),
            'двиг': MouseMotion,
            'добав': AddToDo,
            'список': ToDoList,
            'курс': ExcRates()
        }
        self.active = False

    def run(self) -> bool:
        """ Метод обработки запроса
        :return bool: True - если все прошло успешно, иначе - False
        """
        status = False
        for action in self.handlers.keys():
            if action in self.request:
                status = True
                if Thread(target=self.handlers[action].run, args=(self.request,)).start():
                    return False
            elif 'настр' in self.request:
                Thread(target=Config().run(), args=(self.request,)).start()
        if not status:
            print(f'Неизвестная команда: {self.request}')
        return True
