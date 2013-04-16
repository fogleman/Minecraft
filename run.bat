@echo off
echo Starting pyCraftr
c:\Python\python.exe %1 --disable-auto-save --disable-save %2 %3 %4 %5 %6 %7 %8 %9
del *.pyc 
del *.c
del *.h
del *.so
del thumbs.db