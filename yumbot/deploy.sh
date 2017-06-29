#!/usr/bin/env bash

virtualenv env
source env/bin/activate
pip install -e .
zip lambda.zip __init__.py main.py opentableclient.py yelpclient.py
