@echo off
REM Stop background docs server (port 8000)
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000 " ^| findstr LISTENING') do taskkill /F /PID %%p
echo Docs stopped
