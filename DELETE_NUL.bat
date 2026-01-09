@echo off
echo Deleting nul file in: %~dp0
del /f /q "\\?\%~dp0nul"
if exist "\\?\%~dp0nul" (
    echo Failed - try running as Administrator
) else (
    echo Success!
)
pause
