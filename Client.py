import websockets
import asyncio
import json
import time
from threading import Timer

from EventEmitter import EventEmitter

class Client(EventEmitter):
	def __init__(self, uri, token):
		super().__init__()
		self.ppl = {}
		self.started = False
		self.uri = uri
		
		self.offlineParticipant = {
			'_id': '',
			'name': '',
			'color': '#777'
		}

		self.token = token

	async def start(self):
		if self.started: return
		self.started = True
		await self.connect()

	async def connect(self):
		self.bindEventListeners()

		async with websockets.connect(self.uri) as self.ws:
			try:
				while True:
					data = await self.ws.recv()
					msgs = json.loads(data)
					for msg in msgs:
						if not 'm' in msg.keys(): continue
						await self.emit(msg.get('m'), msg = msg)
			except websockets.ConnectionClosed: pass
	
	async def sendArray(self, msgs):
		str = json.dumps(msgs)
		await self.ws.send(str)

	def stop(self):
		self.started = False
		self.ws.disconnect()
	
	def bindEventListeners(self):
		async def onB(msg):
			await self.sendArray([{'m': 'hi', 'token': self.token}])
		
		self.on('b', onB)

		async def sendTime():
			await self.sendArray([{'m': 't', 'e': time.time()}])

		def sendTimeTimer():
			asyncio.run(sendTime())
			Timer(20, sendTimeTimer).start()

		Timer(20, sendTimeTimer).start()

		async def onP(msg):
			self.participantUpdate(msg)
			await self.emit('p', msg.get('p'))

		self.on('p', onP)
	
	async def participantUpdate(self, update):
		part = self.ppl[update.get('id')] or None
		if part == None:
			part = update
			self.ppl[part.id] = part
			await self.emit('participant added', part)
			await self.emit('count', self.countParticipants())
		else:
			for key in update.keys():
				part[key] = update[key]
			
			try: update.tag
			except: part.tag = None

			try: update.vanished
			except: part.vanished = None

	def countParticipants(self):
		return len(self.ppl.keys())

	def findParticipantById(self, id):
		return self.ppl.get(id) or self.offlineParticipant
