import irclib
import ConfigParser

#modules
import parser
import reloader
import joiner
import tester
import insult


class Pryme:
   def __init__(self):
      config = ConfigParser.ConfigParser()
      config.read('config.ini')

      self.network = config.get('pryme', 'network')
      self.port = int(config.get('pryme', 'port'))
      self.channel = config.get('pryme', 'channel')
      self.nick = config.get('pryme', 'nick')
      self.adminNick = config.get('pryme', 'adminNick')

      self.modules = [
         tester,
         parser,
         reloader,
         joiner,
         insult
      ]

      # Create the IRC object
      irc = irclib.IRC()

      # Register handlers
      irc.add_global_handler('privmsg', self.handleEcho)
      irc.add_global_handler('pubmsg', self.handleEcho)

      # Connect to the network
      self.server = irc.server()
      print "Connecting: "+self.network+':'+str(self.port)+" as "+self.nick+" and joining channel "+self.channel
      self.server.connect(self.network, self.port, self.nick)
      self.server.join(self.channel)

      # Run an infinite loop
      while 1:
         irc.process_once(0.2)

   def send(self, target, message):
      self.msg(message, target)

   def getMessage(self, event):
      return ''.join(event.arguments())
   def getSource(self, event):
      return event.source().split('!')[0]
   def getTarget(self, event):
      return event.target()

   def handleEcho (self, connection, event):
      for module in self.modules:
         try:
            module.message(self, self.getMessage(event), self.getSource(event), self.getTarget(event))
         except:
            self.send(self.getTarget(event), "Module '"+str(module)+"' has crashed")
            pass

   def admin(self, message):
      self.server.privmsg(self.adminNick, message)

   def msg(self, message, target=0):
      if not target:
         target = self.channel
      self.server.privmsg(target, message)
   def debug(self, message):
      print message

pryme = Pryme()
