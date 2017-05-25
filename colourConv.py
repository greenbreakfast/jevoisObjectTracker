#!/usr/bin/python

import colorsys

# input a hex number
# output an object with each 
def splitHexColour(hexCol):
   r = (hexCol >> (2*8)) & 0x0ff
   g = (hexCol >> (8)) & 0x0ff
   b = (hexCol) & 0x0ff
   return {'r':r, 'g':g, 'b':b}

# convert value out of 0xff to a percentage
def percentify(val):
   return (float(val)/255.0)

# convert a percentage to a value out of 0xff
def hexify(percent):
   return ( int( percent*255.0) )


# accept a colour value in hex
# return an object with the corresponding HSV value (0x00 to 0xff)
def hexColourToJevoisHsv(colourHex):
	colourVals = splitHexColour(colourHex)
	percentColourVals = { 
		'r':percentify(colourVals['r']), 
		'g':percentify(colourVals['g']), 
		'b':percentify(colourVals['b']) 
	}

	print ("Converting 0x%06x (%.02f, %.02f, %.02f) to HSV"%(colourHex, percentColourVals['r'], percentColourVals['g'], percentColourVals['b']))
	hsvPercentVals = colorsys.rgb_to_hsv(percentColourVals['r'], percentColourVals['g'], percentColourVals['b'])

	hsvVals = {
		'h': hexify(hsvPercentVals[0]), 
		's': hexify(hsvPercentVals[1]), 
		'v': hexify(hsvPercentVals[2])
	}
	print ("HSV: %d %d %d (%.02f, %.02f, %.02f)"%(hsvVals['h'], hsvVals['s'], hsvVals['v'], hsvPercentVals[0], hsvPercentVals[1], hsvPercentVals[2]) )

	return hsvVals

# accept a colour value in HSV (360deg, 1, 1)
# return an object with the corresponding HSV value (0x00 to 0xff)
def hsvToJevoisHsv(colourHsv):
	hsvVals = {}
	try:
		hsvVals = {
			'h': hexify(float(colourHsv['h'])/360.0), 
			's': hexify(float(colourHsv['s'])), 
			'v': hexify(float(colourHsv['v']))
		}
		print ("HSV: %d %d %d (%.02fdeg, %.02f, %.02f)"%(hsvVals['h'], hsvVals['s'], hsvVals['v'], colourHsv['h'], colourHsv['s'], colourHsv['v']) )
	except:
		print ("ERROR: Could not read Hue value correctly")

	return hsvVals
