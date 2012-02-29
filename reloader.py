def message(pryme, message, source, target):
    if pryme.nick in message:
        if "reload" in message:
            for module in pryme.modules:
                pryme.debug("Reloading '" + str(module) + "'")
                reload(module)
            pryme.send(target, 'Modules Reloaded')
    return
