@echo off

set NOTEBOOK_ENV=venv

cd ..\..\notebook

call ..\%NOTEBOOK_ENV%\Scripts\activate

start "" /B jupyter notebook