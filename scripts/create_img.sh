#!/bin/bash -x


echo $1 > /tmp/oooo
touch /tmp/aaaaaa
cd $1 
. ../venv/bin/activate 
export PYTHONIOENCODING=utf8
python3 ${1}/../scripts/do_dict.py -d ${1}/${2}  -b ${1}/bl.txt -f all.txt -w $3 2>&1  || true
