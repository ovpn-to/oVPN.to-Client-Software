@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)

IF EXIST "%DISTDIR%\ovpn_client.exe" (set BINARY="%DISTDIR%\ovpn_client.exe")

IF DEFINED BINARY (
	IF DEFINED SIGNTOOLCMD1 (%SIGNTOOLCMD1% %BINARY%)
	IF DEFINED SIGNTOOLCMD2 (%SIGNTOOLCMD2% %BINARY%)
	IF DEFINED SIGNTOOLCMD3 (%SIGNTOOLCMD3% %BINARY%)
	IF DEFINED SIGNTOOLCMD4 (%SIGNTOOLCMD4% %BINARY%)
	IF DEFINED SIGNTOOLVERI (
		echo VERIFY: %BINARY%
		pause
		%SIGNTOOLVERI% %BINARY%
		pause
		)
	)

echo SIGN_EXE complete
pause