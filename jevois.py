#!/usr/bin/python

import serial
import time

class Jevois(object):
	def __init__(self, serdev='/dev/tty.usbmodemFA133'):
		self.ser = serial.Serial(serdev, 115200, timeout=1)

	def close(self):
		# TODO: ensure that this works
		if self.ser.is_open:
			self.ser.close()

	# Send a command to JeVois and show response
	def sendCommand(self, cmd):
		"""Send a command to JeVois and show response."""
		print "HOST>> " + cmd
		self.ser.write(cmd + '\n')
		out = ''
		time.sleep(0.1)
		while self.ser.inWaiting() > 0:
			out += self.ser.read(1)
		if out != '':
			print "JEVOIS>> " + out, # the final comma suppresses extra newline, since JeVois already sends one

	def setParRange(self, par, minVal, maxVal):
		"""Send a command to set a range paramter."""
	 	self.sendCommand('setpar {0} {1}...{2}'.format(par, minVal, maxVal) )

	def setHue(self, val, toleranceLow=0, toleranceHigh=0):
		"""Set colour hue range for object tracking mode."""
		self.setParRange('hrange', max(0,val-toleranceLow), min(255,val+toleranceHigh) )

	def setSaturation(self, val, toleranceLow=0, toleranceHigh=0):
		"""Set colour saturation range for object tracking mode."""
		self.setParRange('srange', max(0,val-toleranceLow), min(255,val+toleranceHigh) )

	####################################################################################################
	def setValue(self, val, toleranceLow=0, toleranceHigh=0):
		"""Set colour value range for object tracking mode."""
		self.setParRange('vrange', max(0,val-toleranceLow), min(255,val+toleranceHigh) )

	def setObjectTrackerColourParams(self, hsvVals, tolerance):
		"""Set HSV values for object tracking mode."""
		tol = [[50,25],[75,75],[90,90]]
		try:
			# self.setHue(hsvVals['h'], tol[0][0], tol[0][1])
			# self.setSaturation(hsvVals['s'], tol[1][0], tol[1][1])
			# self.setValue(hsvVals['v'], tol[2][0], tol[2][1])
			self.setHue(hsvVals['h'], tolerance, tolerance)
			self.setSaturation(hsvVals['s'], tolerance, tolerance)
			self.setValue(hsvVals['v'], tolerance, tolerance)
		except Exception, e:
			print >> sys.stderr, "Expected object with H, S, and V integer values"
			print >> sys.stderr, "Exception: %s" % str(e)
			return 1
