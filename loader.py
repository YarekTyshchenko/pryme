def message(pryme, message, source, target):
    if source in pryme.adminNick:
        if pryme.nick in message.pop(0):
            if "addmodule" in message.pop(0):
                moduleName = message.pop(0)
                print 'Importing ' + moduleName
                module = __import__(moduleName)
                pryme.modules.append(module)