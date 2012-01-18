def message(pryme, message, source, target):
	if pryme.nick in message:
		if 'insult' in message:
			pryme.send(target, "Trip on thy sword, "+source+" !")