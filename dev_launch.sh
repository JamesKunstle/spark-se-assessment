#!/bin/bash

export FLASK_APP=project.server
export APP_SETTINGS="project.server.config.DevelopmentConfig"
# from https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date/17776558
flask db init
flask db migrate
flask db upgrade
flask run --host=0.0.0.0 --port=5000
#flask run
