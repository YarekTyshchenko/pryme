def message(pryme, message, source, target):
    if pryme.nick in message:
        if "test" in message:
            pryme.send(
                target,
                "Message :'" + message +
                "' from '" + source +
                "' in channel '" + target + "'"
            )
