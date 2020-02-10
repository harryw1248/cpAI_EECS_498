#!/bin/bash

rm -f app.zip
pip freeze > requirements.txt


zip -r app.zip requirements.txt .ebextensions *.py  # Append any folders/files here
