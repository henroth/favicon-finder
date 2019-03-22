# Prerequisites
Tested on Ubunutu 18.04

    sudo apt-get install python3 python3-pip python3-venv
    python3 -m pip install --user --upgrade pip
    
# Startup

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=application.py
    run flask

# TODO
Investigate ConnectionErrors when populating the DB there seem to be more than I would expect
Investigate favicon results having query parameters, am I constructing them wrong?
