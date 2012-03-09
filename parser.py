#parser

import urllib2
import base64
from xml.dom import minidom

projects = [
   'shopwindow/prime-swshared',
   'shopwindow/prime-swfeedprocessing',
   'shared/prime-localization',
   'shared/prime-shared',
   'darwin/prime-darwin'
]

pryme = 0

def init(globalPryme):
    global pryme
    pryme = globalPryme

def message(pryme, message, source, target):
    if not pryme.nick in message.pop(0):
        return
    if not "list" in message.pop(0):
        return
    for project in projects:
        requests = parse(project)
        if len(requests) > 0:
            pryme.send(target, project + " : " + str(len(requests)))
        for request in requests:
            pryme.send(target, "    " + displayRequest(request))


def displayRequest(request):
    return ("m" + request['id'] +
        " v" + str(request['versions']) +
        " [" + request['branch'] + "] : " + request['summary']
    )


def parse(project):
    url = 'https://gitorious.affiliatewindow.com/' + project + '/merge_requests.xml?status=Open'

    u = pryme.config.get('parser', 'username')
    p = base64.b64decode(pryme.config.get('parser', 'password'))

    # simple wrapper function to encode the username & pass
    def encodeUserData(user, password):
        return "Basic " + (user + ":" + password).encode("base64").rstrip()

    # create the request object and set some headers
    req = urllib2.Request(url)
    req.add_header('Accept', 'application/json')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Authorization', encodeUserData(u, p))
    # make the request and print the results
    try:
        res = urllib2.urlopen(req)
    except:
        print "Failed to retrieve merges for " + project
        return []

    dom = minidom.parseString(res.read())

    def getData(node, name):
        return str(node.getElementsByTagName(name)[0].firstChild.data)

    requests = []
    for node in dom.getElementsByTagName('merge-request'):
        requests.append({
            'id': getData(node, 'id'),
            'created-at': getData(node, 'created-at'),
            'summary': getData(node, 'summary'),
            'status': getData(node, 'status'),
            'versions': node.getElementsByTagName('version').length,
            'branch': getData(node.getElementsByTagName('source_repository')[0], 'branch'),
        })
    print "Found " + str(len(requests)) + ' requests'
    return requests


