"""
Tile Coding Software version 3.0beta
by Rich Sutton
based on a program created by Steph Schaeffer and others
External documentation and recommendations on the use of this code is available in the 
reinforcement learning textbook by Sutton and Barto, and on the web.
These need to be understood before this code is.

This software is for Python 3 or more.

This is an implementation of grid-style tile codings, based originally on
the UNH CMAC code (see http://www.ece.unh.edu/robots/cmac.htm), but by now highly changed. 
Here we provide a function, "tiles", that maps floating and integer
variables to a list of tiles, and a second function "tiles-wrap" that does the same while
wrapping some floats to provided widths (the lower wrap value is always 0).

The float variables will be gridded at unit intervals, so generalization
will be by approximately 1 in each direction, and any scaling will have 
to be done externally before calling tiles.

Num-tilings should be a power of 2, e.g., 16. To make the offsetting work properly, it should
also be greater than or equal to four times the number of floats.

The first argument is either an index hash table of a given size (created by (make-iht size)), 
an integer "size" (range of the indices from 0), or nil (for testing, indicating that the tile 
coordinates are to be returned without being converted to indices).
"""
import numpy as np
basehash = hash

class IHT:
    "Structure to handle collisions"
    def __init__(self, sizeval):
        self.size = sizeval                        
        self.overfullCount = 0
        self.dictionary = {}

        self.hF = None
        self.lF = None
        self.hS = None
        self.lS = None
    def __str__(self):
        "Prepares a string for printing whenever this object is printed"
        return "Collision table:" + \
               " size:" + str(self.size) + \
               " overfullCount:" + str(self.overfullCount) + \
               " dictionary:" + str(len(self.dictionary)) + " items"

    def count (self):
        return len(self.dictionary)
    
    def fullp (self):
        return len(self.dictionary) >= self.size
    
    def getindex (self, obj, readonly=False):
        d = self.dictionary
        if obj in d: return d[obj]
        elif readonly: return None
        size = self.size
        count = self.count()
        print(size-count)
        # print(obj)
        (f, s) = obj
        if self.hF is None or f > self.hF:
            self.hF = f
        if self.lF is None or f < self.lF:
            self.lF = f
        if self.hS is None or s > self.hS:
            self.hS = s
        if self.lS is None or s < self.lS:
            self.lS = s
        if count >= size:
            if self.overfullCount==0: print('IHT full, starting to allow collisions')
            print("{0} {1} | {2} {3}".format(self.hF, self.lF, self.hS, self.lS))
            print(self.size)
            assert(1==2) # never let this happen
            self.overfullCount += 1
            return basehash(obj) % self.size
        else:
            d[obj] = count
            return count

def hashcoords(coordinates, m, readonly=False):
    if type(m)==IHT: return m.getindex(tuple(coordinates), readonly)
    if type(m)==int: return basehash(tuple(coordinates)) % m
    if m==None: return coordinates

from math import floor, log
from itertools import zip_longest

def tiles (ihtORsize, numtilings, floats, ints=[], readonly=False):
    """returns num-tilings tile indices corresponding to the floats and ints"""
    qfloats = [floor(f*numtilings) for f in floats]
    Tiles = []
    #assert(floats[0]<=1 and floats[0]>=0)    
    for tiling in range(numtilings):
        tilingX2 = tiling*2
        coords = [tiling]
        b = tiling
        for q in qfloats:
            coords.append( (q + b) // numtilings )
            b += tilingX2
        coords.extend(ints)
        
        # if coords[1] >= 18:
        #     print("\nbanana")
        #     print(floats)

        Tiles.append(hashcoords(coords, ihtORsize, readonly))
    #print(coords)

    # assert(coords[1])<18

    return Tiles

def tileswrap (ihtORsize, numtilings, floats, wrawidths, ints=[], readonly=False):
    """returns num-tilings tile indices corresponding to the floats and ints, wrapping some floats"""
    qfloats = [floor(f*numtilings) for f in floats]
    Tiles = []
    for tiling in range(numtilings):
        tilingX2 = tiling*2
        coords = [tiling]
        b = tiling
        for q, width in zip_longest(qfloats, wrapwidths):
            c = (q + b%numtilings) // numtilings
            coords.append(c%width if width else c)
            b += tilingX2
        coords.extend(ints)
        Tiles.append(hashcoords(coords, ihtORsize, readonly))
    return Tiles




class myTileInterface:
    # convert to a vector
    def __init__(self, maxBandwidth, numTiles, numTilings):
        self.numTilings = numTilings
        self.numTiles = numTiles
        self.iht = IHT(self.featureSize()) 
        # note we have set our maxsize to precisely the number of tilings expected.
        # we are trying to cause a failure if i've misunderstood how this software works
        self.maxBandwidth = maxBandwidth
        print("\n\nmaxBandwidth = {0}, numTiles = {1}".format(maxBandwidth, numTiles))
        self.scaleFactor = (numTiles*1.0/(maxBandwidth))
        self.initialise()

    """
    def myTiles(self, x):
        # transform the state to the desired format
        x = np.array(x)
        x = x*self.scaleFactor
        tileResponse=[]
        for num in range(len(x)):
            tileResponse.append(tiles(self.iht, self.numTilings, x[num:num+1])[0])
        return tuple(tileResponse)
    """

    def encode(self, x):
        if x > self.maxBandwidth:
            print(x)
            assert(1==2)
        return tiles(self.iht, self.numTilings, [self.scaleFactor * x])


    def encodeToVector(self, x):
        # make a binary vector of featureSize to represent tilings
        output = np.zeros(self.featureSize())
        # print(x)
        # print(self.encode(x))
        for tile in self.encode(x):
            output[tile]=1
        #print(output)
        return output

    def featureSize(self):
        return (self.numTilings+1)*(self.numTiles-1) + self.numTilings


    def initialise(self):
        # generate all the expected values in increments of 0.01 so that all tiles are initialised
        # shouldn't make much difference but its good to have everything sorted early
        for i in np.arange(0.0, self.maxBandwidth+0.1, 0.1):
            self.encodeToVector(i)

