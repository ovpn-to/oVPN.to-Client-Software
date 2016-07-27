# -*- coding: utf-8 -*-
#
# HASH_DLLS

import os
import sys
import time
import json
import types
import hashlib
import threading
import subprocess

if len(sys.argv) > 1:
	if sys.argv[1] == "32":
		BITS = 32
	elif sys.argv[1] == "64":
		BITS = 64
	else:
		print "HASH_DLLS: missing bits"
		sys.exit()

class HASH_DLLS:
	def __init__(self):
		if self.self_vars():
			if os.path.isfile(self.DLL_DBF_HASH_UNSIGNED):
				if self.load_hash_dbf():
					if self.verify_files():
						pass
			else:
				if self.hash_files():
					if self.write_hash_dbf():
						sys.exit()
		else:
			print "init failed"
			sys.exit()

	def self_vars(self):
		self.HASHS_DB = {}
		self.DLL_DIR = "includes\\DLL\\%s" % (BITS)
		self.DLL_DIR_SIGNED = "%s\\signed" % (self.DLL_DIR)
		self.DLL_DIR_UNSIGNED = "%s\\unsigned" % (self.DLL_DIR)
		self.DLL_DBF_HASH_SIGNED = "%s\\dll_hashs_signed.json" % (self.DLL_DIR)
		self.DLL_DBF_HASH_UNSIGNED = "%s\\dll_hashs_unsigned.json" % (self.DLL_DIR)
		
		self.DLL_DIRS = { "UNSIGNED":self.DLL_DIR_UNSIGNED,"SIGNED":self.DLL_DIR_SIGNED }
		self.DLL_HASH_DBS = { "UNSIGNED":self.DLL_DBF_HASH_UNSIGNED,"SIGNED":self.DLL_DBF_HASH_SIGNED }
		try:
			if not os.path.isdir(self.DLL_DIR):
				os.mkdir(self.DLL_DIR)
			
			if not os.path.isdir(self.DLL_DIR_SIGNED):
				os.mkdir(self.DLL_DIR_SIGNED)
			
			if not os.path.isdir(self.DLL_DIR_UNSIGNED):
				os.mkdir(self.DLL_DIR_UNSIGNED)
		except:
			print "could not create working dirs"
			sys.exit()
		print "def self_vars: return True"
		return True

	def load_hash_dbf(self):
		for key,file in self.DLL_HASH_DBS.items():
			if os.path.isfile(file):
				fp = open(file,"rb")
				HASHS_DB = {}
				HASHS_DB[key] = json.loads(fp.read())
				fp.close()
				if len(HASHS_DB[key]) > 0:
					self.HASHS_DB[key] = HASHS_DB[key]
					print "def load_hash_dbf: key '%s', file = '%s' len = '%s' OK" % (key,file,len(self.HASHS_DB[key]))
			else:
				print "def load_hash_dbf: key '%s', file = '%s' not found" % (key,file)
		return True

	def write_hash_dbf(self):
		for key,file in self.DLL_HASH_DBS.items():
			try:
				if len(self.HASHS_DB[key]) > 0:
					fp = open(file, "wb")
					fp.write(json.dumps(self.HASHS_DB[key], ensure_ascii=False))
					fp.close()
					print "def write_hash_dbf: write key '%s', file = '%s' OK" % (key,file)
			except:
				print "def write_hash_dbf: write key '%s', file = '%s' failed!" % (key,file)
				return False
		return True

	def hash_sha512_file(self,file):
		if os.path.isfile(file):
			hasher = hashlib.sha512()
			fp = open(file, 'rb')
			with fp as afile:
				buf = afile.read()
				hasher.update(buf)
			fp.close()
			hash = hasher.hexdigest()
			return hash

	def list_files(self,dir):
		files = []
		content = os.listdir(dir)
		for file in content:
			if file.endswith('.dll'):
				filepath = "%s\\%s" % (dir,file)
				files.append(filepath)
		return files

	def hash_files(self):
		for key,dir in self.DLL_DIRS.items():
			if os.path.exists(dir):
				print "def hash_files: dir = '%s'" % (dir)
				files = {}
				hash_files = self.list_files(dir)
				for file in hash_files:
					if os.path.isfile(file):
						hash = self.hash_sha512_file(file)
						if len(hash) == 128:
							print "def hash_files: hashed file = '%s'" % (file)
							file = file.split("\\")[-1]
							files[file] = hash
						else:
							print "def hash_files: filepath '%s' failed" % (filepath)
							sys.exit()
				self.HASHS_DB[key] = files
		return True

	def verify_files(self):
		for key,dir in self.DLL_DIRS.items():
			if os.path.exists(dir):
				print "\ndef verify_files: dir = '%s' vs. file '%s'" % (dir,self.DLL_HASH_DBS[key])
				notfound, verified, failed  = 0, 0, 0
				verify_files = self.list_files(dir)
				for file in verify_files:
					if os.path.isfile(file):
						hash = self.hash_sha512_file(file)
						file = file.split("\\")[-1]
						if self.HASHS_DB[key][file] == hash:
							verified += 1
							print "def verify_files: file = '%s' OK" % (file)
						else:
							failed += 1
							print "def verify_files: file = '%s' failed" % (file)
					else:
						notfound += 1
						print "def verify_files: file = '%s' notfound" % (file)

				print "def verify_files: key '%s' dir = '%s' notfound = '%s' failed = '%s' verified = '%s'" % (key, dir, notfound, failed, verified)

def app():
	HASH_DLLS()

if __name__ == "__main__":
	app()