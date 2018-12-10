#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import datetime
import sys

class Guard():
    _id = -1
    _minutes = None
    _lastMinuteGoingToSleep = -1
    _totalMinutesAsleep = 0
    
    def __init__(self, id):
        self._id = id
        self._minutes = [0 for i in range(0, 60)]
        assert len(self._minutes) == 60
        
    @property
    def id(self):
        return self._id
        
    @property
    def totalMinutesAsleep(self):
        return self._totalMinutesAsleep

    def wakesUp(self, minuteAwake):
        # print("wakes up - last {0} - until {1}".format(self._lastMinuteGoingToSleep, minuteAwake))
        for i in range(self._lastMinuteGoingToSleep + 1, minuteAwake):
            self._minutes[i] += 1
            self._totalMinutesAsleep += 1

        self._lastMinuteGoingToSleep = -1
        
        # print("wakesUp total {0}".format(self._totalMinutesAsleep))
        # print(self._minutes)
        
    def fallsAsleep(self, minute):
        self._minutes[minute] += 1
        self._totalMinutesAsleep += 1
        self._lastMinuteGoingToSleep = minute
        
        # print("fallsAsleep in minute {0} - total {1}".format(minute, self._totalMinutesAsleep))
        # print(self._minutes)
        
    def mostSleepedMinute(self):
        try:
            print(self._minutes)
            return self._minutes.index(max(self._minutes))
        except ValueError:
            return None

class GuardCollection():
   _guards = None
   _guardMostAsleep = -1
   
   def __init__(self, guards):
        self._guards = guards
        
        
def sortGuardsLogs(input):
    dict = {}
    with open(input, 'r') as f:
        for line in f:
            date = line[1:line.find("]")];
            # On Windows, the minimum accepted year is 1970 (in case you see an error here)
            tstamp = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp()
            dict[tstamp] = line[line.find("]") + 1:]
            # print("Date is {0}".format(date))
            # print(tstamp)
            # print(dict[tstamp])
        
    return collections.OrderedDict(sorted(dict.items()))

# Having a timestamp, for example: 111111111112 (15:00:01)
# and doing '111111111112 - 1' -> 15:00:00 !!!
def buildGuards(sortedLogs):
    guards = {}
    lastGuardOnDuty = -1
    for tstamp, log in sortedLogs.items():
        if "begins shift" in log:
            id = int(log[log.find("#") + 1:log.find(" ", log.find("#"))])
            # print("id is {0}".format(id))
            if id not in guards:
                guards[id] = Guard(id)
                
            lastGuardOnDuty = id
        elif "falls asleep" in log:
            min = datetime.datetime.fromtimestamp(tstamp).minute
            # print(min)
            guards[lastGuardOnDuty].fallsAsleep(min)
        elif "wakes up" in log:
            lastMinuteAsleep = datetime.datetime.fromtimestamp(tstamp).minute
            # print(lastMinuteAsleep)
            guards[lastGuardOnDuty].wakesUp(lastMinuteAsleep)
            
    return guards

def parseInputFile(input):
    sortedLogs = sortGuardsLogs(input)
    return buildGuards(sortedLogs)
    
if __name__ == __name__:
    guards = parseInputFile(sys.argv[1])
    guardMostAsleep = -1
    previousMostSleepedMinutes = 0
    
    for k, g in guards.items():
        if g.totalMinutesAsleep > previousMostSleepedMinutes:
            previousMostSleepedMinutes = g.totalMinutesAsleep
            guardMostAsleep = g.id
            
    print("guard id: {0} - mins: {1} - most sleepws minute: {2}".format(guardMostAsleep, guards[guardMostAsleep].totalMinutesAsleep, guards[guardMostAsleep].mostSleepedMinute()))