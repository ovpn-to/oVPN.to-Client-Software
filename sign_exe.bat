@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED BINARY (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)

IF NOT EXIST %BINARY% (echo %BINARY% NOT FOUND FOR SIGNING && PAUSE && EXIT)

IF DEFINED SIGNTOOLCMD1 (%SIGNTOOLCMD1% %BINARY%)
IF DEFINED SIGNTOOLCMD2 (%SIGNTOOLCMD2% %BINARY%)
IF DEFINED SIGNTOOLCMD3 (%SIGNTOOLCMD3% %BINARY%)
IF DEFINED SIGNTOOLCMD4 (%SIGNTOOLCMD4% %BINARY%)

echo sign_exe.bat complete
