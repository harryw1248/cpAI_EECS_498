#!/bin/bash
python3 -m venv env
source ./env/bin/activate
pip3 install flask gunicorn
