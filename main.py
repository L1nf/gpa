#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/20  14:43
# @Author  : L1nf
# @FileName: main.py
import requests
from bs4 import BeautifulSoup

from format_page import Schedule, Grades
from gpa import GPA

URL = ''  # 教务网址
stu_id = ''  # 学号
pwd = ''  # 密码
academic_year = '2022-2023'  # 学年 e.g. 2022-2023
semester = '1'  # 学期 e.g. 1

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Referer": "http://124.160.107.91:6379/xs_main.aspx?xh=" + stu_id,
    "Host": "124.160.107.91:6379",
    "Upgrade-Insecure-Requests": "1",
}
session = requests.session()


def menu():
    print('========================\n'
          '1: schedule\n'
          '2: grades\n'
          '3: gpa\n'
          'q: quit')
    options = input('Please enter the options:')
    return options


def get_field(url, field):
    page = BeautifulSoup(session.get(url, headers=header).text, 'lxml')
    view_state = page.find('input', attrs={'name': field})['value']
    return view_state


def login():
    view_state = get_field(URL, '__VIEWSTATE')
    event_validation = get_field(URL, '__EVENTVALIDATION')
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    header.update(cookies)
    global stu_id, pwd
    if stu_id == '':
        stu_id = input("Please input your stu_id:")
    if pwd == '':
        pwd = input("Please input your pwd:")
    data = {
        "__VIEWSTATE": view_state,
        "__EVENTVALIDATION": event_validation,
        "TextBox1": stu_id,
        "TextBox2": pwd,
        "RadioButtonList1": "%D1%A7%C9%FA",
        "Button1": "",
    }

    response = session.post(url=URL, data=data, headers=header).text
    if check_login(response) == 1:
        stu_name = BeautifulSoup(response, 'lxml').find('span', attrs={'id': 'xhxm'}).text[0:-2]
        data.update({'stu_name': stu_name})
        return data
    else:
        print(check_login(response))
        print("Try again!")
        exit()


def check_login(html):
    script = BeautifulSoup(html, 'html.parser').find_all('script')[0].text
    if "用户名不存在" in script:
        return "stu_id not exist!"
    elif "密码错误" in script:
        return "Wrong pwd!"
    elif "用户名不能为空！！" in script:
        return "stu_id can't be empty!"
    elif "密码不能为空！！" in script:
        return "pwd can't be empty!"
    else:
        print("Login successfully!")
        return 1


def get_schedule_page(data):
    url = URL + "/xskbcx.aspx?xh=" + stu_id + "&xm=" + data.get('stu_name') + "&gnmkdm=N121603"
    schedule_page = session.post(url, headers=header).text
    soup = BeautifulSoup(schedule_page, 'lxml')
    return soup


def get_grades_page(data):
    url = URL + 'xscjcx_dq.aspx?xh=' + stu_id + '&xm=' + data.get('stu_name') + '&gnmkdm=N121605'
    view_state = get_field(url, '__VIEWSTATE')
    event_validation = get_field(url, '__EVENTVALIDATION')
    global academic_year, semester
    if academic_year == '':
        academic_year = input("Please input academic year:")
    if semester == '':
        semester = input("Please input semester:")

    data.update({'__VIEWSTATE': view_state})
    data.update({'__EVENTVALIDATION': event_validation})
    data.update({'ddlxn': academic_year})
    data.update({'ddlxq': semester})
    data.update({'btnCx': '+%B2%E9++%D1%AF+'})

    grades_page = session.post(url, data=data, headers=header).text
    soup = BeautifulSoup(grades_page, 'lxml')
    return soup


def main():
    global URL
    if URL == '':
        URL = input("Please input url:")
    data = login()
    options = menu()
    while options != 'q':
        if options == '1':
            schedule_page = get_schedule_page(data)
            Schedule(schedule_page).output()
        elif options == '2':
            gredes_page = get_grades_page(data)
            Grades(gredes_page).output()
        elif options == '3':
            gredes_page = get_grades_page(data)
            grade = Grades(gredes_page).resolve_page()
            GPA(grade).output()
        options = menu()


if __name__ == '__main__':
    main()
