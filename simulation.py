#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211 Assignment 5 by Diandra Vega"""


import csv
import argparse
import os
import random


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--file", help="Use a CSV file for script processing.")
PARSER.add_argument("--servers", help="Number of servers in load balancer.")
ARGS = PARSER.parse_args()


class Queue(object):
    """Class for abstract data structure for queues. Used from
    'Problem Solving with Algorithms and Data Structures, Release 3.0'
    by Brad Miller, David Ranum."""
    def __init__(self):
        """Queue class constructor."""
        self.items = []

    def is_empty(self):
        """Checks if queue list is empty."""
        return self.items == []

    def enqueue(self, item):
        """Inserts item into rear of the queue."""
        self.items.insert(0, item)

    def dequeue(self):
        """Removes next/first item from the queue."""
        return self.items.pop()

    def size(self):
        """Returns size of a queue list."""
        return len(self.items)


class Server(object):
    """Processes server network request queue.

    Attributes:
        current_task (obj): Should be object from Request class.
        time_remaining (int): Time remaining to process request.
    """
    def __init__(self):
        """Constructor for Server class."""
        self.current_task = None
        self.time_remaining = 0


    def tick(self):
        """Calculates time remaining for server to finish processing queue."""
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None


    def busy(self):
        """Checks if server is already processing a request."""
        if self.current_task != None:
            return True
        else:
            return False


    def start_next(self, new_task):
        """Begins next processing task in the queue."""
        self.current_task = new_task
        self.time_remaining = new_task.get_req_time()


class Request(object):
    """Calculates how long a network request takes to be processed.

    Attributes:
        timestamp (int): Time request has began to be processed.
        req_time (int): Amount of time it takes a request to be processed.
    """
    def __init__(self, time, ptime):
        """Constructor for Request class."""
        self.timestamp = time
        self.req_time = ptime


    def get_stamp(self):
        """Gets time a request begins to be processed at."""
        return self.timestamp


    def get_req_time(self):
        """Gets the length of processing time."""
        return self.req_time


    def wait_time(self, current_time):
        """Calculates how long it takes to wait for a request to finish."""
        return current_time - self.timestamp


def simulateOneServer(filename):
    """Iterates through a CSV file of network requests and adds each item
    into a queue. Afterwards, each item in the queue gets processed
    then the function calculates how long the average wait time for requests
    to be processed is on a single server.

    ARGS:
        filename (str): Name of file.

    RETURNS:
        float: Returns a floating number of the average wait time in seconds.

    EXAMPLES:
        >>> simulateOneServer('requests.csv')
        Average wait time for requests on one server is 2502.0 seconds.
    """
    open_file = open(filename, 'r')
    data = csv.reader(open_file)
    waittimes = []
    queue = Queue()
    server = Server()

    for row in data:
        requests = Request(int(row[0]), int(row[2]))
        queue.enqueue(requests)

        if server.busy() is not True and queue.is_empty() is not True:
            task = queue.dequeue()
            waittimes.append(task.wait_time(int(row[0])))
            server.start_next(task)

        server.tick()

    latency = float(sum(waittimes) / len(waittimes))
    results = "Average wait time for requests on one server is {}" \
              " seconds.".format(latency)
    return results


def simulateManyServers(filename, hosts=None):
    """Iterates through a CSV file of network requests and adds each item
    into a queue. Afterwards, each item in the queue gets processed
    then the function calculates how long the average wait time for requests
    to be processed is on a load balancer of servers.

    ARGS:
        filename (str): Name of file.
        hosts (int): Number of hosts on the load balancer.

    RETURNS:
        float: Returns a floating number of the average wait time in seconds.

    EXAMPLES:
        >>> simulateManyServers('requests.csv', 4)
        Average wait time for requests on load balancer with 4 servers
        is 1495.0 seconds."""
    open_file = open(filename, 'r')
    data = csv.reader(open_file)
    waittimes = []
    servers = {}
    queue = Queue()
    server_keys = []

    for host in range(1, int(hosts) + 1):
        servers["server{0}".format(host)] = Server()

    for key, val in servers.iteritems():
        server_keys.append(key)

    for row in data:
        requests = Request(int(row[0]), int(row[2]))
        queue.enqueue(requests)

        serv = random.choice(server_keys)

        if not servers[serv].busy() and not queue.is_empty():
            task = queue.dequeue()
            waittimes.append(task.wait_time(int(row[0])))
            servers[serv].start_next(task)
        else:
            newkey = random.choice(server_keys)

            if not servers[newkey].busy() and not queue.is_empty():
                task = queue.dequeue()
                waittimes.append(task.wait_time(int(row[0])))
                servers[newkey].start_next(task)

            servers[newkey].tick()

        servers[serv].tick()
    latency = float(sum(waittimes) / len(waittimes))

    results = "Average wait time for requests on load balancer with {}" \
              " servers is {} seconds.".format(hosts, latency)
    return results

def main(filename=ARGS.file, hosts=None):
    """Main function of this program. It will run one of two simulations
    based on parameters passed into arguments. If no int is given for
    the number of servers on load balancer, then the program will
    simulate the average request wait time on one server. If an int
    is given for the number of servers on load balancer, then the
    program will simulate the average request wait time going through
    a load balancer.

    ARGS:
        filename (str): Name of CSV file.
        hosts (int, optional): Number of hosts on load balancer.

    RETURNS:
        string: Returns a string that includes average wait time
            for requests to complete.

    EXAMPLES:
        >>> main('requests.csv', 20)
        Average wait time for requests on load balancer with 20 servers
        is 1290.0 seconds.
    """

    if hosts is None:
        print simulateOneServer(filename)
    else:
        print simulateManyServers(filename, hosts)

    return


if __name__ == '__main__':
    if ARGS.file and ARGS.servers:
        main(ARGS.file, ARGS.servers)
    elif ARGS.file:
        main(ARGS.file)
    else:
        print "No file specified. Please see 'python simulation.py' -h" + \
              " for help."
        os.system('python simulation.py -h')
        exit()
