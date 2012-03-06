def message(pryme, message, source, target):
    if (pryme.nick == message.pop(0)):
        if ('insult' == message.pop(0)):
            pryme.send(target, "Trip on thy sword, " + message.pop(0) + " !")
