import sock

sendingPort = 6666

while True:
	data = raw_input()

	packet = sock.Functions.backToJSON(data)
	thisSocket = sock.Socket()

	thisSocket.SendTo('192.168.1.103', packet)