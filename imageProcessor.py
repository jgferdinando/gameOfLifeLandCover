#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 09:44:29 2021

@author: Joe
"""

from PIL import Image

#uses categories from ESA land cover 10 meter with extra 

#land cover color dictionary
landcover = {
    'trees': (0,100,0,255),
    'shrubland': (255,187,34,255),
    'grassland': (255,255,76,255),
    'cropland': (240,150,255,255),
    'buildup': (250,0,0,255),
    'barren': (180,180,180,255),
    'snowice': (240,240,240,255),
    'water': (0,100,200,255),
    'wetland': (0,150,160,255),
    'mangrove': (0,207,117,255),
    'mosslichen': (250,230,160,255),
    'prep': (255,255,255,255),
    'settlement': (0,0,0,255),
    'agf1': (0,200,0,255),
    'agf2': (0,190,0,255),
    'agf3': (0,180,0,255),
    'agf4': (0,170,0,255),
    'agf5': (0,160,0,255),
    'agf6': (0,150,0,255),
    'agf7': (0,140,0,255),
    'agf8': (0,130,0,255),
    'agf9': (0,120,0,255)
    }

#loop for generations
generations = 10
for i in range(generations):
    im = Image.open("./landCoverFrames/gen{}.png".format(i))
    img = im
    pixelMap = im.load()
    pixelMap2 = pixelMap
    #nested loops for x, y. adjust to leave 1 pixel buffer 
    for j in range(img.size[0]-2):
        x = j + 1
        for k in range(img.size[1]-2):
            y = k + 1
            #check conditions
            #advance states
            if pixelMap[x,y] == landcover['prep']:
                pixelMap2[x,y] = landcover['agf1']
            elif pixelMap[x,y] == landcover['agf1']:
                pixelMap2[x,y] = landcover['agf2']
            elif pixelMap[x,y] == landcover['agf2']:
                pixelMap2[x,y] = landcover['agf3']
            elif pixelMap[x,y] == landcover['agf3']:
                pixelMap2[x,y] = landcover['agf4']
            elif pixelMap[x,y] == landcover['agf4']:
                pixelMap2[x,y] = landcover['agf5']
            elif pixelMap[x,y] == landcover['agf5']:
                pixelMap2[x,y] = landcover['agf6']
            elif pixelMap[x,y] == landcover['agf6']:
                pixelMap2[x,y] = landcover['agf7']
            elif pixelMap[x,y] == landcover['agf7']:
                pixelMap2[x,y] = landcover['agf8']
            elif pixelMap[x,y] == landcover['agf8']:
                pixelMap2[x,y] = landcover['agf9']
            elif pixelMap[x,y] == landcover['agf9']:
                pixelMap2[x,y] = landcover['trees']
            
            #if grass, crop, barren
            elif pixelMap[x,y] == landcover['cropland'] or pixelMap[x,y] == landcover['barren'] or pixelMap[x,y] == landcover['grassland']:
                #add surrounding values to a list to check
                adjacencies = []
                adjacencies.append(pixelMap[x,y+1])
                adjacencies.append(pixelMap[x+1,y+1])
                adjacencies.append(pixelMap[x+1,y])
                adjacencies.append(pixelMap[x+1,y-1])
                adjacencies.append(pixelMap[x,y-1])
                adjacencies.append(pixelMap[x-1,y-1])
                adjacencies.append(pixelMap[x-1,y])
                adjacencies.append(pixelMap[x-1,y+1])
                #reset count and then tally adjacency types
                adjTrees = 0
                adjShrub = 0
                adjGrass = 0
                adjCrops = 0
                adjBuild = 0
                adjBarrn = 0
                adjSnowy = 0
                adjWater = 0
                adjWtlnd = 0
                adjMngrv = 0
                adjLchen = 0
                adjPreps = 0
                adjStlmt = 0
                for adjacency in adjacencies:
                    if adjacency == landcover['trees']:
                        adjTrees += 1
                    elif adjacency == landcover['shrubland']:
                        adjShrub += 1
                    elif adjacency == landcover['grassland']:
                        adjGrass += 1
                    elif adjacency == landcover['cropland']:
                        adjCrops += 1
                    elif adjacency == landcover['buildup']:
                        adjBuild += 1
                    elif adjacency == landcover['barren']:
                        adjBarrn += 1
                    elif adjacency == landcover['snowice']:
                        adjSnowy += 1
                    elif adjacency == landcover['water']:
                        adjWater += 1
                    elif adjacency == landcover['wetland']:
                        adjWtlnd += 1
                    elif adjacency == landcover['mangrove']:
                        adjMngrv += 1
                    elif adjacency == landcover['mosslichen']:
                        adjLchen += 1
                    elif adjacency == landcover['prep']:
                        adjPreps += 1
                    elif adjacency == landcover['settlement']:
                        adjStlmt += 1
                    else:
                        continue
                #check state and adjacencies:
                if adjTrees + adjStlmt + adjPreps > 3:
                    pixelMap2[x,y] = landcover['prep']
                else:
                    continue
            #if trees, shrub, build-up, snow, water, wetland, mangrove, moss, or any other, skip
            else:
                pixelMap2[x,y] = pixelMap[x,y]

  
    img.save("./landCoverFrames/gen{}.png".format(i+1)) 
    im.close()
    img.close()