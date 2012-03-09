def message(pryme, message, source, target):
    if pryme.nick in message.pop(0):
        action = message.pop(0)
        channel = message.pop(0)
        if "join" in action:
            pryme.debug("Joining channel: " + channel)
            pryme.server.join(channel)
        if "part" in message:
            pryme.debug("Leaving channel: " + channel)
            pryme.server.part(channel)