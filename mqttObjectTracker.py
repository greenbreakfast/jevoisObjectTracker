#!/usr/bin/python

import time
import json
import sys, getopt

import paho.mqtt.client as mqtt

import jevois, colourConv


def printUsage():
	print 'mqttObjectTrackerColourTuning.py -t <tolerance> -s <MQTT Server> -t <MQTT Topic> -p <MQTT PORT>'
	sys.exit(2)

def parseCommandLineArgs(config, argv):
	# check for arguments
	if len(argv) != 8:
		printUsage()

	# parse the arguments
	try:
		opts, args = getopt.getopt(argv,"hl:s:t:p:",["tolerance=", "server=", "topic=", "port="])
	except getopt.GetoptError:
		printUsage()

	# interpret the arguments
	for opt, arg in opts:
		if opt == '-h':
			printUsage()
		elif opt in ("-l", "--tolerance"):
			try:
				config['tolerance'] = int(arg)
			except Exception, e:
				print >> sys.stderr, "Expected an integer number value"
				print >> sys.stderr, "Exception: %s" % str(e)
				sys.exit(1)
		elif opt in ("-s", "--server"):
			config['mqtt']['server'] = arg
		elif opt in ("-t", "--topic"):
			config['mqtt']['topic'] = arg
		elif opt in ("-p", "--port"):
			try:
				config['mqtt']['port'] = int(arg)
			except Exception, e:
				print >> sys.stderr, "Expected an integer number value"
				print >> sys.stderr, "Exception: %s" % str(e)
				sys.exit(1)

def mqttRoutine(config):
	## setup mqtt and jevois objects
	mqttc = mqtt.Client()
	#machine = jevois.Jevois()


	## define the mqtt callbacks
	# when connection is made
	def on_connect(client, userdata, flags, rc):
		print("Connection result: " + str(rc))
		# subscribe to topic specified by config
		mqttc.subscribe(config['mqtt']['topic'], 0)

	def on_message(client, userdata, msg):
		if msg.payload:
			print(msg.topic + ":: payload is " + str(msg.payload))
			handleMessage(msg.topic, msg.payload)

	def on_subscribe(client, userdata, mid, granted_qos):
		print("Subscribed: " + str(mid) + " " + str(granted_qos))

	def on_disconnect(client, userdata, rc):
		print("Disconnected from Server")
		# close the serial port
		#machine.close()
	## end of mqtt callbacks

	## other functions
	def handleMessage(topic, payload):
		if topic == config['mqtt']['topic']:
			# read json data from topic
			try:
				msg = json.loads(payload)
			except Exception, e:
				print >> sys.stderr, "Expected JSON on MQTT topic ", config['mqtt']['topic']
				print >> sys.stderr, "Exception: %s" % str(e)
				return 1
			# program jevois with received hsv values
			if "h" not in msg or "s" not in msg or "v" not in msg:
				print >> sys.stderr, "Expected JSON with h, s, v parameters on MQTT topic ", config['mqtt']['topic']
				return 1
			tol = config['tolerance']
			if "tolerance" in msg:
				tol = msg['tolerance']

			#print("Programming jevois with (H:", msg['h'], ", S:", msg['s'], ", V:", msg['v'], ") and tolerance of ", tol )
			# convert hsv values to Jevois HSV (0-255)
			jevoisHsv = colourConv.hsvToJevoisHsv(msg)
			print("Programming jevois with (H:", jevoisHsv['h'], ", S:", jevoisHsv['s'], ", V:", jevoisHsv['v'], ") and tolerance of ", tol )
			#machine.setObjectTrackerColourParams(jevoisHsv, tol)



	## Assign event callbacks
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.on_disconnect = on_disconnect
	# Connect
	mqttc.connect(config['mqtt']['server'], config['mqtt']['port'], 60)

	# TODO: add a ctrl+c handler to call:
	# machine.close()

	# Continue the network loop
	mqttc.loop_forever()


# main code
def main(argv):
	# default configuration
	config = {
		'tolerance': 10,
		'mqtt': {
			'server': "",
			'topic': "",
			'port': 1883	# TODO: confirm this port number
		}
	}

	# parse command line arguments
	parseCommandLineArgs(config, argv)

	# run mqtt code
	mqttRoutine(config)



if __name__ == "__main__":
	main(sys.argv[1:])
