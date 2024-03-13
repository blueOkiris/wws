@echo off

REM Set up environment. Does nothing if already installed
python -m virtualenv .venv
.\.venv\Scripts\pip install pyvda pystray

REM Actually run the script
.\.venv\Scripts\python wws.py

