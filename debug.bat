@echo off
set SOURCEDIR=%~dp0.
call %SOURCEDIR%\set_dirs.bat %~1

echo run debug on %BITS% bits
echo PYEXE=%PYEXE%
REM pause

call %SOURCEDIR%\includes_to_appdata.bat

%PYEXE% %SOURCEDIR%\ovpn_client.py %~2

echo "hit to quit"
pause
