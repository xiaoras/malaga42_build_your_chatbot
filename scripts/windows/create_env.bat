@echo off

set NOTEBOOK_ENV=venv

cd ..\..

virtualenv %NOTEBOOK_ENV% --clear

call venv\Scripts\activate

pip install -r requirements.txt