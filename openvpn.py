# -*- coding: utf-8 -*-
import os, time, subprocess, sys, json
from datetime import datetime
import shlex
import win32process

# .py file imports
from debug import debug
from debug import devmode
import release_version
import hashings
import signtool
import encodes
import platform

def values(DEBUG):
    debug(9,"[openvpn.py] def values()",DEBUG,True)
    try:
    
        OSVER = "Win7"
        if "Windows-10" in platform.platform():
            OSVER = "Win10"
        
        ARCH = get_arch(DEBUG)
        BUILT = "Apr 16 2020"
        TIMESTAMP = 1586988000
        VERSION = "2.4.9"
        BUILT_V = "I601"
        
        if OSVER == "Win10":
            SHA_512 = "0a18f720856429da8f68a9ab1ec782ee3655981cbfb5b33b94d03e85ba8b1315b370d7c35fe0f23ec7b1e12c2647c26cb5124cf890dec43b0f110253b42deb2d"
            F_SIZE = 4310696
        elif OSVER == "Win7":
            SHA_512 = "9589aff2daf60325d79fd561f326fcd02e7628dcb2c6cf067ac32f0753c1659596e6a64faf054cdd323c3f937098ccca62fbb4fbb8e9a1535f4db008cca6b2f5"
            F_SIZE = 4296720
        else:
            debug(1,"[openvpn.py] def values: OSVERSION failed = '%s'"%(platform.platform()),DEBUG,True)
            sys.exit()
        
        URLS = {
            "REM" : "https://%s/files/openvpn" % (release_version.org_data()["VCP_DOMAIN"]),
            "ALT" : "https://swupdate.openvpn.net/community/releases"
            }
        
        SETUP_FILENAME = "openvpn-install-%s-%s-%s.exe" % (VERSION,BUILT_V,OSVER)
        OPENVPN_DL_URL =  "%s/%s" % (URLS["REM"],SETUP_FILENAME)
        OPENVPN_DL_URL_ALT = "%s/%s" % (URLS["ALT"],SETUP_FILENAME)
        
        return {
                "ARCH":ARCH, "BUILT":BUILT, "TIMESTAMP":TIMESTAMP, "VERSION":VERSION, "BUILT_V":BUILT_V, 
                "SHA_512":SHA_512, "F_SIZE":F_SIZE, "SETUP_FILENAME":SETUP_FILENAME,
                "URLS":URLS, "OPENVPN_DL_URL":OPENVPN_DL_URL, "OPENVPN_DL_URL_ALT":OPENVPN_DL_URL_ALT,
                }
    except Exception as e:
        debug(1,"[openvpn.py] def values: failed, exception = '%s'"%(e),DEBUG,True)
        sys.exit()

def supported_platforms(DEBUG):
    debug(9,"[openvpn.py] def supported_platforms()",DEBUG,True)
    return [ "AMD64", "x86" ]

def get_arch(DEBUG):
    debug(9,"[openvpn.py] def get_arch()",DEBUG,True)
    data = os_platform(DEBUG)
    if data == "AMD64":
        ARCH = "x86_64"
    elif data == "x86":
        ARCH = "i686"
    else:
        sys.exit()
    debug(9,"[openvpn.py] def get_arch: ARCH = '%s'" % (ARCH),DEBUG,True)
    return ARCH

def os_platform(DEBUG):
    debug(9,"[openvpn.py] def os_platform()",DEBUG,True)
    true_platform = os.environ['PROCESSOR_ARCHITECTURE']
    try:
        true_platform = os.environ["PROCESSOR_ARCHITEW6432"]
    except KeyError:
        pass
        #true_platform not assigned to if this does not exist
    if true_platform in supported_platforms(DEBUG):
        debug(9,"[openvpn.py] def os_platform: true_platform = '%s'" % (true_platform),DEBUG,True)
        return true_platform
    else:
        debug(1,"[openvpn.py] def os_platform: true_platform = '%s' NOT SUPPORTED" % (true_platform),DEBUG,True)
        sys.exit()

def win_detect_openvpn(DEBUG,OPENVPN_EXE):
    # returns [ OPENVPN_DIR, OPENVPN_EXE ]
    try:
        debug(1,"[openvpn.py] def win_detect_openvpn()",DEBUG,True)
        if OPENVPN_EXE == False:
            debug(1,"[openvpn.py] def win_detect_openvpn: check programfiles",DEBUG,True)
            programfiles = [ "PROGRAMFILES", "PROGRAMFILES(x86)", "PROGRAMW6432" ]
            for getenv in programfiles:
                programfiles_dir = os.getenv(getenv)
                file = "%s\\OpenVPN\\bin\\openvpn.exe" % (programfiles_dir)
                if os.path.isfile(file):
                    debug(1,"[openvpn.py] def win_detect_openvpn: '%s'" % (file),DEBUG,True)
                    OPENVPN_DIR = "%s\\OpenVPN\\bin" % (programfiles_dir)
                    break
        else:
            try:
                OPENVPN_DIR = OPENVPN_EXE.rsplit('\\', 1)[0]
            except:
                return False
        
        if not OPENVPN_DIR == False and os.path.isdir(OPENVPN_DIR):
            OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
            if os.path.isfile(OPENVPN_EXE):
                return { "OPENVPN_DIR":OPENVPN_DIR,"OPENVPN_EXE":OPENVPN_EXE }
    except:
        debug(1,"[openvpn.py] def win_detect_openvpn: failed",DEBUG,True)
    debug(1,"[openvpn.py] def win_detect_openvpn: return False",DEBUG,True)
    return False

def win_get_openvpn_version(DEBUG,OPENVPN_DIR):
    OPENVPN_EXE = "%s\\openvpn.exe" % (OPENVPN_DIR)
    if not os.path.isfile(OPENVPN_EXE):
        debug(1,"[openvpn.py] def win_get_openvpn_version: OPENVPN_EXE not found",DEBUG,True)
        return False
    try:
        cmdstring = '"%s" --version' % (OPENVPN_EXE)
        cmdargs = shlex.split(cmdstring)
        p = subprocess.Popen(cmdargs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,creationflags = win32process.CREATE_NO_WINDOW)
        output, err = p.communicate()
        rc = p.returncode
        OVPN_VERSION = encodes.code_fiesta(DEBUG,'decode',output,'win_get_openvpn_version').splitlines()[0].split( )[1].replace(".","")
        OVPN_BUILT = encodes.code_fiesta(DEBUG,'decode',output,'win_get_openvpn_version').splitlines()[0].split("built on ",1)[1].split()
        debug(1,"[openvpn.py] def win_get_openvpn_version: OVPN_VERSION = '%s', OVPN_BUILT = '%s'"%(OVPN_VERSION,OVPN_BUILT),DEBUG,True)
        return [ OVPN_VERSION, OVPN_BUILT ]
    except Exception as e:
        debug(1,"[openvpn.py] def win_get_openvpn_version: failed, exception = '%s'"%(e),DEBUG,True)
    return False

def win_detect_openvpn_version(DEBUG,OPENVPN_DIR,OVPN_LATEST_BUILT = None, OVPN_LATEST_BUILT_TIMESTAMP = 0):
    try:
        debug(1,"[openvpn.py] def win_detect_openvpn_version()",DEBUG,True)
        if OVPN_LATEST_BUILT == None:
            OVPN_LATEST_BUILT = values(DEBUG)["BUILT"].split()
        else:
            OVPN_LATEST_BUILT = OVPN_LATEST_BUILT.split()
        if OVPN_LATEST_BUILT_TIMESTAMP == 0:
            OVPN_LATEST_BUILT_TIMESTAMP = values(DEBUG)["TIMESTAMP"]
        DATA = win_get_openvpn_version(DEBUG,OPENVPN_DIR)
        if not DATA == False:
            OVPN_VERSION = DATA[0]
            OVPN_BUILT = DATA[1]
        else:
            debug(1,"[openvpn.py] def w_d_o_v: failed, DATA == False",DEBUG,True)
            return False
        debug(1,"[openvpn.py] def w_d_o_v: myOVPN_VERSION = %s, my OVPN_BUILT = %s, my OVPN_LATEST_BUILT = %s" % (OVPN_VERSION,OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
        
        if len(OVPN_BUILT) == 3 and len(OVPN_LATEST_BUILT) == 3:
            STR1 = str(OVPN_BUILT[0]+OVPN_BUILT[1]+OVPN_BUILT[2])
            STR2 = str(OVPN_LATEST_BUILT[0]+OVPN_LATEST_BUILT[1]+OVPN_LATEST_BUILT[2])
            if STR1 == STR2:
                debug(1,"[openvpn.py] def w_d_o_v: my OVPN_BUILT '%s' == OVPN_LATEST_BUILT '%s': True"%(OVPN_BUILT,OVPN_LATEST_BUILT),DEBUG,True)
                return True
            else:
                months = { 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12 }
                built_mon = OVPN_BUILT[0]
                built_month_int = months[built_mon]
                built_day = int(OVPN_BUILT[1])
                built_year = int(OVPN_BUILT[2])
                built_timestamp = int(time.mktime(datetime(built_year,built_month_int,built_day,0,0).timetuple()))
                if built_timestamp >= OVPN_LATEST_BUILT_TIMESTAMP:
                    debug(1,"[openvpn.py] def w_d_o_v: my built_timestamp '%s' >= OVPN_LATEST_BUILT_TIMESTAMP '%s': True" % (built_timestamp,OVPN_LATEST_BUILT_TIMESTAMP),DEBUG,True)
                    return True
                else:
                    debug(1,"[openvpn.py] def w_d_o_v: my built_timestamp '%s' < OVPN_LATEST_BUILT_TIMESTAMP '%s': False" % (built_timestamp,OVPN_LATEST_BUILT_TIMESTAMP),DEBUG,True)
        else:
            debug(1,"[openvpn.py] def w_d_o_v: OVPN_VERSION '%s' failed"%(OVPN_VERSION),DEBUG,True)
        return False
    except Exception as e:
        debug(1,"[openvpn.py] def w_d_o_v: failed, exception = '%s'"%(e),DEBUG,True)
    debug(1,"[openvpn.py] def w_d_o_v: return False",DEBUG,True)
    return False

def list_openvpn_files(DEBUG,OPENVPN_DIR,type):
    debug(1,"[openvpn.py] def list_openvpn_files()",DEBUG,True)
    try:
        dir = OPENVPN_DIR
        if os.path.exists(dir):
            content = os.listdir(dir)
            list = []
            for file in content:
                if file.endswith(type):
                    list.append(file)
            if len(list) >= 1:
                debug(1,"[openvpn.py] def list_openvpn_files: dir '%s', files = '%s', list = '%s'" % (dir,len(list),list),DEBUG,True)
                return list
        else:
            debug(1,"[openvpn.py] def list_openvpn_files: dir '%s' not found!" % (dir),DEBUG,True)
    except:
        debug(1,"[openvpn.py] def list_openvpn_files: failed",DEBUG,True)
    debug(1,"[openvpn.py] def list_openvpn_files: return False",DEBUG,True)
    return False

def check_files(DEBUG,OPENVPN_DIR):
    debug(1,"[openvpn.py] def check_files()",DEBUG,True)
    # search signtool
    if not signtool.find_signtool(DEBUG) == False:
        # check signatures
        files1 = list_openvpn_files(DEBUG,OPENVPN_DIR,".exe")
        files2 = list_openvpn_files(DEBUG,OPENVPN_DIR,".dll")
        files = files1 + files2
        if files == False:
            return False
        for file in files:
            filepath = "%s\\%s" % (OPENVPN_DIR,file)
            if not signtool.signtool_verify(DEBUG,filepath):
                bakfile = "%s.codesign_error" % filepath
                try:
                    os.rename(filepath,bakfile)
                except Exception as e:
                    debug(1,"[openvpn.py] def check_files: os.rename(%s,%s) failed"%(filepath,bakfile),DEBUG,True)
                if os.path.isfile(filepath):
                    return False
        # all file signatures verified
        return True
    debug(1,"[openvpn.py] def check_files: failed",DEBUG,True)
    return False

def check_file_hashs(DEBUG,OPENVPN_DIR,type):
    debug(1,"[openvpn.py] def check_file_hashs(%s)"%(type),DEBUG,True)
    types = [ ".exe", ".dll" ]
    if not type in types:
        debug(1,"[openvpn.py] def check_file_hashs: type '%s' invalid"%(type),DEBUG,True)
        return False
    try:
        content = list_openvpn_files(DEBUG,OPENVPN_DIR,type)
        if content == False:
            return False
        try:
            filename = values(DEBUG)["SETUP_FILENAME"]
            try:
                hashs = values(DEBUG)["OPENVPN_FILEHASHS"][filename]
            except:
                return False
            
        except:
            debug(2,"[openvpn.py] def check_file_hashs: filename/hashs failed",DEBUG,True)
            sys.exit()
        
        debug(2,"[openvpn.py] filename = '%s' hashs = '%s'"%(filename,hashs),DEBUG,True)
        for file in content:
            debug(2,"[openvpn.py] def check_file_hashs: file = '%s'" % (file),DEBUG,True)
            filepath = "%s\\%s" % (OPENVPN_DIR,file)
            hasha = hashings.hash_sha512_file(DEBUG,filepath)
            debug(2,"[openvpn.py] def check_file_hashs: hasha = '%s'" % (hasha),DEBUG,True)
            try:
                hashb = hashs[file]
            except:
                return False
            if hasha == hashb:
                debug(2,"[openvpn.py] def check_file_hashs: hash file = '%s' OK!" % (file),DEBUG,True)
            else:
                debug(1,"[openvpn.py] def check_file_hashs: hash file = '%s' failed" % (file),DEBUG,True)
                return False
        return True
    except:
        debug(1,"[openvpn.py] def check_file_hashs: failed",DEBUG,True)
        sys.exit()
        return False

"""
def upgrade_openvpn(DEBUG):
    pass

def load_openvpnbin_from_remote(self):
    pass

def verify_openvpnbin_dl(self):
    pass

def win_install_openvpn(self):
    pass

def extract_ovpn(self):
    pass

def win_select_openvpn(self):
    pass

def find_signtool(self):
    pass

def signtool_verify(self,file):
    pass
"""