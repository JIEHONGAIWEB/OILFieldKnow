@echo off
REM Start docs in background (no window): http://127.0.0.1:8000
REM Stop: run stop-docs.bat
cd /d "%~dp0"
set NO_MKDOCS_2_WARNING=1
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden -FilePath python -ArgumentList '-m','mkdocs','serve' -WorkingDirectory '%~dp0'"
echo Docs started: http://127.0.0.1:8000
start http://127.0.0.1:8000
