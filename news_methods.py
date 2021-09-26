#!/usr/bin/python3.7
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import random
import pymongo
from pymongo import MongoClient
import time
import pyowm
import math
import datetime
from datetime import datetime, timedelta
import urllib.request
import bs4
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
import datetime

from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

cluster = MongoClient("mongodb+srv://BeryWolf:123@cluster0-onin2.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["school_data"]
collection = db["log_pas"]

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def get_news(html):
    soup = BeautifulSoup(html)
    i = 1
    mas = []*5
    for h in soup.find_all("h2", class_="mg-card__title"):
        if i <= 5:
            mas.append(h.text)
        i += 1
    return mas

def get_course(html):
    output = ""
    soup = BeautifulSoup(html)
    div = soup.find("div", class_="finance-exchange-rate__data")
    for course in div.find_all("div", class_="finance-exchange-rate__value"):
        output += course.text
    return output


def post_log_pas(login_pass, id):
    login_pass = login_pass.split()
    login = login_pass[0]
    password = login_pass[1]
    output = "Успешно"
    try:
        post = {"_id": id, "login": login, "pass": password, "crutch": "crutch"}
        collection.insert_one(post)
        return output
    except pymongo.errors.DuplicateKeyError:
        output = "Ваш id уже зарегистрирован"
        return output


def update_log_pas(login, password, id):
    output = "Успешно"
    collection.update_one({"_id": id}, {"$set": {"login": login}})
    collection.update_one({"_id": id}, {"$set": {"pass": password}})
    return output


def get_page(url):
    s = requests.Session()
    s.get(url.rsplit('/',maxsplit=1)[0])
    r = s.get(url)
    return r.text

def get_name(id):
    s = requests.Session()
    link = "https://vk.com/id"+str(id)
    r = requests.get(link, cookies=s.cookies, verify=False)

    soup = BeautifulSoup(r.text)
    name = soup.find("h2", class_="op_header")
    return name.text


def get_lessons(login, password):
    s = requests.Session()
    data = {
        "login": login,
        "password": password
    }
    r = s.post('https://login.school.mosreg.ru/?ReturnUrl=https%3a%2f%2fschools.school.mosreg.ru%2fmarks.aspx%3fschool%3d50637%26tab%3dweek', data=data)
    r = requests.get('https://schools.school.mosreg.ru/schedules/view.aspx?school=50637&group=1703835869914216728', cookies=s.cookies, verify=False)
    soup = BeautifulSoup(r.text)
    print(soup)
    try:
        div = soup.find("div", class_="page-wrapper")
        div2 = div.find("div", id="content")
        table = div2.find("table", class_="scheduleWeekEditorParent")
        tr = table.find_all("tr", class_="wWeek")

        date = "d" + datetime.datetime.today().strftime("%Y%m%d") +"_"
        # date ="d20200320_"
        output = ""
        for i in range(8):
            teach_time_place = ""
            date1 = date + str(i + 1)
            td = tr[i].find("td", id=date + str(i + 1))
            for a in tr[i].find("td", id=date + str(i + 1)):
                a = td.find("a", class_="aL")
                lesson = a.text
                output += "Урок: " + lesson + "\n"

            for p in tr[i].find("td", id=date + str(i + 1)):
                teach_time_place = td.find_all("p")
                teacher = teach_time_place[0]
                time = teach_time_place[1]
                place = teach_time_place[2]
                output += "Препадователь: " + teacher.text + "\n"
                output += "Время Н/К: " + time.text + "\n"
                output += "Кабинет: " + place.text + "\n"
            output += "\n"
        if output.replace("\n", "") == "":
            output = "Расписания нету" + "\n" + "Лежим, чилимся 😎"
            return output
        else:
            return output


    except AttributeError:
        pass
        output = "Расписания нету" + "\n" + "Лежим, чилимся 😎"
        return output