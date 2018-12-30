#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import collections
import concurrent.futures
import pstats
import regex
import sys

def readPolymer(filepath):
    with open(filepath, 'r') as f:
        return f.read()
    
def reducePolymer(polymer):
    pattern = regex.compile(r'(\p{L})(?!\1)(?i:\1)')
    polyCopy = polymer

    while True:
        match = pattern.search(polyCopy)
        if not match:
            break
        
        polyCopy = pattern.sub("", polyCopy)

    return polyCopy

def collapsePolymer(polymer):
    keys = list(collections.Counter(polymer))
    return collapse(polymer, keys)

def collapse(polymer, keys):
    visited = []
    mostReduced = sys.maxsize
    for k in keys:
        if k.lower() in visited:
            continue
            
        visited.append(k.lower())
        copy = polymer.replace(k, '')
        if k.isupper():
            copy = copy.replace(k.lower(), '')
        else:
            copy = copy.replace(k.upper(), '')
       
        reduced = reducePolymer(copy)
       
        if len(reduced) < mostReduced:
            mostReduced = len(reduced)

    return mostReduced
             
# Naive test just to play with futures
def collapsePolymerByFutures(polymer):
    futures = []
    times = list(collections.Counter(polymer))
    # // to force int division
    firstHalf = times[:len(times)//2]
    secondHalf = times[len(times)//2:]

    size = sys.maxsize
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures.append(executor.submit(collapse, polymer, firstHalf))
        futures.append(executor.submit(collapse, polymer, secondHalf))
        
        nExcepts = 0
        for fut in concurrent.futures.as_completed(futures):
            try:
                if fut.result() < size:
                    size = fut.result()
            except Exception as E:
                nExcepts += 1
                
        if nExcepts:
            print("Total exceptions: {0}".format(nExcepts))
            
    return size
    
# Naive test #2: just to play with futures
def collapseSingleKey(polymer, key):
    copy = polymer.replace(key, '')
    if key.isupper():
        copy = copy.replace(key.lower(), '')
    else:
        copy = copy.replace(key.upper(), '')
   
    return len(reducePolymer(copy))

def collapsePolymerByFuturesUnrolled(polymer):
    futures = []
    keys = list(collections.Counter(polymer))
    visited = []
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for k in keys:
            if k.lower() in visited:
                continue
                
            futures.append(executor.submit(collapseSingleKey, polymer, k))
            visited.append(k.lower())

        size = sys.maxsize
        nExcepts = 0
        for fut in concurrent.futures.as_completed(futures):
            try:
                if fut.result() < size:
                    size = fut.result()
            except Exception as E:
                nExcepts += 1
                
        if nExcepts:
            print("Total exceptions: {0}".format(nExcepts))
            
    return size

def profile(func, polymer):
    profiler = cProfile.Profile()
    profiler.enable()
    shortestPolymer = func(polymer)
    profiler.disable()
    print("** Profiling: {0}\n".format(func.__name__))
    print("Shortest collapsed polymer: {0}".format(shortestPolymer))
    ps = pstats.Stats(profiler, stream=sys.stdout)
    ps.print_stats()
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You have to pass the input filepath.")
        exit(-1)
      
    polymer = readPolymer(sys.argv[1])
    reduced = reducePolymer(polymer)
    print ("Sizes input - reduced: {0} - {1}".format(len(polymer), len(reduced)))
    
    print("\n###################################################\n")
    profile(collapsePolymer, polymer)
    
    print("\n###################################################\n")
    profile(collapsePolymerByFutures, polymer)
    
    print("\n###################################################\n")
    profile(collapsePolymerByFuturesUnrolled, polymer)

