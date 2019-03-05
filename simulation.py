#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment 5 by Diandra Vega"""


import csv
import argparse
import os


req_url = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--file", help="Use a CSV file for script processing.")
PARSER.add_argument("--servers", help="Number of servers in load balancer.")
ARGS = PARSER.parse_args()


class Queue:
    """Docstring"""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server:
    """Docstring 1"""
    def __init__(self):
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
        self.time_remaining = new_task.get_req_time()


class Request:
    """Docstring 2"""
    def __init__(self, time, ptime):
        self.timestamp = time
        self.req_time = ptime


    def get_stamp(self):
        return self.timestamp


    def get_req_time(self):
        return self.req_time


    def wait_time(self, current_time):
        return current_time - self.timestamp


def main(filename='requests.csv'):
    """Docstring 3"""
    open_file = open(filename, 'r')
    data = csv.reader(open_file)
    queue = Queue()
    server = Server()

    def simulateOneServer(filename=data):
        """Docstring"""
        waittimes = []

        for row in filename:
            requests = Request(int(row[0]), int(row[2]))
            queue.enqueue(requests)

            if server.busy() is not True and queue.is_empty() is not True:
                task = queue.dequeue()
                waittimes.append(task.wait_time(int(row[0])))
                server.start_next(task)

            server.tick()

        latency = sum(waittimes) / len(waittimes)

        return latency


    def simulateManyServers(filename=data, hosts=None):
        """Docstring"""
        ## Implement with round robin? ##
        waittimes = []
        hostlist = list(range(1, hosts + 1))

        for row in filename:
            requests = Request(int(row[0]), int(row[2]))
            queue.enqueue(requests)

            if server.busy() is not True and queue.is_empty() is not True:
                task = queue.dequeue()
                waittimes.append(task.wait_time(int(row[0])))
                server.start_next(task)

            server.tick()

    #    latency = sum(waittimes) / len(waittimes)
        return hostlist


    print simulateOneServer()
    print simulateManyServers(data, 4)

    return


if __name__ == '__main__':
    main('requests.csv')
#    if ARGS.file:
#        main(ARGS.file)
#    else:
#        print "No file specified. Please see 'python simulation.py' -h" + \
#              " for help."
#        os.system('python simulation.py -h')
#        print "Exiting . . ."
#        exit()