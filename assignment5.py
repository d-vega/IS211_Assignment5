#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment 5 by Diandra Vega"""


import random


req_url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
req_file = open('requests.csv', 'r')


class Server:
    """Docstring 1"""
    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0


    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None


    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False


    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate


class Request:
    """Docstring 2"""
    def __init__(self, time):
        self.timestamp = time
#        self.pages = random.randrange(1, 21)     # Don't need this piece?


    def get_stamp(self):
        return self.timestamp


#    def get_pages(self):
#        return self.pages


    def wait_time(self, current_time):
        return current_time - self.timestamp


def main():
    """Docstring 3"""
    return


if __name__ == '__main__':
    main()