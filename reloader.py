def message(pryme, message, source, target):
    if source not in pryme.adminNick:
        return
	
    if pryme.nick in message.pop(0):
        if "reload" in message.pop(0):
            for module in pryme.modules:
                pryme.debug("Reloading '" + str(module) + "'")
                reload(module)
            pryme.send(target, 'Modules Reloaded')
