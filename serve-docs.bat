@echo off
REM 启动文档阅读器: http://127.0.0.1:8000
cd /d "%~dp0"
set NO_MKDOCS_2_WARNING=1
python -m mkdocs serve
