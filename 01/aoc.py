#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def buildFreqList(inputFile):
    freqList = []
    with open(inputFile, "r") as f:
        for line in f:
            try:
                freqList.append(int(line))
            except:
                print("Line {0} does not form a number".format(line))
                
    return freqList
    
    
def calcFreq(baseFreq, freqList):
    endFreq = baseFreq
    endFreq =+ sum(freqList)
    return endFreq

def findFirstRepeated(baseFreq, freqList):
    currentFreq = baseFreq
    visitedFrequencies = [currentFreq]
    
    while True:
        for freq in freqList:
            currentFreq += freq
            if currentFreq in visitedFrequencies:
                return currentFreq
            
            visitedFrequencies.append(currentFreq)
                
                
if __name__ == "__main__":
    baseFreq = 0
    inputFile = sys.argv[1]
    freqList = buildFreqList(inputFile)
    resultFreq = calcFreq(baseFreq, freqList)
    print("The resulting frequency is {0}".format(resultFreq))
    repeatedFreq = findFirstRepeated(baseFreq, freqList)
    print("The first repeated frequency is {0}".format(repeatedFreq))