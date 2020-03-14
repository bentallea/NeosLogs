@echo OFF

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT

if %OS%==32BIT "%~dp0\bin\python-3.8.2-embed-win32\python.exe" %~dp0\bin\neos.py "%appdata%" %1 %2
if %OS%==64BIT "%~dp0\bin\python-3.8.2-embed-amd64\python.exe" %~dp0\bin\neos.py "%appdata%" %1 %2
