import sys

class Helper(object):

	def __init__(self, _ConfigDefault):
		self._ConfigDefault = _ConfigDefault
	
	#following from http://code.activestate.com/recipes/475186/
	def has_colours(self, stream):
		if not hasattr(stream, "isatty"):
			return False
		if not stream.isatty():
			return False # auto color only on TTYs
		try:
			import curses
			curses.setupterm()
			return curses.tigetnum("colors") > 2
		except:
			# guess false in case of error
			return False
	
	def printout(self, text, colour):
		if not colour:
			colour=self._ConfigDefault['mesg.white']
		if self.has_colours(sys.stdout):
			seq = "\x1b[1;%dm" % (colour) + text + "\x1b[0m"
			sys.stdout.write(seq)
		else:
			sys.stdout.write(text)
			
	#following from http://code.activestate.com/recipes/266466/
	def HTMLColorToRGB(self, colorstring):
		try:
			""" convert #RRGGBB to an (R, G, B) tuple """
			colorstring = colorstring.strip()
			if colorstring[0] == '#': colorstring = colorstring[1:]
			if len(colorstring) != 6:
				raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
			r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
			r, g, b = [int(n, 16) for n in (r, g, b)]
			return (r, g, b)
		except ValueError as text:
			self.printout("[error]   ", self._ConfigDefault['mesg.red'])
			print "Color Error RGB! " + str(text)
			exit()