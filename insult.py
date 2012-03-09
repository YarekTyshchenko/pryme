def message(pryme, message, source, target):
    if pryme.nick in message.pop(0):
        if 'insult' in message.pop(0):
            pryme.send(target, "Trip on thy sword, " + message.pop(0) + " !")
