class Event:
	def __init__(self, eventName, handler):
		self.eventName = eventName
		self.handler = handler
	def CallHandler(self,*arg):
		self.handler(*arg)

class Messenger:
	events = []
	@staticmethod
	def AddListener(eventName, handler):
		Messenger.events.append(Event(eventName, handler))

	@staticmethod
	def BroadcastMessage(eventName, *args):
		for handler in Messenger.GetEvents(eventName):
			handler.CallHandler(*args)

	@staticmethod
	def RemoveListener(eventName, handler):
		for event in Messenger.GetEvents(eventName):
			if (event.handler == handler):
				Messenger.events.remove(event)

	@staticmethod
	def GetEvents(eventName):
		result = []
		for i in range(0, len(Messenger.events)):
			if Messenger.events[i].eventName == eventName:
				result.append(Messenger.events[i])
		return result