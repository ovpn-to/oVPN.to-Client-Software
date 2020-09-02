@echo off
IF NOT DEFINED EXESTRING (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED DISTDIR (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT DEFINED SIGNTOOL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %SIGNTOOL% (echo %SIGNTOOL% NOT FOUND && PAUSE && EXIT)
IF NOT DEFINED CERTUTIL (echo "DO NOT RUN THIS FILE DIRECTLY" && PAUSE && EXIT)
IF NOT EXIST %CERTUTIL% (echo %CERTUTIL% NOT FOUND && PAUSE && EXIT)

for %%v in ("%DISTDIR%\*.dll") do (
    for %%A in ("%%v") do (
        IF NOT "%%~nxA" == "msvcr100.dll" IF NOT "%%~nxA" == "msvcp100.dll" (
            IF NOT EXIST %DLLDIR_U%\%%~nxA (
                echo copy /Y "%%v" "%DLLDIR_U%\"
                copy /Y "%%v" "%DLLDIR_U%\"
            ) else (
                setlocal EnableDelayedExpansion
                set /a COUNTER=1
                for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %%v sha1"') do (
                    IF !COUNTER! EQU 2 set "SHA1_DIST=%%D"
                    set /a COUNTER+=1
                )
                echo !SHA1_DIST: =!
                set /a COUNTER=1
                for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %DLLDIR_U%\%%~nxA sha1"') do (
                    IF !COUNTER! EQU 2 set "SHA1_U=%%D"
                    set /a COUNTER+=1
                )
                echo !SHA1_U: =!
                IF "!SHA1_DIST: =!" NEQ "!SHA1_U: =!" (
                    del "%DLLDIR_U%\%%~nxA" 2> nul
                    del "%DLLDIR_S%\%%~nxA" 2> nul
                    echo SHA1 check Failed, copy new File
                    echo copy /Y "%%v" "%DLLDIR_U%\"
                    copy /Y "%%v" "%DLLDIR_U%\"
                )
                endlocal
            )
            IF NOT EXIST %DLLDIR_S%\%%~nxA (
                timeout /t 20
                IF DEFINED SIGNTOOLCMD2 (%SIGNTOOLCMD2% "%%v")
                IF DEFINED SIGNTOOLVERI (
                    echo VERIFY: %%v
                    %SIGNTOOLVERI% "%%v"
                )
                IF NOT EXIST %DLLDIR_S% (
                    echo !!ATTENTION!! Create %DLLDIR_S% to save signed DLL
                ) else (
                    echo copy /Y "%%v" "%DLLDIR_S%\"
                    copy /Y "%%v" "%DLLDIR_S%\"
                )
            ) else (
                echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
                copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
            )
        )
    )
)

for %%v in ("%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\*.dll") do (
    for %%A in ("%%v") do (
        IF NOT EXIST %DLLDIR_U%\%%~nxA (
            echo copy /Y "%%v" "%DLLDIR_U%\"
            copy /Y "%%v" "%DLLDIR_U%\"
        ) else (
            setlocal EnableDelayedExpansion
            set /a COUNTER=1
            for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %%v sha1"') do (
                IF !COUNTER! EQU 2 set "SHA1_DIST=%%D"
                set /a COUNTER+=1
            )
            echo !SHA1_DIST: =!
            set /a COUNTER=1
            for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %DLLDIR_U%\%%~nxA sha1"') do (
                IF !COUNTER! EQU 2 set "SHA1_U=%%D"
                set /a COUNTER+=1
            )
            echo !SHA1_U: =!
            IF "!SHA1_DIST: =!" NEQ "!SHA1_U: =!" (
                del "%DLLDIR_U%\%%~nxA" 2> nul
                del "%DLLDIR_S%\%%~nxA" 2> nul
                echo SHA1 check Failed, copy new File
                echo copy /Y "%%v" "%DLLDIR_U%\"
                copy /Y "%%v" "%DLLDIR_U%\"
            )
            endlocal
        )
        IF NOT EXIST %DLLDIR_S%\%%~nxA (
            timeout /t 20
            IF DEFINED SIGNTOOLCMD2 (%SIGNTOOLCMD2% "%%v")
            IF DEFINED SIGNTOOLVERI (
                echo VERIFY: %%v
                %SIGNTOOLVERI% "%%v"
            )
            IF NOT EXIST %DLLDIR_S% (
                echo !!ATTENTION!! Create %DLLDIR_S% to save signed DLL
            ) else (
                echo copy /Y "%%v" "%DLLDIR_S%\"
                copy /Y "%%v" "%DLLDIR_S%\"
            )
        ) else (
            echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\"
            copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\lib\gtk-3.0\3.0.0\theming-engines\"
        )
    )
)

for %%v in ("%DISTDIR%\*.pyd") do (
    for %%A in ("%%v") do (
        IF NOT EXIST %DLLDIR_U%\%%~nxA (
            copy /Y "%%v" "%DLLDIR_U%\"
        ) else (
            setlocal EnableDelayedExpansion
            set /a COUNTER=1
            for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %%v sha1"') do (
                IF !COUNTER! EQU 2 set "SHA1_DIST=%%D"
                set /a COUNTER+=1
            )
            echo !SHA1_DIST: =!
            set /a COUNTER=1
            for /F "tokens=* delims=" %%D in ('"%CERTUTIL% -hashfile %DLLDIR_U%\%%~nxA sha1"') do (
                IF !COUNTER! EQU 2 set "SHA1_U=%%D"
                set /a COUNTER+=1
            )
            echo !SHA1_U: =!
            IF "!SHA1_DIST: =!" NEQ "!SHA1_U: =!" (
                del "%DLLDIR_U%\%%~nxA" 2> nul
                del "%DLLDIR_S%\%%~nxA" 2> nul
                echo SHA1 check Failed, copy new File
                echo copy /Y "%%v" "%DLLDIR_U%\"
                copy /Y "%%v" "%DLLDIR_U%\"
            )
            endlocal
        )
        IF NOT EXIST %DLLDIR_S%\%%~nxA (
            timeout /t 20
            IF DEFINED SIGNTOOLCMD2 (%SIGNTOOLCMD2% "%%v")
            IF DEFINED SIGNTOOLVERI (
                echo VERIFY: %%v
                %SIGNTOOLVERI% "%%v"
            )
            IF NOT EXIST %DLLDIR_S% (
                echo !!ATTENTION!! Create %DLLDIR_S% to save signed DLL
            ) else (
                echo copy /Y "%%v" "%DLLDIR_S%\"
                copy /Y "%%v" "%DLLDIR_S%\"
            )
        ) else (
            echo copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
            copy /Y "%DLLDIR_S%\%%~nxA" "%DISTDIR%\"
        )
    )
)

echo SIGN_DLL complete
