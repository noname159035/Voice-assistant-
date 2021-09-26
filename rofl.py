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


def speak(what):
    print("[log] " + what)
    engine.say(what)
    engine.runAndWait()
    engine.stop()

r = sr.Recognizer()
m = sr.Microphone(device_index=1)
engine = pyttsx3.init()

voices = engine.getProperty("voices")

# for voice in voices:
#     print(voice, voice.id)
#     engine.setProperty('voice', voice.id)
#     engine.say("Hello World!")
#     engine.runAndWait()
#     engine.stop()

engine.setProperty("voice", voices[5].id)

speak("Да-Да")

print(voices)

time.sleep(5)

speak("Сегодня в Подольске минус тринадцать градусов, Облалчно с проясненипями, ветер 2 метра в секунду, вечером  будет минус четырнадцать метров в секунду")

time.sleep(4)

speak("Соратник Навального Волков объявлен в межгосударственный розыск")
speak("В России впервые с 17 октября выявили менее 15 тыс. заразившихся коронавирусом")
speak("Разработку сверхтяжелой ракеты «Енисей» для полетов к Луне приостановили")


time.sleep(4)

speak("Рад стараться")



exit(0)

