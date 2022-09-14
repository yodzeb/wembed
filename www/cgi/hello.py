from flask import Flask, request, Response
import json
import os
import sys
import subprocess
import re
import shutil

app = Flask(__name__)

filere = r'^[a-zA-Z0-9\.]{3,16}$'
wordre = r'^[a-zA-Z0-9\.]{1,26}$'

corpus_root="/var/www/txt/wembed/corpus/"

@app.route("/corpus", methods=["GET"])
def list_corpus():
    filelist = os.listdir( corpus_root)
    
    return Response(json.dumps(filelist), status=200, mimetype='application/json')

@app.route("/corpus", methods=["POST"])
def create_corpus():
    corpus_name = request.get_json()["name"]

    assert re.match(filere, corpus_name)
    if os.path.isdir(corpus_root+corpus_name):
        return Response("{'error':'already exists'}", status=400, mimetype='application/json')
    else:
        os.mkdir(corpus_root+corpus_name)
    return  Response("{'error':'Created'}", status=201, mimetype='application/json')

@app.route("/corpus/<corpus_name>", methods=["DELETE"])
def delete_corpus(corpus_name):
    corpus_name# = request.get_json()["name"]
    assert re.match(filere, corpus_name)
    if os.path.isdir(corpus_root+corpus_name):
        shutil.rmtree(corpus_root+corpus_name)
    else:
        return Response("{'error':'does not exist'}", status=404, mimetype='application/json')
    return "Deleted corpus"

@app.route("/corpus/<corpus_name>/dict", methods=["PUT"])
def reinit_dict(corpus_name):
    cmd = corpus_root+"/../scripts/update_dict.sh "+corpus_root+" "+corpus_name
    
    #ret=subprocess.run([corpus_root+"/../scripts/update_dict.sh", corpus_root, corpus_name])# -f all.txt
    ret=subprocess.check_output(cmd.split(" "))# -f all.txt
    return cmd+" - "+str(ret)+"recreated dict"

@app.route("/corpus/<corpus_name>/picture/<word>", methods=["PUT"])
def do_image(corpus_name, word):
    assert re.match(filere, corpus_name)
    assert re.match(wordre, word)
    
    cmd = corpus_root+"/../scripts/create_img.sh "+corpus_root+" " +corpus_name+ " "+word
    ret=subprocess.check_output(cmd.split(" "))# -f all.txt
    return cmd+" - "+str(ret)+"recreated dict"


@app.route("/corpus/<corpus_name>", methods=["GET"])
def corpus_details(corpus_name):
    assert re.match(filere, corpus_name)
    if os.path.isdir(corpus_root+corpus_name):
        filelist = os.listdir( corpus_root+"/"+corpus_name)
        return Response(json.dumps(filelist), status=200, mimetype='application/json')
    else:
        return Response("not found", status=404)

@app.route("/corpus/<corpus_name>", methods=["POST"])
def upload_file(corpus_name):
    file = request.files['file']
    #return  (file.filename)
    assert re.match(filere, file.filename)
    file.save(os.path.join(corpus_root, corpus_name, file.filename))
    return "ok"
