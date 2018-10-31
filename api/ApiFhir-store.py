# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:37:55 2018

@author: christian marechal
"""

""" 
slack Arkhn
https://arkhn.slack.com/messages/DDLQU3L2U/

pour deployer
https://gist.github.com/LaRiffle/eb6a8ed7713ed617899f1bab8224c7a3


Creation d'une branche
git checkout -b christian_api_getfile

Exemple d utilisation de l'API Flask 

http://127.0.0.1:5000/yml
http://localhost:5000/getdirect/yml/practitioner/

"""

import os
import pandas as pd
import numpy as np
import sys
import pickle
from math import * 
import glob
pd.set_option('display.max_columns', 30)

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask import jsonify 
from flask import Flask, render_template


from flask import send_file

app = FlaskAPI(__name__, static_url_path='',  static_folder='')

def setbasedir(path):    
    os.chdir(path)
    print(os.getcwd())

if False:#debug sur edi
    setbasedir('D:/ecomdataforgoodfr/Arkhn/flaskarkh')
    
def chargefile(filename):    
    # Open a file: file
    file = open(filename,mode='r')     
    # read all lines at once
    all_of_it = file.read()     
    # close the file
    file.close()
    return all_of_it

def html(content):  # Also allows you to set your own <head></head> etc
   return '<html><head>arkhm</head><body>' + content + '</body></html>'

@app.route('/yml')
def api_yml():
    global tab_yml
    
    kind = 'yml'
    filesYml = glob.glob('data\\'+kind+'/**/*.yml', recursive=True)
    ret = '<hr>'
    tab_yml = pd.DataFrame(columns=['name','path'])
    
    for x in filesYml:
        ret = ret + '<br>' + x  
        y = x.split('\\')
        y = y[len(y)-1]
        k = y.rfind(".")
        #suppression de l'extension 'yml'
        print(y[:k], file=sys.stderr)
        tab_yml = tab_yml.append({'name':y[:k], 'path':x}, ignore_index=True)        
    return html(ret)

#TEST UNITAIRE
#TEST UNITAIRE
##### pytest
#TEST UNITAIRE
#TEST UNITAIRE


def getdirect_file(kind,fname):
    global tab_yml
    
    df = tab_yml.loc[tab_yml['name'] == fname]
    filename = df.iloc[0]['path']
    return send_file(filename, mimetype='text/csv')
    #return filename

#http://localhost:5000/getdirect/yml/practitioner/
@app.route('/getdirect/<kind>/<fname>/', methods=['GET'])
def getdirect(kind,fname):
    #kind = 'yml'
    return getdirect_file(kind,fname)

#http://localhost:5000/get_yml2/Identification/Individuals/practitioner.yml/
@app.route('/get_yml2/<dir0>/<dir1>/<fname>/', methods=['GET'])
def get_yml2(dir0,dir1,fname):
    kind = 'yml'
    filename = 'data/'+kind+'/'+dir0+'/'+dir1+'/'+fname
    #return filename
    return send_file(filename, mimetype='text/csv') #'text/csv')

#http://localhost:5000/get_yml/DataTypes/HumanName.yml/
@app.route('/get_yml/<dir0>/<fname>/', methods=['GET'])
def get_yml(dir0,fname):
    kind = 'yml'
    filename = 'data/'+kind+'/'+dir0+'/'+fname
    #return filename
    return send_file(filename, mimetype='text') #'text/csv')

@app.route('/get_image')
def get_image():
    filename = 'ok.gif'
    return send_file(filename, mimetype='image/gif')

@app.route('/hello', methods = ['GET'])
def api_hello():    
    start_path = '.' # current directory
    #for path,dirs,files in os.walk(start_path):
    #    for filename in files:
    #        print(os.path.join(path,filename), file=sys.stderr)            
    return ("hello")
    
if __name__ == "__main__":
    #app.run(debug=True) 
    app.config['TEMPLATES_AUTO_RELOAD']=True
    print ("__main__", file=sys.stderr) 
    api_yml()
    app.run(debug=True,use_reloader=True)
    