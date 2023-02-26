#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/1/14  12:35
# @Author  : L1nf
# @FileName: gpa.py
def is_chinese(string):
    if '\u4e00' <= string <= '\u9fff':
        return True
    return False


def str_to_num(string):
    if string == '优秀':
        return 5
    elif string == '良好':
        return 4
    elif string == '中等':
        return 3
    elif string == '及格':
        return 2
    else:
        return 0


def num_to_num(number):
    number = int(number)
    if 95 <= number:
        return 5
    elif 60 <= number:
        return 1.5 + (number - 60) / 10
    else:
        return 0


class GPA:
    grades_credits = []

    def __init__(self, grades):
        self.grades_credits = [grades[i][1:] for i in range(len(grades))]
        self.format_list()

    def format_list(self):
        for course in self.grades_credits:
            course[0] = float(course[0])
            if is_chinese(course[1]):
                course[1] = str_to_num(course[1])
            else:
                course[1] = num_to_num(course[1])

    def sum_grades_credits(self):
        num = 0
        for course in self.grades_credits:
            num += course[0] * course[1]
        return num

    def sum_credits(self):
        credit = 0
        for course in self.grades_credits:
            credit += course[0]
        return credit

    def output(self):
        print(self.sum_grades_credits() / self.sum_credits())
