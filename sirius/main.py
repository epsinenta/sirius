""" Модуль для многопоточности, распознования речи """
import time
from threading import Thread
import speech_recognition
from processing import Process, play_song
import datetime
import traceback


class VoiceBot:
    """ Класс бота, слушающего пользователя"""

    def __init__(self, bot_name):
        """ Метод инициализация бота
        :param bot_name: Имя, на которое бот отзывается
        :type bot_name: str
        """
        self.name = bot_name
        self.speech_recognition = speech_recognition.Recognizer()
        self.speech_recognition.pause_threshold = 0.3
        self.listening = False

    def listen(self):
        """ Метод слушания пользователя """
        try:
            with speech_recognition.Microphone() as mic:
                self.speech_recognition.adjust_for_ambient_noise(source=mic)
                audio = self.speech_recognition.listen(source=mic)
                request = self.speech_recognition.recognize_google(audio_data=audio, language='ru-RU').lower()
                self.check(request)
        except speech_recognition.UnknownValueError:
            pass


    def check(self, request):
        """ Метод проверки на то, принимает ли команды пользователя бот
        :param request: Текст запроса
        :type request: str
        """
        print(request)
        if self.name in request and not self.listening:
            self.listening = True
            play_song('start')

        if self.listening:
            process = Process(request)
            self.listening = process.run()

    def run(self):
        try:
            while True:
                self.listen()

        except:
            with open('log.txt', 'a') as f:
                f.write(f'{datetime.datetime.now()}:\n')
                f.write(f'{traceback.format_exc()}\n')


if __name__ == '__main__':
    while 1:
        try:
            settings = open(f'config.txt', 'r')
            name = settings.readlines()[0][:2]
            settings.close()
            bot = VoiceBot(name)
            bot.run()
        except:
            with open('log.txt', 'a') as f:
                f.write(f'{datetime.datetime.now()}:\n')
                f.write(f'{traceback.format_exc()}\n')
