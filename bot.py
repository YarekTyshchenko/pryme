import irclib
import sys
import ConfigParser
import signal


class Pryme:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        self.config = config;

        self.network = self.config.get('pryme', 'network')
        self.port = int(self.config.get('pryme', 'port'))
        self.channel = self.config.get('pryme', 'channel')
        self.nick = self.config.get('pryme', 'nick')
        self.adminNick = self.config.get('pryme', 'adminNick')

        self.modules = [
            'parser',
            'reloader',
            'joiner',
            'insult',
            'loader',
            'api'
        ]

        modules = []
        for module in self.modules:
            if not module in sys.modules:
                print "importing " + module
                moduleObject = __import__(module)
                try:
                    moduleObject.init(self)
                except:
                    pass
                modules.append(moduleObject)
        self.modules = modules

        # Create the IRC object
        self.irc = irclib.IRC()

        # Register handlers
        self.irc.add_global_handler('privmsg', self.handleEcho)
        self.irc.add_global_handler('pubmsg', self.handleEcho)

        # Connect to the network
        self.server = self.irc.server()
        print "Connecting: " + self.network + ':' + str(self.port) + " as " + self.nick
        self.server.connect(self.network, self.port, self.nick)
        print  "Joining channel " + self.channel
        self.server.join(self.channel)

    def run(self):
        # Run an infinite loop
        while 1:
            self.irc.process_once(0.2)

    def send(self, target, message):
        self.msg(message, target)

    def getMessage(self, event):
        return ''.join(event.arguments()).split(' ')

    def getSource(self, event):
        return event.source().split('!')[0]

    def getTarget(self, event):
        return event.target()

    def handleEcho(self, connection, event):
        for module in self.modules:
            try:
                module.message(self, self.getMessage(event), self.getSource(event), self.getTarget(event))
            except AttributeError:
                pass
            except Exception as exception:
                self.send(self.getTarget(event), "Module '"+str(module)+"' has crashed")
                print exception
                pass

    def admin(self, message):
        self.server.privmsg(self.adminNick, message)

    def msg(self, message, target=0):
        if not target:
            target = self.channel
        self.server.privmsg(target, message)

    def debug(self, message):
        print message

    def shutdown(self, signal, frame):
        print 'Shutting Down...'
        for module in self.modules:
            try:
                module.shutdown()
            except:
                pass
        sys.exit(0)

pryme = Pryme()
signal.signal(signal.SIGINT, pryme.shutdown)
pryme.run()
