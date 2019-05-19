#!/bin/bash

source ./serverside/venv/bin/activate
python3 ./serverside/hackCU/manage.py runserver && ssh -R hackcuimagefacedetection:80:localhost:8000 serveo.net
