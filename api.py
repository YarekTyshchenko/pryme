from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse

pryme = 0
channels = []
server = 0

def init(globalPryme):
    global pryme
    pryme = globalPryme
    port = int(pryme.config.get('api', 'port'))
    Thread(target=serve_on_port, args=[port]).start()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_path.query)
        #print query
        message = ''.join(query['message'])
        self.send_response(200)
        #self.send_header("Content-type", "text/plain")
        self.end_headers()
        #self.wfile.write(message)
        print message
        pryme.send('#prime', message)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def serve_on_port(port):
    global server
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

def message(pryme, message, source, target):
    pass

def shutdown():
    server.shutdown()
