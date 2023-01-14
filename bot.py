from Client import Client
from EventEmitter import EventEmitter
import asyncio
from dotenv import get_key

class Bot:
	def __init__(self):
		self.cl = Client("wss://mppclone.com:8443", get_key(key_to_get='MPPCLONE_TOKEN', dotenv_path='.env'))
		self.desiredChannel = '✧𝓓𝓔𝓥 𝓡𝓸𝓸𝓶✧'
		self.bindEventListeners()

	def start(self):
		asyncio.run(self.cl.start())

	async def sendChat(self, str):
		await self.cl.sendArray([{'m': 'a', 'message': '\u034f' + str}])
	
	def bindEventListeners(self):
		self.cl.on('hi', self.onHi)
		self.cl.on('ch', self.onCh)
		self.cl.on('a', self.onA)
		self.cl.on('participant added', self.onParticipantAdded)

	async def onHi(self, msg):
		print('Connecting to ' + self.desiredChannel)
		await self.cl.sendArray([{'m': 'ch', '_id': self.desiredChannel}])

	async def onCh(self, msg):
		print('Connected to ' + msg.get('ch').get('_id'))

	async def onA(self, msg):
		print(msg.get('p').get('name') + ': ' + msg.get('a'))

		str = msg.get('a')
		match str:
			case '/help':
				await self.sendChat('Commands: /help, /about')
			case '/about':
				await self.sendChat('This bot was made in Python.')
	
	async def onParticipantAdded(self, msg):
		p = msg
		print(p.get('name') + " [" + p.get('_id') + "] joined the room")

def main():
	bot = Bot()
	bot.start()

if __name__ == "__main__":
	main()
