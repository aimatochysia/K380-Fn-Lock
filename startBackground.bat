@echo off
set "K380FnLock=K380-Fn-Lock.exe"
set "startupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Copy K380-Fn-Lock.exe to the startup folder
copy "%K380FnLock%" "%startupFolder%" >nul

exit /b
