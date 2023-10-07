NOTEBOOK_ENV="venv"

cd ../

virtualenv $NOTEBOOK_ENV --clear

source venv/bin/activate

pip install -r requirements.txt