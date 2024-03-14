@echo off

REM Set up environment. Does nothing if already installed
python -m virtualenv .venv
.\.venv\Scripts\pip install pyvda==0.4.3 pystray==0.19.5

REM Actually run the script
.\.venv\Scripts\python wws.py

