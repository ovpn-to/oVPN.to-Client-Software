# -*- coding: utf-8 -*-
from debug import debug
import platform
import time

# ATTENTION
# win32api include in py2exe 0.9.2.2 give a import error pywintypes with python3.4.4. To fix it edit the Hooks file from py2exe:
# C:\Program Files\Python34_64\Lib\site-packages\py2exe\hooks.py
# Comment Line 250 with #
# Now all works fine

from win32api import GetSystemMetrics, GetModuleHandle, PostQuitMessage, LoadResource
from win32con import SM_CXSMICON, SM_CYSMICON, CW_USEDEFAULT, IMAGE_ICON, IMAGE_BITMAP, IDI_INFORMATION, IDI_APPLICATION, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_DESTROY, WS_OVERLAPPED, WS_SYSMENU, WM_USER, RT_ICON
from win32gui import CreateIconFromResource, CreateWindow, DestroyWindow, LoadIcon, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY, RegisterClass, UnregisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

WINVER10 = False
if "Windows-10" in platform.platform():
	WINVER10 = True

class notify:
	def __init__(self):

		message_map = { WM_DESTROY: self.send_notify_destroy }
		wc = WNDCLASS()
		self.hinst = wc.hInstance = GetModuleHandle(None)
		wc.lpszClassName = str("PythonTaskbar")
		wc.lpfnWndProc = message_map
		self.classAtom = RegisterClass(wc)

	def send_notify(self,DEBUG,TRAYSIZE,DEV_DIR,text,title):
		try:
			
			while not self.isDestroyed() == True:
				sleep(0.01)
			self.destroyed = False
			debug(222,"[win_notification.py] def send_notify: [Win10 = %s]" % (WINVER10),DEBUG,True)
			style = WS_OVERLAPPED | WS_SYSMENU
			self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,0, 0, CW_USEDEFAULT,CW_USEDEFAULT,0, 0, self.hinst, None)
			UpdateWindow(self.hwnd)

			try:
				RT_ICON_SIZE = 11
				#RT_ICON_SIZE = 15
				if TRAYSIZE == 32 or WINVER10 == True:
					RT_ICON_SIZE = 10
					#RT_ICON_SIZE = 14
				""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648060(v=vs.85).aspx """
				hicon = CreateIconFromResource(LoadResource(None, RT_ICON, RT_ICON_SIZE), True)
				debug(222,"[win_notification.py] def send_notify: CreateIconFromResource() #1",DEBUG,True)
			except Exception as e:
				debug(222,"[win_notification.py] def send_notify: CreateIconFromResource() #1 failed, exception = '%s'"%(e),DEBUG,True)
				try:
					raise Exception
					icon_path = "%s\\else\\app_icons\\shield_exe.ico" % (DEV_DIR)
					#icon_path = "%s\\else\\app_icons\\app_layer.ico" % (DEV_DIR)
					#icon_path = "%s\\else\\app_icons\\shield_exe_48.ico" % (DEV_DIR)
					#icon_path = "%s\\else\\app_icons\\shield_exe_64.ico" % (DEV_DIR)
					#icon_path = "%s\\else\\some_icons\\shield_256.bmp" % (DEV_DIR)
					#icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
					icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
					ico_x = GetSystemMetrics(SM_CXSMICON)
					ico_y = GetSystemMetrics(SM_CYSMICON)
					debug(1,"[win_notification.py] def send_notify: ico_x = '%s' ico_y = '%s'"%(ico_x,ico_y),DEBUG,True)
					""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648045(v=vs.85).aspx """
					hicon = LoadImage(self.hinst, icon_path,IMAGE_ICON, ico_x, ico_y, icon_flags)
					debug(222,"[win_notification.py] def send_notify: LoadImage() #2",DEBUG,True)
				except Exception as e:
					debug(222,"[win_notification.py] def send_notify: LoadImage() #2 failed, exception = '%s'"%(e),DEBUG,True)
					try:
						""" https://msdn.microsoft.com/en-us/library/windows/desktop/ms648072(v=vs.85).aspx """
						hicon = LoadIcon(0, IDI_INFORMATION)
						debug(222,"[win_notification.py] def send_notify: LoadIcon() #3",DEBUG,True)
					except Exception as e:
						debug(222,"[win_notification.py] def send_notify: LoadIcon() #3 failed, exception = '%s'"%(e),DEBUG,True)
						return False
			
			flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
			nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Tooltip")
			
			anyreturn = Shell_NotifyIcon(NIM_ADD, nid)
			debug(222,"[win_notification.py] def send_notify: Shell_NotifyIcon() #1 returned = '%s'"%(anyreturn),DEBUG,True)
			
			anyreturn = Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,WM_USER + 20,hicon, "Balloon Tooltip", text, 200,title))
			debug(222,"[win_notification.py] def send_notify: Shell_NotifyIcon() #2 returned = '%s'"%(anyreturn),DEBUG,True)
			
			if WINVER10 == False:
				time.sleep(10)
			
			anyreturn = DestroyWindow(self.hwnd)
			debug(222,"[win_notification.py] def send_notify: DestroyWindow() returned = '%s'"%(anyreturn),DEBUG,True)

			#anyreturn = UnregisterClass(self.classAtom, self.hinst)
			#debug(1,"[win_notification.py] def send_notify: UnregisterClass() returned = '%s'"%(anyreturn),DEBUG,True)

			debug(1,"[win_notification.py] def send_notify: [Win10 = %s] return" % (WINVER10),DEBUG,True)
			self.destroyed = True
			return None
		except Exception as e:
			debug(1,"[win_notification.py] def send_notify: failed, exception = '%s'"%(e),DEBUG,True)

	def send_notify_destroy(self, hwnd, msg, wparam, lparam):
		nid = (self.hwnd, 0)
		Shell_NotifyIcon(NIM_DELETE, nid)
		PostQuitMessage(0)
		debug(222,"[win_notification.py] def send_notify_destroy: return",True,True)
		return None

	def isDestroyed(self):
		try:
			return self.destroyed
		except:
			return True
