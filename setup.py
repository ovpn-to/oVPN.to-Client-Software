# -*- coding: utf-8
import sys
#sys.setrecursionlimit(3000)
from distutils.core import setup
import py2exe
import os, site, shutil, time
import struct
import release_version

BITS = struct.calcsize("P") * 8
appversion = release_version.setup_data()["version"]
cpu = 'x86'
inno = 'win32'
crt = 'Microsoft.VC100.CRT_win32'
if BITS == 64:
    cpu = 'amd64'
    inno = 'win64'
    crt = 'Microsoft.VC100.CRT_win64'

manifest = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" xmlns:asmv3="urn:schemas-microsoft-com:asm.v3" manifestVersion="1.0">
    <assemblyIdentity
        version="{APPVERSION}"
        processorArchitecture="{CPU}"
        name="oVPN.to Client"
        type="win32"
    />
    <description>oVPN.to Client</description>
    <asmv3:trustInfo xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
        <asmv3:security>
            <asmv3:requestedPrivileges>
                <asmv3:requestedExecutionLevel
                level="requireAdministrator"
                uiAccess="false" />
            </asmv3:requestedPrivileges>
        </asmv3:security>
    </asmv3:trustInfo>
    <asmv3:application>
        <asmv3:windowsSettings xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">'
            <dpiAware>true/PM</dpiAware>
        </asmv3:windowsSettings>
    </asmv3:application>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="{CPU}"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
</assembly>
'''.format(APPVERSION=appversion, CPU=cpu)

SOURCEDIR = os.getcwd()
DIST_DIR = "%s\\%s" % (SOURCEDIR,release_version.setup_data()["DIST_DIR1"])
BUILD_DIR = "%s\\build%s" % (SOURCEDIR,BITS)

site_dir = site.getsitepackages()[1] 
include_dll_path = os.path.join(site_dir, 'gnome')

gtk_dirs_to_include = ['etc\\fonts', 'lib\\gtk-3.0', 'lib\\girepository-1.0', 'share\\glib-2.0', 'share\\icons\\hicolor', 'share\\icons\\Adwaita\\scalable', 'share\\icons\\Adwaita\\32x32', 'share\\locale']

gtk_dlls = []
tmp_dlls = []
tmpdir = SOURCEDIR+"\\tmp"
tmpdlldir = tmpdir+"\\dll"

if not os.path.exists(tmpdlldir):
    os.makedirs(tmpdlldir)

for dll in os.listdir(include_dll_path):
    if dll.lower().endswith('.dll'):
        gtk_dlls.append(os.path.join(include_dll_path, dll))
        tmp_dlls.append(os.path.join(tmpdlldir, dll))

for dll in gtk_dlls:
    shutil.copy(dll, tmpdlldir)

setup_dict = dict(
    data_files = [('',['includes/'+crt+'/msvcp100.dll','includes/'+crt+'/msvcr100.dll']),],
    zipfile = 'ovpn_client.lib',
    windows=[
        {
            "version":release_version.setup_data()["version"],
            "product_name":release_version.setup_data()["name"],
            "description":release_version.setup_data()["description"],
            "script":release_version.setup_data()["script"],
            "icon_resources" : [(1, 'else\\app_icons\\shield_exe.ico')],
            "copyright" : "Copyright %s" % (release_version.setup_data()["copyright"]),
            "company_name" : "%s %s" % (release_version.org_data()["ORG"],release_version.org_data()["ADD"]),
            "other_resources" : [(24,1,manifest)],
        }
    ],
    options={
        'build': {'build_base': BUILD_DIR },
        'py2exe': {
        'dist_dir': DIST_DIR,
        'bundle_files' : 3,
        'optimize'     : 2,
        'skip_archive' : False,
        'compressed'   : False,
        'unbuffered'   : False,
        'includes'     : release_version.setup_data()["py2exe_includes"],
        'excludes'     : release_version.setup_data()["py2exe_excludes"],
        'packages'     : [ 'gi' ],
        'dll_excludes' : release_version.setup_data()["dll_excludes"],
        }
    }
)

lines = list()
lines.append(';!!!DONT EDIT THIS FILE MANUALLY, IT WILL BE OVERWRITTEN IN NEXT BUILD RUN!!!')
lines.append('#define AppExeName "%s"' % release_version.setup_data()["exename"])
lines.append('#define Version "%s"' % release_version.version_data()["VERSION"])
lines.append('#define AppName "%s"' % release_version.version_data()["NAME"])
lines.append('#define AppDir "%s"' % release_version.version_data()["NAME"])
lines.append('#define AppPublisher "%s %s"' % (release_version.org_data()["ORG"],release_version.org_data()["ADD"]))
lines.append('#define AppURL "%s"' % release_version.org_data()["SITE"])
lines.append('[Setup]')
lines.append('AppVersion=v{#Version}-gtk3_%s' % inno)
lines.append('AppVerName={#AppName} v{#Version}-gtk3_%s' % inno)
lines.append('AppSupportURL=%s' % release_version.org_data()["SUPPORT"])
lines.append('AppUpdatesURL=%s' % release_version.org_data()["UPDATES"])
lines.append('AppCopyright=Copyright %s'  % release_version.setup_data()["copyright"])
lines.append('OutputBaseFilename=ovpn_client_v{#Version}-gtk3_%s_setup' % inno)
if release_version.version_data()["SIGN"] == True:
    #lines.append('SignTool=signtool1')
    lines.append('SignTool=signtool2')
    #lines.append('SignTool=signtool3')
    #lines.append('SignTool=signtool4')
if inno == "win32":
    lines.append('DefaultDirName={pf}\{#AppDir}')
else:
    lines.append('DefaultDirName={pf64}\{#AppDir}')
if release_version.version_data()["SIGN"] == True:
    lines.append('SignedUninstaller=yes')
else:
    lines.append('SignedUninstaller=no')
lines.append('Compression=lzma2/max')
lines.append('SolidCompression=yes')
lines.append('AppId={{991F58FC-8D40-4B45-B434-6A10AAC12FBA}')
lines.append('AppName={#AppName}')
lines.append('AppMutex={#AppExeName},Global\{#AppExeName}')
lines.append('SetupMutex={#AppDir},Global\{#AppDir}')
lines.append('AppPublisher={#AppPublisher}')
lines.append('AppContact={#AppPublisher}')
lines.append('AppPublisherURL={#AppURL}')
lines.append('AppReadmeFile={#AppURL}')
lines.append('VersionInfoVersion=0.{#Version}')
lines.append('DefaultGroupName={#AppName}')
lines.append('AllowNoIcons=yes')
lines.append('OutputDir=.')
lines.append('SetupIconFile=else\\app_icons\shield_exe.ico')
lines.append('WizardImageFile=else\\app_icons\shield_exe_2.bmp')
lines.append('WizardSmallImageFile=else\\app_icons\shield_exe.bmp')
lines.append('WizardImageStretch=no')
lines.append('UninstallDisplayIcon={app}\{#AppExeName}')
lines.append("""Uninstallable=not IsTaskSelected('portablemode')""")
lines.append('DisableDirPage=no')
lines.append('LicenseFile=LICENSE')
lines.append('LanguageDetectionMethod=uilanguage')
lines.append('ShowLanguageDialog=auto')
lines.append('[Tasks]')
lines.append('Name: portablemode; Description: "Portable Mode"; Flags: unchecked')
lines.append('[InstallDelete]')
lines.append('Type: files; Name: "{userdesktop}\oVPN.to Client.lnk";')
lines.append('Type: files; Name: "{commondesktop}\oVPN.to Client.lnk";')
lines.append('Type: filesandordirs; Name: {app}\dns\;')
lines.append('Type: filesandordirs; Name: {app}\etc\;')
lines.append('Type: filesandordirs; Name: {app}\lib\;')
lines.append('Type: filesandordirs; Name: {app}\locale\;')
lines.append('Type: filesandordirs; Name: {app}\share\;')
lines.append('Type: filesandordirs; Name: {app}\ico\;')
lines.append('Type: files; Name: {app}\*.dll;')
lines.append('Type: files; Name: {app}\*.pyd;')
lines.append('Type: files; Name: {app}\*.lib;')
lines.append('Type: files; Name: {app}\*.pem;')
lines.append('Type: files; Name: {app}\{#AppExeName};')
lines.append('[Languages]')
lines.append('Name: "english"; MessagesFile: "compiler:Default.isl"')
lines.append('Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"')
lines.append('Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"')
lines.append('Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"')
lines.append('Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"')
lines.append('Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"')
lines.append('Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"')
lines.append('Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"')
lines.append('Name: "french"; MessagesFile: "compiler:Languages\French.isl"')
lines.append('Name: "german"; MessagesFile: "compiler:Languages\German.isl"')
lines.append('Name: "greek"; MessagesFile: "compiler:Languages\Greek.isl"')
lines.append('Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"')
lines.append('Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"')
lines.append('Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"')
lines.append('Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"')
lines.append('Name: "norwegian"; MessagesFile: "compiler:Languages\\Norwegian.isl"')
lines.append('Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"')
lines.append('Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"')
lines.append('Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"')
lines.append('Name: "scottishgaelic"; MessagesFile: "compiler:Languages\ScottishGaelic.isl"')
lines.append('Name: "serbiancyrillic"; MessagesFile: "compiler:Languages\SerbianCyrillic.isl"')
lines.append('Name: "serbianlatin"; MessagesFile: "compiler:Languages\SerbianLatin.isl"')
lines.append('Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"')
lines.append('Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"')
lines.append('Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"')
lines.append('Name: "ukrainian"; MessagesFile: "compiler:Languages\\Ukrainian.isl"')
lines.append('[Tasks]')
lines.append('Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked')
lines.append('[Components]')
lines.append('Name: "main"; Description: "%s"; Types: full compact custom; Flags: fixed' % release_version.version_data()["NAME"])
lines.append('Name: "languages"; Description: "Languages"; Types: full')
lines.append('Name: "languages\deutsch"; Description: "Deutsch"; Types: full')
lines.append('Name: "languages\espanol"; Description: "Espanol"; Types: full')
lines.append('Name: "languages\\french"; Description: "French"; Types: full')
lines.append('Name: "themes"; Description: "Themes"; Types: full')
lines.append('Name: "themes\AdwaitaDark"; Description: "AdwaitaDark"; Types: full')
lines.append('Name: "themes\FlatRemixOS"; Description: "FlatRemixOS"; Types: full')
lines.append('Name: "themes\Greybird"; Description: "Greybird"; Types: full')
lines.append('Name: "themes\Windows"; Description: "Windows"; Types: full')
lines.append('[Files]')
lines.append('Source: "%s\\*"; DestDir: "{app}"; Flags:replacesameversion' % (DIST_DIR))
lines.append('Source: "%s\\appdata\*"; DestDir: "{app}\\appdata\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\etc\*"; DestDir: "{app}\\etc\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\lib\*"; DestDir: "{app}\\lib\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\share\\glib-2.0\*"; DestDir: "{app}\\share\\glib-2.0\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\share\\icons\*"; DestDir: "{app}\\share\\icons\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\share\\locale\\locale.alias"; DestDir: "{app}\share\locale\"; Flags:replacesameversion' % (DIST_DIR))
lines.append('Source: "%s\\share\\locale\\en\*"; DestDir: "{app}\\share\\locale\\en\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\share\\themes\\Adwaita\*"; DestDir: "{app}\\share\\themes\\Adwaita\"; Flags:replacesameversion recursesubdirs' % (DIST_DIR))
lines.append('Source: "%s\\locale\\de\*"; DestDir: "{app}\locale\de\"; Flags:replacesameversion recursesubdirs; Components: languages\deutsch' % (DIST_DIR))
lines.append('Source: "%s\\share\\locale\\de\*"; DestDir: "{app}\\share\\locale\\de\"; Flags:replacesameversion recursesubdirs; Components: languages\deutsch' % (DIST_DIR))
lines.append('Source: "%s\\locale\\es\*"; DestDir: "{app}\\locale\\es\"; Flags:replacesameversion recursesubdirs; Components: languages\espanol' % (DIST_DIR))
lines.append('Source: "%s\\share\\locale\\es\*"; DestDir: "{app}\\share\\locale\\es\"; Flags:replacesameversion recursesubdirs; Components: languages\espanol' % (DIST_DIR))
lines.append('Source: "%s\\locale\\fr\*"; DestDir: "{app}\\locale\\fr\"; Flags:replacesameversion recursesubdirs; Components: languages\\french' % (DIST_DIR))
lines.append('Source: "%s\\share\\locale\\fr\*"; DestDir: "{app}\\share\\locale\\fr\"; Flags:replacesameversion recursesubdirs; Components: languages\\french' % (DIST_DIR))
lines.append('Source: "%s\\share\\themes\\Adwaita-dark\*"; DestDir: "{app}\\share\\themes\\Adwaita-dark\"; Flags:replacesameversion recursesubdirs; Components: themes\AdwaitaDark' % (DIST_DIR))
lines.append('Source: "%s\\share\\themes\\Flat-Remix-OS\*"; DestDir: "{app}\\share\\themes\\Flat-Remix-OS\"; Flags:replacesameversion recursesubdirs; Components: themes\FlatRemixOS' % (DIST_DIR))
lines.append('Source: "%s\\share\\themes\\Greybird\*"; DestDir: "{app}\share\\themes\\Greybird\"; Flags:replacesameversion recursesubdirs; Components: themes\Greybird' % (DIST_DIR))
lines.append('Source: "%s\\share\\themes\\MS-Windows\*"; DestDir: "{app}\share\\themes\\MS-Windows\"; Flags:replacesameversion recursesubdirs; Components: themes\Windows' % (DIST_DIR))
lines.append('[Icons]')
lines.append('Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"')
lines.append('Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"')
lines.append('Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon')
lines.append('[Registry]')
lines.append('Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: string; ValueName: "{app}\{#AppExeName}"; ValueData: "~ HIGHDPIAWARE"; Flags: noerror uninsdeletevalue')

innoscript = "%s\\inno_setup.iss" % (SOURCEDIR)
ind = open(innoscript, "wt")
for line in lines:
    ind.write("%s\n"%(line))
ind.close()
if not os.path.exists(innoscript):
    print(".inno file not created")
    sys.exit()


#setup(**setup_dict)
setup(**setup_dict)

if not os.path.exists(DIST_DIR):
    os.makedirs(DIST_DIR)

for dll in tmp_dlls:
    shutil.copy(dll, DIST_DIR)
    os.remove(dll)

for d in gtk_dirs_to_include:
    shutil.copytree(os.path.join(site_dir, 'gnome', d), os.path.join(DIST_DIR, d))