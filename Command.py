class Command:
	def __init__(self, id, cb, visible):
		self.id = id
		self.cb = cb
		self.visible = visible or False
