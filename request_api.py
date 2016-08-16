# -*- coding: utf-8 -*-
import os, random, requests, string, sys

# .py file imports
from debug import debug
import release_version


def random_string():
	int = random.randint(16,32)
	rand = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(int))
	return rand
	
def useragent(DEBUG):
	debug(99,"def useragent()",DEBUG,True)
	user_agent = 007
	rand = random_string()
	try:
		version = release_version.version_data()["VERSION"]
		versionint = 0
		
		try:
			split = version.split(".")
			versionint = "%s%s%s" % (split[0],split[1],split[2])
		except:
			debug(1,"def useragent: version.split failed",DEBUG,True)
		
		if versionint > 0:
			version = versionint
		user_agent = "client/%s" % (version)
	except:
		debug(1,"def useragent: construct user-agent failed",DEBUG,True)
	headers = { 'User-Agent':"%s/%s" % (user_agent,rand) }
	debug(99,"def useragent: return headers = '%s'" % (headers),DEBUG,True)
	return headers