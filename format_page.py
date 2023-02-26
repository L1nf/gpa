#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/20  14:50
# @Author  : L1nf
# @FileName: format_page.py
from abc import ABCMeta, abstractmethod

from prettytable import PrettyTable


class Page(metaclass=ABCMeta):
    soup = None
    table = []

    def __init__(self, page):
        self.soup = page
        self.table.clear()
        time = []
        for option in self.soup.findAll('option'):
            if option.get('selected') == 'selected':
                time.append(option.get('value'))
        print(time[0] + '学年，第' + time[1] + '学期:')

    @abstractmethod
    def resolve_page(self):
        pass

    @abstractmethod
    def output(self):
        pass


class Schedule(Page):
    def resolve_page(self):
        classes = []
        rows = self.soup.findAll('tr')[4:-1]
        for row in rows:
            columns = row.findAll('td')
            for column in columns:
                if column.get('align') == 'center' and column.text != '\xa0':
                    classes.append(str(column))
        for i in range(len(classes)):
            index = classes[i].find('>') + 1
            self.table.append(classes[i][index:-5].split('<br/>')[0:4])

    def output(self):
        self.resolve_page()
        table = PrettyTable()
        table.field_names = ['课程名', '时间', '老师', '教室']
        table.add_rows(self.table)
        table.align[1] = 'l'
        print(table)


class Grades(Page):
    def resolve_page(self):
        rows = self.soup.findAll('tr')[4:]
        for row in rows:
            columns = row.findAll('td')
            grade = []
            num = 0
            for column in columns:
                if num == 3 or num == 6 or num == 7:
                    grade.append(str(column)[4:-5])
                num += 1
            self.table.append(grade)
        return self.table

    def output(self):
        self.resolve_page()
        table = PrettyTable()
        table.field_names = ['课程名', '学分', '成绩']
        table.add_rows(self.table)
        table.align[1] = 'l'
        print(table)
