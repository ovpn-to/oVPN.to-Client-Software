from distutils.core import setup
import py2exe
import sys, os, site, shutil

site_dir = site.getsitepackages()[1] 
include_dll_path = os.path.join(site_dir, 'gnome')

gtk_dirs_to_include = ['etc\\fonts', 'lib\\gtk-3.0', 'lib\\girepository-1.0', 'share\\glib-2.0', 'share\\icons\\hicolor', 'share\\icons\\Adwaita\\scalable', 'share\\icons\\Adwaita\\32x32', 'share\\locale']

gtk_dlls = []
tmp_dlls = []
cdir = os.getcwd() 
for dll in os.listdir(include_dll_path):
	if dll.lower().endswith('.dll'):
		gtk_dlls.append(os.path.join(include_dll_path, dll))
		tmp_dlls.append(os.path.join(cdir, dll))

for dll in gtk_dlls:
	shutil.copy(dll, cdir)

setup_dict = dict(
	version = "0.0.5.8",name = "oVPN.to Client for Windows",description = "oVPN.to Client",
	windows=[
		{
			'script':'ovpn_client.py',
			'icon_resources': [(1, 'else\\app_icons\\shield_exe.ico')],
			'uac_info': "requireAdministrator",
			'copyright': 'Copyright (C) 2016 oVPN.to',
			'company_name': 'oVPN.to Anonymous Services'
		}
	],
	options={
		'py2exe': {
		'bundle_files' : 3,
		'compressed'   : False,
		'unbuffered'   : False,
		'includes'     : [ 'gi','requests','cairo','types','os','platform','sys','hashlib','random','time','zipfile','subprocess','threading','socket','random','gettext','locale','_winreg','base64' ],
		'excludes'     : [  ],
		'optimize'     : 2,
		'packages'     : [ 'gi' ],
		'dll_excludes' : [ 'crypt32.dll','tcl85.dll', 'tk85.dll','DNSAPI.DLL','USP10.DLL','MPR.DLL','MSIMG32.DLL','API-MS-Win-Core-LocalRegistry-L1-1-0.dll','IPHLPAPI.DLL','w9xpopen.exe','mswsock.dll','powrprof.dll']
		}
	}
)


setup(**setup_dict)
setup(**setup_dict)

dest_dir = os.path.join(cdir, 'dist')

if not os.path.exists(dest_dir):
	os.makedirs(dest_dir)

for dll in tmp_dlls:
	shutil.copy(dll, dest_dir)
	os.remove(dll)

for d in gtk_dirs_to_include:
	shutil.copytree(os.path.join(site_dir, 'gnome', d), os.path.join(dest_dir, d))
