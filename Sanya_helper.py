import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from selenium import webdriver
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import pymongo
from pymongo import MongoClient
import webbrowser
from pyowm import OWM
from pyowm.commons.enums import SubscriptionTypeEnum
import datetime
from pyowm.utils.measurables import kelvin_to_celsius
from news_methods import *
from tkinter import *
from PIL import ImageTk,Image
# from main import window

def start(window, text):
    config = {
        'subscription_type': SubscriptionTypeEnum.FREE,
        'language': 'ru',
        'connection': {
            'use_ssl': True,
            'verify_ssl_certs': True,
            'use_proxy': False,
            'timeout_secs': 5
        },
        'proxies': {
            'http': 'http://user:pass@host:port',
            'https': 'socks5://user:pass@host:port'
        }
    }

    opts = {
        "alias": ("саня", "саша", "александр", "сань", "алекс"),
        "tbr": ("скажи", "расскажи"),
    }

    cmds = {
        "tell": ('отправь сообщение', "напиши", "ответь", "напиши сообщение"),
        "record": ('запиши', "создай заметку", "запломни"),
        "web": ("открой", ""),
        "surf": ("найди в интернете", ""),
        "end": ("спасибо", "спасибо большое", "спасибо вам большое"),
        "add": ("добавь пользователя", ""),
        "weather": ("погода на сегодня", "какая сейчас погода на улице", "погода"),
        "news": ("новости", "свежие новости"),
    }

    web = {
        "википедию": "https://ru.wikipedia.org/wiki/Заглавная_страница",
        "вконтакте": "https://vk.com/id321732462",
        "youtube": "https://www.youtube.com/",
        "twitch": "https://www.twitch.tv/?no-reload=true",
        "браузер": "https://yandex.ru"
    }

    login, password = "89692812234", "VFRcbv70"
    vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()

    cluster = MongoClient("mongodb+srv://BeryWolf:123@cluster0-onin2.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = cluster["helper"]
    collection = db["vk_id"]

    owm = OWM("eb49772597d537e373cd2a9027b7b35d", config=config)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Moscow, RU')
    w = observation.weather

    mas = [] * 3

    def check():
        # print("$$$", text.get("1.0", END).split("\n"))
        if len(text.get("1.0", END).split("\n")) - 1 == 2:
            text.delete("1.0", END)


    def speak(what):
        print("[log] " + what)
        check()
        text.insert(END, "\n[log] " + what)
        window.update()
        engine.say(what)
        engine.runAndWait()
        engine.stop()

    def callback(recognizer, audio):
        try:
            voice = recognizer.recognize_google(audio, language="ru-Ru").lower()
            print("[log] Расспознано: " + voice)
            check()
            text.insert(END, "\n[log] " + voice)
            window.update()
            if voice.startswith(opts["alias"]):
                cmd = voice
                id = 0000
                site = "none"
                for x in opts["alias"]:
                    cmd = cmd.replace(x, "").strip()
                for x in opts["tbr"]:
                    cmd = cmd.replace(x, "").strip()
                y = cmd.split()
                if y[0] == "напиши" or y[0] == "отправь":
                    cmd = cmd.split()
                    if y[1] == "сообщение":
                        name = y[2]
                        cmd = cmd[0] + cmd[1]
                    else:
                        name = y[1]
                        cmd = cmd[0]
                    try:
                        results = collection.find({"name": name})
                        for result in results:
                            id = result["_id"]
                        window.update()
                        print(name, id)
                    except TypeError:
                        print("Некорректный формат данных...")
                        check()
                        text.insert(END, "\n[log] " + "Некорректный формат данных...")
                        window.update()
                elif y[0] == "открой":
                    site = y[1]
                    cmd = y[0]
                # распознаем и выполняем команду
                cmd = recognize_cmd(cmd)
                execute_cmd(cmd, id, site)  #

        except sr.UnknownValueError:
            print("[log] Непонял...")
            check()
            text.insert(END, "\n[log] " + "Непонял...")
            window.update()

        except sr.RequestError as e:
            print("[log] Отсутствует интернет соединение")
            check()
            text.insert(END, "\n[log] " + "Отсутствует интернет соединение")
            window.update()

    def recognize_cmd(cmd):
        key = "no_find"
        try:
            for x in cmds:
                for i in range(len(cmds[x])):
                    if cmds[x][i] == cmd:
                        key = x
        except UnboundLocalError as e:
            print("[log] Неизвестная комманда")
            check()
            text.insert(END, "\n[log] " + "Неизвестная комманда")
            window.update()
            key = "no_find"

        return key

    def execute_cmd(cmd, user_id, site):

        if cmd == "tell":
            speak("Записываю")
            text.insert(END, "\n[log] " + "Записываю")
            window.update()
            with sr.Microphone(device_index=1) as source:
                audio = r.listen(source)
            query = r.recognize_google(audio, language="ru-Ru")
            if id != 0:
                vk_session.method('messages.send',
                                  {'user_id': user_id, 'message': query.lower(), 'random_id': 0})
                speak("Отправил " + query.lower())
                text.insert(END, "\n[log] " + "Отправил " + query.lower())
                window.update()
            else:
                speak("Пользователя с таким именем не найдено")
                # text.insert(END, "\n[log] " + "Пользователя с таким именем не найдено")
                window.update()

        elif cmd == "end":
            speak("Всегда пожалуйста")
            exit(0)

        elif cmd == "surf":
            window.update()
            speak("Что вы хотите найти в интернете?")
            # text.insert(END, "\n[log] " + "Что вы хотите найти в интернете?")
            window.update()
            # time.sleep(1)
            with sr.Microphone(device_index=1) as source:
                audio = r.listen(source)
            query = r.recognize_google(audio, language="ru-Ru")
            driver = webdriver.Firefox(executable_path=r"C:\\Users\\User\\Desktop\\geckodriver\\geckodriver.exe")
            driver.get("https://yandex.ru/")
            driver.find_element_by_id("text").send_keys(query)
            driver.find_element_by_xpath(
                "//button[@class='button mini-suggest__button button_theme_websearch button_size_ws-head i-bem button_js_inited']").click()
            speak("Вот что я нашел по запросу " + query)
            window.update()


        elif cmd == "add":
            window.update()
            speak("Продиктуйте его id и имя")
            window.update()
            time.sleep(1)
            with sr.Microphone(device_index=1) as source:
                audio = r.listen(source)
            query = r.recognize_google(audio, language="ru-Ru")
            query = query.split()
            vk_id = query[0]
            vk_name = query[1].lower()
            # print(query)
            collection.insert_one({"_id": int(vk_id), "name": vk_name})
            window.update()
            print("[log] Пользователь добавлен успешно")
            text.insert(END, "\n[log] " + "Пользователь добавлен успешно")
            window.update()

        elif cmd == "web":
            webbrowser.open(web[site], new=2)

        elif cmd == "scr":
            window.update()
            speak("ааааааа")
            window.update()

        elif cmd == "news":

            window.update()
            mas = get_news(get_html("https://yandex.ru/news"))
            for i in range(len(mas)):
                window.update()
                speak(mas[i])


        elif cmd == "weather":
            ans = "В Подольске сейчас " + w.detailed_status + ", " + str(
                round(w.temperature('celsius')["temp"])) + " градусов, ветер " + str(
                w.wind()["speed"]) + " метров в секунду"
            window.update()
            speak(ans)
            # text.insert(END, "\n[log] " + ans)
            window.update()

        elif cmd == "record":
            window.update()
            speak("Записываю")
            text.insert(END, "\n[log] " + "Записываю")
            window.update()
            with sr.Microphone(device_index=1) as source:
                audio = r.listen(source)
            query = r.recognize_google(audio, language="ru-Ru")
            file = open("C://Users//User//Desktop//Заметки.txt", "a")
            now = datetime.datetime.today()
            file.write("\n" + str(now.date()) + " " + (now.strftime("%H:%M:%S")) + "\n" + query + "\n" + ".")
            time.sleep(1)
            window.update()
            speak("Заметка была создана")
            text.insert(END, "\n[log] " + "Заметка была создана")
            window.update()
        else:
            window.update()
            speak("Я тебя не понял, повтори")
            text.insert(END, "\n[log] " + "Я тебя не понял, повтори")
            window.update()

    # запуск

    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[5].id)

    speak("Да-Да")
    window.update()
    time.sleep(2)





    while True:
        window.update()
        with m as source:
            audio = r.listen(source)
        callback(r, audio)
        # window.update()