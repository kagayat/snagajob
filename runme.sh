#!/bin/bash

./fix_json.sh applications.json
./fix_json.sh correct_answers.json

python process.py fixed_applications.json fixed_correct_answers.json