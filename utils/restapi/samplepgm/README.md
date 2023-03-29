# Rest-api sample programs

## Topology
   [FLASK-APP] ------ [CURL COMMAND]

## Pre-requistes

### Install Packages
* sudo apt install python3.10-venv

### Create virtual enviornment
* source .venv/bin/activate
* pip3 install flask
* pip3 install flask-sqlalchemy
* pip3 freeze > requirements.txt

## Running the application

### Running Flask package

* Set the Enviornment variable
```
   export FLASK_APP=application.py
   export FLASK_DEBUG=1
```

* Execute the db_install to add entries
``` python3.10 db_instantiation.py ```

* Run the Flask application
``` flask run```

## CURL COMMANDS

* GET :          curl  http://127.0.0.1:5000/drinks
* GET-SPECIFIC : curl  http://127.0.0.1:5000/drinks/1 
* POST :         curl -vX POST  http://127.0.0.1:5000/drinks -H "Content-Type: application/json" -d @juice_entry.json
* DELETE :       curl -X  DELETE http://127.0.0.1:5000/drinks/3
