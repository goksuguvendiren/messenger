import socket
import sys
import threading
import urllib2, json
from messenger import Messenger

ListeningPort = 6666
SendingPort = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', ListeningPort))

#fatih = Functions.getFatihsIP()
USERS = {'server' : '178.62.156.238', 'fatih' : 'fatih', 'goksu' : '127.0.0.1' }

class Object:
	@staticmethod
	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class User:
	friends = []
	awaitingFriends = []

	def __init__(self, username, userIP):
		self.username = username
		self.userIP = userIP
	
	def addFriend(self, ip):
		toBeAdded = Functions.findUserByIP(ip)
		self.awaitingFriends.append(toBeAdded)

	def findFriendByIp(self, ip):
		for i in self.friends:
			if i.userIP == ip:
				return i
		return False

	def findAwaitingByIP(self, ip):
		for i in self.awaitingFriends:
			if i.userIP == ip:
				return i
		return False

	def deleteAwaiting(self, ip):
		for i in range(len(self.awaitingFriends)):
			if self.awaitingFriends[i].userIP == ip:
				del(self.awaitingFriends[i])

	def answer(self, choice):
		if choice == 'accept':
			self.accept()
		elif choice == 'decline':
			self.decline()

	def accept(self, ip):
		otherUser = self.findAwaitingByIP(ip)
		self.friends.append(otherUser)
		self.deleteAwaiting(ip)
		print otherUser.username + "'s been accepted !"

	def decline(self, ip):
		otherUser = self.findAwaitingByIP(ip)
		self.deleteAwaiting(ip)
		print otherUser.username + "'s been declined !"

me = User('myself', '127.0.0.1')

class Socket:
	def ListenTo(self):
		while True:
			# receive data from client (data, addr)
			data = s.recvfrom(1024)
			content = data[0]
			addr = data[1]
			print data
			Messenger.BroadcastMessage("incomingMessage", data)

	def SendTo(self, ip, message):     
		s.sendto(message, (ip, SendingPort))

class Functions:
	@staticmethod	
	def findSender(data):
		return data[1]
	
	@staticmethod
	def findContent(data):
		return data[0]
	
	@staticmethod	
	def findCommand(data):
		content = Functions.findContent(data)
		result = content.split(' ')
		command = result[0]
		return command
	
	@staticmethod
	def printMessage(data):
		content = Functions.findContent
		print content
	
	@staticmethod
	def ask(data):
		senderIP = Functions.findSender(data)
		sender = Functions.findUserByIP(senderIP)
		Socket.SendTo(senderIP, sender.username + " wants to add you !\n")
		Socket.SendTo(senderIP, "if you want to accept, print 'accept', otherwise, print 'decline'.")
	
	@staticmethod
	def toUser(data):
		ip = Functions.findSender
		User.addFriend(ip)
	
	@staticmethod	
	def getFatihsIP():
		request = urllib2.Request("http://ip.fatihbakir.net/ips.txt")
		result = urllib2.urlopen(request)
		string = result.read()
		page = json.loads(string)
		ip = page['ev']
		print ip
		return ip
	
	@staticmethod
	def findUserByIP(ip):
		for i in USERS:
			if i.userIP == ip:
				return i
		return False

Messenger.AddListener("incomingMessage", Functions.findCommand)
Messenger.AddListener("waitingFriend", Functions.toUser)
Messenger.AddListener("waitingFriend", Functions.ask)

sock = Socket()

ListeningThread = threading.Thread(name = 'LThread', target = sock.ListenTo)
ListeningThread.start()

while True:
	data = raw_input()
	
	sock.SendTo("127.0.0.1", data)