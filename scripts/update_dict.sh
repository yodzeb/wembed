#!/bin/bash -x


echo $1 > /tmp/oooo
touch /tmp/aaaaaa
cd $1 
. ../venv/bin/activate 
rm -f ${1}/${2}/all.txt
cat ${1}/${2}/*.txt > ${1}/${2}/all.txt
export PYTHONIOENCODING=utf8
python3 ${1}/../scripts/do_dict.py -d ${1}/${2}  -a ${1}../corpus/bl.txt -f all.txt -W $3 -e $4 2>&1  || true

