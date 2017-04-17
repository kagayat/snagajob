#!/bin/bash

cat $1 | sed -E 's/([[:blank:]])([a-zA-Z0-9]+)(\:)/\1"\2"\3/g' > fixed_$1