import sock
import json

sendingPort = 6666

class Object:
	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def findContentOfMessage(self, rawData):
		newData = rawData.split(' ')
		if len(newData) < 2:
			print "Invalid operator"
		else :
			Data = ' '.join(newData[2:])
			return Data

	def findCommand(self, rawData):
		result = rawData.split(' ')
		command = result[0]
		return command

while True:
	rawData = raw_input()

	packet = Object()
	packet.event = packet.findCommand(rawData)
	packet.subdata = Object()
	packet.subdata.content = packet.findContentOfMessage(rawData)

	print packet.event
	jsonIs = packet.to_JSON()

	print jsonIs

	thisSocket = sock.Socket()

	thisSocket.SendTo('192.168.1.103', jsonIs)