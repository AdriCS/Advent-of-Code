#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import sys

def buildInputList(inputFile):
    with open(inputFile, 'r') as f:
        return f.read().splitlines()
        
def calcHash(inputList):
    totalTwos = 0
    totalThrees = 0

    for line in inputList:
        freqs = collections.Counter(line)
        twos = [freq for freq in freqs.values() if freq == 2]
        threes = [freq for freq in freqs.values() if freq == 3]
        
        if twos:
            totalTwos += 1
            # print("\t{0}".format(totalTwos) + str(twos))
            
        if threes:
            totalThrees += 1
            # print("\t{0}".format(totalThrees) + str(threes))
            
    return (totalTwos * totalThrees)

def findCommonLetters(inputList):
    head = inputList[0]
    # others = inputList[2:]

    for candidate in inputList:
        others = list(filter(lambda key: key != candidate, inputList))
        
        for otherCandidate in others:
            # The problem states that there are TWO boxes that differ by ONE character only.
            totalDifferentChars = sum(1 for a, b in zip(candidate, otherCandidate) if a != b)
            if totalDifferentChars == 1:
                # This doesn't work because if the differing char appears in another place of
                # otherCandidate, it will get pushed in.
                ## convert list to string
                ## commonChars = ''.join([c for c in candidate if for c in otherCandidate])
                commonChars = ""
                for i in range(0, len(candidate)):
                    if candidate[i] == otherCandidate[i]:
                        commonChars += candidate[i]
                
                print("Found candidates {0} and {1} => common part: {2}".format(candidate, otherCandidate, commonChars))
                return commonChars
    
if __name__ == "__main__":
    inputFile = sys.argv[1]
    inputList = buildInputList(inputFile)
    hash = calcHash(inputList)
    print("Hash: {0}".format(hash))
    
    common = findCommonLetters(inputList)
    print("Final result: {0}".format(common))
    