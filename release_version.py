print "join release_version.py"

import struct
BITS = struct.calcsize("P") * 8

def version_data():
	data = {
			"VERSION" : "0.6.6",
			"SIGN" : True,
			"NAME" : "%s Client" % (org_data()["ORG"]),
		}
	return data

def build_data():
	from datetime import date
	import time
	data = {
		"YEAR" : date.today().year,
		"MONTH" : date.today().month,
		"DAY" : date.today().day,
		"STAMP" : int(time.time())
	}
	return data

def org_data():
	data = {
			"ORG" : "oVPN.to",
			"ADD" : "Anonymous Services",
			"SITE" : "https://oVPN.to",
			"EMAIL" : "support@ovpn.to",
			"SUPPORT" : "https://vcp.ovpn.to/?site=support",
			"CHAT_URL" : "https://webirc.ovpn.to",
			"IRC_ADDR" : "irc://irc.ovpn.to:6697 (SSL)",
			"UPDATES" : "https://board.ovpn.to/v4/index.php?thread/57314-ovpn-client-for-windows-beta-binary-releases/&action=firstNew",
			"VCP_DOMAIN" : "vcp.ovpn.to",
			"API_POST" : "xxxapi.php",
			"API_DOMAIN" : "vcp.ovpn.to",
			"API_PORT" : "443",
		}
	return data

def setup_data():
	data = { 
			"script" : "ovpn_client.py",
			"exename" : "ovpn_client.exe",
			"version" : "0.%s" % (version_data()["VERSION"]),
			"name" : "%s for Windows" % (version_data()["NAME"]),
			"description" : "%s %s" % (version_data()["NAME"],version_data()["VERSION"]),
			"copyright" : "(C) 2010 - %s %s" % (build_data()["YEAR"],org_data()["ORG"]),
			"DIST_DIR1" : "dist%s"%(BITS),
			"DIST_DIR2" : "dist_check_bin%s"%(BITS),
			"py2exe_excludes" : [ 'tcl','tcl8.5','tk8.5','win32pipe','win32wnet','_tkinter','Tkinter','Tk','_testcapi' ],
			"py2exe_includes" : [ 'gi','requests','cairo','types','os','platform','sys','hashlib','random','time','zipfile','subprocess','threading','socket','random','gettext','locale','_winreg','base64','zlib','netifaces','ctypes' ],
			"dll_excludes" : [ 'libgstreamer-1.0-0.dll','MSVCR100.dll','pywintypes27.dll','crypt32.dll','tcl85.dll', 'tk85.dll','DNSAPI.DLL','USP10.DLL','MPR.DLL','MSIMG32.DLL','API-MS-Win-Core-LocalRegistry-L1-1-0.dll','IPHLPAPI.DLL','w9xpopen.exe','mswsock.dll','powrprof.dll'],
		}
	return data

print "version_data() = '%s'" % (version_data())
print "build_data() = '%s'" % (build_data())
print "org_data() = '%s'" % (org_data())
print "setup_data() = '%s'" % (setup_data())


import sys, os
if len(sys.argv) > 1:
	
	if sys.argv[1] == "SET_VERSION_FILES":
		
		def write_releasefile(key,file,content):
			if os.path.isfile(file):
				fp = open(file, "wb")
				fp.write(content)
				fp.close()
				print "%s written content '%s' to file '%s'" % (key,file,content)
			else:
				print "file '%s' not found" % (file)
		
		setrelease = {
			"winb" : { "file" : "set_version.bat", "content" : 'set RELEASE=%s' % (version_data()["VERSION"]) },
			"hard" : { "file" : "release_hard%s.py" % (BITS), "content" : 'def builtdate(): return "%s %s - built: %d-%02d-%02d (%d) %s BITS"' % (version_data()["NAME"],version_data()["VERSION"],build_data()["YEAR"],build_data()["MONTH"],build_data()["DAY"],build_data()["STAMP"],BITS) },
			}
			
		for key, value in setrelease.items():
			write_releasefile(key,value["file"],value["content"])

print "leave release_version.py"