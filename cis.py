# -*- coding: utf-8 -*-

from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)

import os, time, json, glob, sys

import comparator

reload(sys)
sys.setdefaultencoding('euc-kr')
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

from logging import Formatter, FileHandler

handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)

Adaptive = {"on": 0, "off": 1}
Token = {"rich": "R", "small": "S"}


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fileUpload', methods=['POST'])

def fileUpload():
    '''
    print request
    print request.form
    print request.args
    print request.files
    print request.values
    print request.data
    print request.form['lang']
    print request.form['token']
    print request.form['criterion']
    '''
    if 'file' not in request.files:
        return render_template("home.html")
    
    if 'file2' not in request.files:
        return render_template("home.html")

    startTime = time.time()
    target = os.path.join(basedir, 'images/')

    file = request.files['file']
    filename = file.filename
    destination = target + filename
    file.save(destination)

    file2 = request.files['file2']
    filename2 = file2.filename
    destination2 = target + filename2
    file2.save(destination2)
    
    print('files : ' , file, file2)

    if filename.endswith(".zip") != True:
        return render_template("home.html")
    if filename2.endswith(".zip") != True:
        return render_template("home.html")

    res = unzipNresult(filename, filename2, request.form['lang'], request.form['token'], int(request.form['criterion']))
    print ('res : ', res)
    endTime = time.time() - startTime
    endTime = format(endTime, ".3f")
    res['time'] = endTime
    return jsonify(res)

def unzipNresult(dir_name, dir_name2, lang, token, criterion=10):
    #make directory
    timeStr = time.strftime('%H%M%S')
    os.makedirs(os.path.join(basedir, 'data/'+timeStr))

    #src1
    O_dir = dir_name
    O_dir = O_dir[:len(O_dir) - 4] ## remove .zip
    O_dire = "./data/" + timeStr + "/" + O_dir
    os.system('unzip ./images/' + O_dir + '.zip' + ' -d ' + O_dire)
    O_dire = O_dire + "/"

    #src2
    T_dir = dir_name2
    T_dir = T_dir[:len(T_dir) - 4] ## remove .zip
    T_dire = "./data/" + timeStr + "/" + T_dir
    os.system('unzip ./images/' + T_dir + '.zip' + ' -d ' + T_dire)
    T_dire = T_dire + "/"

    print('T_dire:', T_dire, 'O_dire:', O_dire)
    return comparator.getResult(O_dire, T_dire, lang=lang, tokenizerOption=token, criterion=criterion)

@app.route("/show_code", methods=['GET'])
def show_code():
    src1_path = request.args.get('src1')
    file1 = open(src1_path, 'r').read()
    code1 = str(unicode(file1, 'euc-kr'))
    return code1
    DIRE = request.args.get('where_dir')
    file1_name = request.args.get('file1')
    file2_name = request.args.get('file2')

    path_file1 = DIRE + file1_name
    path_file2 = DIRE + file2_name

    file1 = open(path_file1, 'r')
    file2 = open(path_file2, 'r')
    reFile1 = file1.read()
    reFile1 = str(unicode(reFile1, 'euc-kr'))
    reFile2 = file2.read()
    reFile2 = str(unicode(reFile2, 'euc-kr'))
    return render_template('show_code.html', File1_name=file1_name + "\n", File2_name=file2_name + "\n", File1=reFile1,
                           File2=reFile2)


@app.route("/show_one_code", methods=['GET'])
def show_one_code():
    DIRE = request.args.get('where_dir')
    file1_name = request.args.get('file1')
    path_file1 = DIRE + file1_name
    file1 = open(path_file1, 'r')
    reFile1 = file1.read()
    reFile1 = str(unicode(reFile1, 'euc-kr'))

    return render_template('show_one_code.html', File_name=file1_name + "\n", File=reFile1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3005, debug=True)
