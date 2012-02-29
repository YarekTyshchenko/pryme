import re


def message(pryme, message, source, target):
    if pryme.nick in message:
        if "addmodule" in message:
            moduleName = getModuleName(message)
            module = __import__(moduleName)
            pryme.modules.append(module)


def getModuleName(message):
    try:
        p = re.compile(':([^ ]+)')
        m = p.search(message)
        module = m.group()[1:]
    except:
        module = 0
        pass

    return module
