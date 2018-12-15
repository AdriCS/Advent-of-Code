#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import sys

class Rectangle():
    _id = "-1"
    _topLeft = ()
    _width = 0
    _height = 0

    def __init__(self, id = "None", tl = (0,0), w = 0, h = 0):
        self._id = id
        self._topLeft = tl
        self._width = w
        self._height = h
        
    def __eq__(self, other):
        return self.id == other.id
        
    def __str__(self):
        toret = "#"
        toret += str(self.id)
        toret += " @ ("
        toret += str(self.topLeft[0])
        toret += ","
        toret += str(self.topLeft[1])
        toret += ") ("
        toret += str(self.bottomRight[0])
        toret += ","
        toret += str(self.bottomRight[1])
        toret += ") : "
        toret += str(self.width)
        toret += "x"
        toret += str(self.height)
        toret += " = "
        toret += str(self.area())
        
        return toret
    
    @property
    def id(self):
        return self._id
        
    @property    
    def topLeft(self):
        return self._topLeft
    
    @property
    def bottomRight(self):
        return (self.topLeft[0] + self.width - 1,
                self.topLeft[1] + self.height - 1)

    @property
    def topRight(self):
        return (self.topLeft[0] + self.width - 1,
                self.topLeft[1])

    @property
    def bottomLeft(self):
        return (self.topLeft[0],
                self.topLeft[1] + self.height - 1)
                
    @property
    def width(self):
        return self._width
        
    @property
    def height(self):
        return self._height
    
    def area(self):
        return self.width * self.height

    def intersection(self, other):
        if self == other:
            return self
        
        tlx = max(min(self.topLeft[0], self.bottomRight[0]), min(other.topLeft[0], other.bottomRight[0]))
        tly = max(min(self.topLeft[1], self.bottomRight[1]), min(other.topLeft[1], other.bottomRight[1]))
        brx = min(max(self.topLeft[0], self.bottomRight[0]), max(other.topLeft[0], other.bottomRight[0]))
        bry = min(max(self.topLeft[1], self.bottomRight[1]), max(other.topLeft[1], other.bottomRight[1]))
        
        w = brx - tlx + 1
        h = bry - tly + 1
        
        if not tlx <= brx:
            w = 0
            
        if not tly <= bry:
            h = 0
        
        return type(self)(self.id + " & " + other.id,(tlx, tly), w, h)
    
    __and__ = intersection
    
    def union(self, other):
      if self == other:
        return self
        
      tlx = min(self.topLeft[0], other.topLeft[0])
      tly = min(self.topLeft[1], other.topLeft[1])
      w = max(self.bottomRight[0], other.bottomRight[0]) - tlx + 1
      h = max(self.bottomRight[1], other.bottomRight[1]) - tly + 1
      
      return Rectangle(self.id + " | " + other.id, (tlx, tly), w, h)
      
    __or__  = union
####
class Canvas():
    _canvas = None
    _w = 0
    _h = 0
    _usedSlots = 0
    _possibleUsableIds = None
    _conflictIds = None
    
    def __init__(self, width, height):
        self._canvas = [["." for x in range(0, width)] for y in range(0, height)]
        self._w = width
        self._h = height
        self._possibleUsableIds = []
        self._conflictIds = []
        
    def __str__(self):
        str = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                str += self._canvas[y][x]
                str += ' '
            str += '\n'
            
        return str

    @property
    def width(self):
        return self._w
        
    @property
    def height(self):
        return self._h
        
    @property
    def used(self):
        return self._usedSlots
        
    @property
    def usableId(self):
        # print("has {0}".format(len(self._possibleUsableIds)))
        assert len(self._possibleUsableIds) == 1
        return self._possibleUsableIds[0]
        
    def fill(self, rectangle):
        rx = rectangle.topLeft[0]
        ry = rectangle.topLeft[1]
        rw = rectangle.width
        rh = rectangle.height

        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                if self._canvas[y][x] == ".":
                    self._canvas[y][x] = rectangle.id
                    
                    if rectangle.id not in self._possibleUsableIds and rectangle.id not in self._conflictIds:
                        self._possibleUsableIds.append(rectangle.id)
                        # print("Possible id: {0}".format(rectangle.id))
                        
                elif self._canvas[y][x].isdigit():
                    id = self._canvas[y][x]
                    # print("Rect {0} has a conflict with id {1}".format(rectangle.id, id))
                    
                    if id not in self._conflictIds:
                        self._conflictIds.append(id)
                        
                    if rectangle.id not in self._conflictIds:
                        self._conflictIds.append(rectangle.id)
                        
                    # self._conflictIds.extend([id, rectangle.id])
                    
                    if id in self._possibleUsableIds:
                        self._possibleUsableIds.remove(id)
                        
                    if rectangle.id in self._possibleUsableIds:
                        self._possibleUsableIds.remove(rectangle.id)
                        
                    self._usedSlots += 1
                    self._canvas[y][x] = "X"
                    
                # print("Possible ids has: {0}".format(self._possibleUsableIds))
####
def parseInputFile(inputFile):
   rectangles = []
   union = Rectangle()
   
   with open(inputFile, 'r') as f:
    for line in f:
        id = line[1:line.find("@") - 1]
        tlx = int(line[line.find("@") + 2:line.find(",")])
        tly = int(line[line.find(",") + 1:line.find(":")])
        w = int(line[line.find(":") + 2:line.find("x")])
        h = int(line[line.find("x") + 1:])
        
        rectangles.append(Rectangle(id, (tlx, tly), w, h))
        union = union | rectangles[-1]

   return rectangles, union.width, union.height
        
    
if __name__ == "__main__":
    inputFile = sys.argv[1]
    rectangles, totalWidth, totalHeight = parseInputFile(inputFile)
    canvas = Canvas(totalWidth, totalHeight)
    
    print("Total width: {0} / height: {1}".format(totalWidth, totalHeight))
    # print("Canvas w: {0} / h: {1}".format(canvas.width, canvas.height))
    
    canvas.fill(rectangles[0])
    # print(canvas)
    for r in rectangles[1:]:
        canvas.fill(r)
        # print(canvas)

    print("---------------------")
    # print(canvas)
    print("Total used: {0}".format(canvas.used))
    print("Usable id: {0}".format(canvas.usableId))