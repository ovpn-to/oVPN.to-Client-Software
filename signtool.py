# -*- coding: utf-8 -*-
import os, subprocess

# .py file imports
from debug import debug
from debug import devmode
from debug import devdir
import hashings
import openvpn


def find_signtool(DEBUG):
    debug(1,"[signtool.py] def find_signtool()",DEBUG,True)
    try:
        BIN_DIR = os.getcwd()
        ARCH = openvpn.get_arch(DEBUG)
        
        exe64 = "signtool_w10sdk_x64.exe"
        signtool64 = "%s\\%s" % (BIN_DIR,exe64)
        signtoolhash64 = "e85d79cc617642f585cb9e4ad5dd919b8d15570a291bdd1e69fd38d4f278bc4b6f110329e8fa6948b7d516917cc2bde43532cde33e8c5e66355d0c97cfd7ebc2"
        
        exe32 = "signtool_w10sdk_x86.exe"
        signtool32 = "%s\\%s" % (BIN_DIR,exe32)
        signtoolhash32 = "233304669aefeec9ad5d19bd2dd5bb19ea35ce31da0b3aabe5ab859259608a58725fac5993637c9635e5912138d3eb477773351f0ee81cc3ce756d713163cf31"
        
        if ARCH == "x86_64":
            if os.path.isfile(signtool64):
                signtool = signtool64
                signtoolhash = signtoolhash64
            elif os.path.isfile(signtool32):
                signtool = signtool32
                signtoolhash = signtoolhash32
            else:
                signtool = "%s\\includes\\codesign\\%s" % (devdir(),exe64)
                signtoolhash = signtoolhash64
        else:
            signtool = signtool32
            signtoolhash = signtoolhash32
        
        if not os.path.isfile(signtool):
            debug(1,"[signtool.py] def signtool_verify_files: signtool '%s' not found"%(signtool),DEBUG,True)
            signtool = "%s\\includes\\codesign\\%s" % (devdir(),exe32)
            signtoolhash = signtoolhash32
        if os.path.isfile(signtool):
            hash = hashings.hash_sha512_file(DEBUG,signtool)
            if signtoolhash == hash:
                debug(1,"[signtool.py] def find_signtool: signtool = '%s'" % (signtool),DEBUG,True)
                return signtool
            else:
                debug(1,"[signtool.py] def find_signtool: signtoolhash failed",DEBUG,True)
        else:
            debug(1,"[signtool.py] def signtool_verify_files: signtool not found",DEBUG,True)
    except Exception as e:
        debug(1,"[signtool.py] def find_signtool: failed exception '%s'"%(e),DEBUG,True)
    return False

def signtool_verify(DEBUG,file):
    debug(1,"[signtool.py] def signtool_verify(%s)"%(file),DEBUG,True)
    signtool = find_signtool(DEBUG)
    if os.path.isfile(file):
        
        cscertsha1 = "029f2b420f1ca580fa90101aabef3aff96ae9076".upper()
        #if devmode() == True:
        #   cscertsha1 = "1234000012340000123400001234000012340000"
        verbose = "/q"
        if DEBUG == True:
            verbose = "/v"
        string1 = '"%s" verify %s /a /all /pa /tw /sha1 %s "%s"' % (signtool,verbose,cscertsha1,file)
        debug(1,"[signtool.py] def signtool_verify: string1 = '%s'"%(string1),DEBUG,True)
        exitcode1 = 1
        try:
            exitcode1 = subprocess.check_call("%s" % (string1),shell=True)
        except:
            pass
        if exitcode1 == 0:
            debug(1,"[signtool.py] def signtool_verify: file = '%s' signature verified"%(file),DEBUG,True)
            return True
        else:
            debug(1,"[signtool.py] def signtool_verify: file = '%s' signature failed"%(file),DEBUG,True)
            """
            # only check file is signed from same CA if DEVMODE is True
            if devmode() == False:
                return False
            else:
                return False
            """
            """
            debug(1,"[signtool.py] def signtool_verify: file = '%s' check signature CA hash"%(file),DEBUG,True)
            cacertsha1 = "21F94C255A8B20D21A323CA5ACB8EBF284E09037"
            string2 = '"%s" verify /v /a /all /pa /tw /ca %s "%s"' % (signtool,cacertsha1,file)
            """
            debug(1,"[signtool.py] def signtool_verify: file = '%s' check signature old hash"%(file),DEBUG,True)
            oldcscertsha1 = "21F94C255A8B20D21A323CA5ACB8EBF284E09037"
            string2 = '"%s" verify %s /a /all /pa /tw /sha1 %s "%s"' % (signtool,verbose,oldcscertsha1,file)
            
            debug(1,"[signtool.py] def signtool_verify: string2 = '%s'"%(string2),DEBUG,True)
            exitcode2 = 1
            try:
                exitcode2 = subprocess.check_call("%s" % (string2),shell=True)
            except:
                pass
            if exitcode2 == 0:
                debug(1,"[signtool.py] def signtool_verify: file = '%s' signature old hash verified"%(file),DEBUG,True)
                return True
            else:
                debug(1,"[signtool.py] def signtool_verify: file = '%s' signature old hash failed"%(file),DEBUG,True)
                return False
    else:
        debug(1,"[signtool.py] def signtool_verify(%s) not found"%(file),DEBUG,True)
        return False
