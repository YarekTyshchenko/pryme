def message(pryme, message, source, target):
	originalMessage = message[:]
    if pryme.nick in message.pop(0):
        if "test" in message.pop(0):
            pryme.send(
                target,
                "Message :'" + originalMessage +
                "' from '" + source +
                "' in channel '" + target + "'"
            )
