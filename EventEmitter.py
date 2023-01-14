import inspect

class EventEmitter:
	def __init__(self):
		self.events = {}

	def on(self, evt, func):
		if not evt in self.events.keys():
			self.events[evt] = []
		
		self.events[evt].append(func)

	def off(self, evt, func):
		if not evt in self.events.keys(): return
		try:
			self.events[evt].remove(func)
		except: pass

	async def emit(self, evt, **args):
		if not evt in self.events.keys(): return
		for func in self.events[evt]:
			if inspect.iscoroutinefunction(func):
				await func(**args)
			else:
				func(**args)
