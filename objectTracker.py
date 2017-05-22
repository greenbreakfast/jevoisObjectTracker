#!/usr/bin/python

import time
import sys, getopt

import jevois
import colourConv


def printUsage():
   print 'objectTrackerColourTuning.py -c <color hexcode> -t <tolerance>'
   sys.exit(2)


# Main code
def main(argv):
	colourHex = 0
	tolerance = 10

	# check for arguments
	if len(argv) != 4:
		printUsage()

	# parse the arguments
	try:
		opts, args = getopt.getopt(argv,"hc:t:",["colour=","tolerance="])
	except getopt.GetoptError:
		printUsage()

	# interpret the arguments
	for opt, arg in opts:
		if opt == '-h':
			printUsage()
		elif opt in ("-c", "--colour"):
			try:
				colourHex = int(arg, 16)
			except Exception, e:
				print >> sys.stderr, "Expected a hex colour code"
				print >> sys.stderr, "Exception: %s" % str(e)
				sys.exit(1)
		elif opt in ("-t", "--tolerance"):
			try:
				tolerance = int(arg)
			except Exception, e:
				print >> sys.stderr, "Expected an integer number value"
				print >> sys.stderr, "Exception: %s" % str(e)
				sys.exit(1)

	# convert hex colour into HSV colour (array)
	colourHsv = colourConv.hexColourToHsv(colourHex)

	# instantiate the jevois object
	machine = jevois.Jevois()

	# set the object tracker colour value
	machine.setObjectTrackerColourParams(colourHsv, tolerance)

	# close the serial port
	machine.close()


if __name__ == "__main__":
   main(sys.argv[1:])



