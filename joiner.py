import re

def message(pryme, message, source, target):
    if pryme.nick in message:
        if "join" in message:
            channel = parseChannel(message)
            pryme.debug("Joining channel: " + channel)
            pryme.server.join(channel)
        if "part" in message:
            channel = parseChannel(message)
            if not channel:
                channel = target
            pryme.debug("Leaving channel: " + channel)
            pryme.server.part(channel)


def parseChannel(message):
    channel = 0
    try:
        p = re.compile('[#&][^\x07\x2C\s]{0,200}')
        m = p.search(message)
        channel = m.group()
    finally:
        return channel
