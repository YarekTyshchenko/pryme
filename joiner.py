def message(pryme, message, source, target):
    if source in pryme.adminNick:
        if pryme.nick in message.pop(0):
            action = message.pop(0)
            if "join" in action:
                channel = message.pop(0)
                pryme.debug("Joining channel: " + channel)
                pryme.server.join(channel)
            
            if "part" in action:
                pryme.debug("Leaving channel: " + target)
                pryme.server.part(target)