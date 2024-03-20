import numpy as np
import trimesh
import math

def getMinX(polygon):
    return polygon.bounds[0]

def getMinY(polygon):
    return polygon.bounds[1]

def getMaxX(polygon):
    return polygon.bounds[2]

def getMaxY(polygon):
    return polygon.bounds[3]

def getShoulder(sections, armpits_location):
    chestPolygon = getLargerAreaPolygon(sections[armpits_location-1])
    minY = getMinY(chestPolygon)
    maxY = getMaxY(chestPolygon)
    sumError = 100000
    cont = armpits_location
    position = None
    shoulder = None
    length = None
    for section in sections[armpits_location:]:
        miY = section.bounds[0][1]
        maY = section.bounds[1][1]
        difMin = abs(minY-miY)
        difMax = abs(maxY-maY)
        sumDifError = difMin + difMax
        if sumDifError < sumError:
            sumError = sumDifError
            position = cont
            shoulder = section
            length = getLargerAreaPolygon(section).length
        cont = cont + 1
    
    return shoulder, position, length

def getArmpits(sections):
    location_percentage = 76 # percentage
    approximate_location = math.floor(location_percentage*len(sections)/100)
    section_min = approximate_location - 10
    section_max = approximate_location + 10
    range_sections = range(section_min, section_max)
    armpits = None
    position = None
    length = None
    stop = False
    for index in range_sections:
        if stop == False:
            if len(sections[index].entities) == 1:
                armpits = sections[index]
                position = index
                length = sections[index].polygons_closed[0].length
                stop = True
                
    return armpits, position, length

def getChest (sections, armpits_location):
    cont = armpits_location
    stop = False
    minimum = 100
    chest = None
    position = None
    length = None
    while stop == False:
        polygon = getLargerAreaPolygon(sections[cont])
        minimumPolygonX = getMinX(polygon)
        if minimumPolygonX < minimum:
            minimum = minimumPolygonX
            chest = sections[cont]
            position = cont
            length = polygon.length
        else:
            stop = True
        cont = cont - 1
        
    return chest, position, length
