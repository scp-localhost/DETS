# for the app routes
from webapp import app 
from flask import Flask, redirect, url_for, render_template, request, abort, send_from_directory, jsonify
from  datetime import datetime 
from flask_table import Table, Col, LinkCol  #https://pypi.org/project/Flask-Table/0.2.9/
from urllib.request import urlopen
import os
import sqlite3
import random
import base64
import json
cwd = os.getcwd()

class pig:
  def __init__(a_pig, name \
               , db = ''):
               #, db = '/sd/etc/pineapple/pineapple.db'
    paths = [cwd+ '/data/Foo.db',cwd+ '/data/Pig_Perimeter.db']
    pth = iter(paths)
    while not(os.path.exists(db)):db = next(pth)
    a_pig.cwd = cwd
    a_pig.name = name
    a_pig.ds = []
    a_pig.db = db
    a_pig.mens_rea = False
    a_pig.sql = ''

def bu(this_pig):
        s = 'sqlite3 \''+this_pig.db+'\' ".backup \''+this_pig.db+str(datetime.now())+'\'"'
        try:
                os.system(s)
                return s
        except:return False

def dbLand(this_pig):#import sqlite3#https://www.sqlite.org/inmemorydb.html
    conn = sqlite3.connect(this_pig.db)#conn = sqlite3.connect(":memory:")
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(this_pig.sql)
    this_pig.ds = c.fetchall()
    conn.commit()
    conn.close()
    
def safeStr(message,xcode='encode'):
  import base64
  if xcode == 'encode':
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    msg = base64_bytes.decode('ascii')
  else:
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    msg = message_bytes.decode('ascii')
  return msg

def tableMkr(items):
        class ItemTable(Table):
                for v in items[0]:#exec("%s=Col('%s')" % (v,v))
                        if v=='name':
                                name = LinkCol('name', 'specific_qry',url_kwargs=dict(qry='a'),attr='name')
                        elif v in ['data_cli', 'sql']:
                                for idx,item in enumerate(items):
                                       items[idx][v] =  safeStr(item[v],1)
                                exec("%s=Col('%s')" % (v,v))
                        elif v=='a': a=''
                        else: exec("%s=Col('%s')" % (v,v))
                      
        class Item(object):
            def __init__(self, name, description):
                    for v in items[0]:exec("self.%s=%s)" % (v,v))
        return ItemTable(items)#return table.__html__()
      
def updQrys():
        try:
                mainPig = pig('napolion')
                mainPig.db = cwd+ '/data/Pig_Perimeter.db'
                mainPig.sql = 'SELECT a , name , sql FROM honeyCalls;'
                dbLand(mainPig)
                return mainPig.ds
        except Exception as bork:
                print(bork)
                return False

qrys=[{'a':'fuzz','name':'Fuzz Bait','sql':'SELECT "No fuzzing allowed" foo'}]
upd = updQrys()
if upd:qrys = upd
title = 'Perimeter Pig'
#===============routeland=============>
@app.route('/_sql')
def sql_ajax():
        for aaarg in request.args:print(aaarg,request.args.get(aaarg))
        qry = request.args.get('qry', 'calls')
        rec = request.args.get('rec', 0, type=int)
        ds = specific_qry(qry,'ds')
        divs = []
        htm = ''
        print(len(ds))
        if rec<len(ds):
                for key in ds[0]:
                        if ds[rec]:
                                if key == 'scr':
                                        divs.append((key,safeStr(ds[rec][key],1)))
                                else:divs.append((key,ds[rec][key]))
                for div in divs:htm=htm+'<textarea name="'+div[0]+'">'+div[1]+'</textarea>'
        return htm

@app.route('/sql/')
@app.route('/sql')
def sql():return render_template('sql.html',title = title,head='Showing query:',div='',frm='calls',rec='0')

@app.route('/menu')
def menu():return render_template('table.html',table=tableMkr(specific_qry('menu','ds')), title = title,tblhead='Le Menu~')

@app.route('/submit/sql', methods=['POST'])
def submit_sql(frm='frm',rec=0):
        for aaarg in request.values:print(aaarg,request.values.get(aaarg))
        s='INSERT INTO honeyCalls values('
        div = []
        cnt=0
        last = len(request.form)
        for item in request.form:
                cnt=cnt+1
                d = ',' if cnt<last else ''
                div.append((item,request.form[item]))
                if item == 'qry': frm=request.form[item]
                elif item == 'rec': rec=request.form[item]
                elif item == 'scr': s=s+'\''+ safeStr(request.form[item])+'\''+ d
                else: s=s+'\''+ request.form[item]+'\''+ d
        if 'scr' in request.form:s=s+',"\''+ request.form['scr']+'\'"'
        s=s+');'
        ds = specific_qry(frm,'ds')
        print(s)
        return render_template("bigdiv.html",title = title,head='form data...',div=div, frm=frm,rec=rec)

@app.route('/frm/')
@app.route('/frm')
def frm(head='heading',div='div'):
        return render_template("bigdiv.html",title = title,head=head,div=div, frm='frm')

@app.route('/frm/<frm>')
def specific_frm(frm):
        head=frm
        div=''
        return render_template("bigdiv.html",title = title,head=head,div=div, frm=frm)

@app.route('/latest#')
@app.route('/latest')
@app.route('/latest/')
def latest():
        try:
            qry = 'latest'
            return render_template("tables.html",refresh=True,bfq=tableMkr(specific_qry('bfq','ds')),table=tableMkr(specific_qry(qry,'ds')), title = title,tblhead='Latest',qry=qry)
        except Exception as bork:
            return render_template("bigdiv.html",title = title,head='SQL Action Borken',div=bork)

@app.route('/qry')
@app.route('/qry/')
def qry():
        try:
            #table = tableMkr(specific_qry('bfq','ds'))
            return render_template("tables.html",refresh=True,bfq=tableMkr(specific_qry('bfq','ds')),table=tableMkr(updQrys()), title=title,tblhead='Qry Main List')
        except Exception as bork:
                return render_template("bigdiv.html",title=title,head='SQL Action Borken',div=bork)

@app.route('/qry/<qry>')
@app.route('/qry/<qry>/')
@app.route('/qry/<qry>/<form>')
def specific_qry(qry,form=''):#qry dataset output as table, JSON or data
        if (form in ['json','tbl','','#', 'ds']):
                try:
                        qrys = updQrys()
                        this_pig = pig('babe')#get db from Bastards.db table
                        if qry in ['tbl','json']:
                                form = qry
                                items = qrys
                        else:
                                dic = next((sub for sub in qrys if sub['a'] == qry),qry[0])
                                this_pig.sql = safeStr(dic['sql'],1)
                                print(this_pig.sql)
                                if "db" in dic: db = dic['db']#print(db)
                                dbLand(this_pig)
                                items = this_pig.ds
                        if form == 'ds':
                                return items
                        elif form == 'json':
                                return jsonify(items)
                        else:
                                table = tableMkr(items)
                                if form == 'tbl':
                                        return str(table.__html__())
                                else:return render_template("tables.html",table=table,title=title,tblhead=dic['name'],qry=qry)
                except Exception as bork:
                        return render_template("bigdiv.html",title=title,head='SQL Action Borken',div=bork)
        else:return redirect("/qry/fuzz/json"), 302

@app.route('/submit', methods=['POST'])#generic target - lists what you've posted
def submit():#for aaarg in request.args:print(aaarg,request.args.get(aaarg))
        div = []
        for item in request.form:div.append((item,request.form[item]))
        return render_template("bigdiv.html",title = title,head='form data...',div=div, frm='frm')

#==========================>Utils - careful...these'll f-up your db
#
@app.route('/cmd/<ILikeShells>')
@app.route('/cmd/')
@app.route('/cmd')
def cmd(ILikeShells=''):
        div = [{'cmd','ls'}]
        return render_template('cmd.html',title = title,head='C2:',div=div,frm='calls',rec='0')

@app.route('/_cmd/<ILikeShells>')
@app.route('/_cmd/')
@app.route('/_cmd')
def _cmd(ILikeShells=''):
        try:
                div = _cmdX(ILikeShells)
                return render_template("bigdiv.html",title=title,head='Command Completed',div=div)
        except Exception as bork:
                return render_template("bigdiv.html",title=title,head='Command Borken',div=bork+':'+div)
def _cmdX(ILikeShells):
        s = (safeStr(ILikeShells,1),'echo \'fuck off\'')[ILikeShells=='']#bHMgLWFsIC4v
        print(s)
        try:
                #msg = os.system(s)
                msg = os.popen(s).read()
                return msg
        except:
                return False

@app.route('/bu/')
@app.route('/bu')
def backup():
        try:
                div = bu(pig('babe'))
                return render_template("bigdiv.html",title=title,head='Backup Completed',div=div)
        except Exception as bork:
                return render_template("bigdiv.html",title=title,head='Backup Borken',div=bork+':'+div)
@app.route('/init')
def init():
        try:
                initQs = ['DROP TABLE if exists tblFoo;'
                          ,'CREATE TABLE  if not exists tblFoo (a TEXT, name TEXT, sql TEXT);'
                          ,'INSERT INTO tblFoo VALUES (\'a\',\'name\',\'sql\')'
                          ]
                this_pig = pig('babe')
                for sql in initQs:
                        this_pig.sql = sql#print(this_pig.sql)
                        dbLand(this_pig)
                return render_template("bigdiv.html",title=title,head='Action Completed',div=this_pig.ds)
        except Exception as bork:
                return render_template("bigdiv.html",title=title,head='Action Borken',div=bork)

#==========================>Generic Server stuff
@app.route('/')
def index():return render_template("index.html",title = title)

@app.route('/home')
@app.route('/redirect')
def test():
    return redirect("http://127.0.0.1:8080"), 302
@app.route('/static/images/favicon.gif')
def favicongif():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.gif', mimetype='image/vnd.microsoft.icon')
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.errorhandler(404)
def page_not_found(error):
    abort(418)#418 I'm a teapot
#==========================>PoC's & examples
@app.route('/_add_remote/<url>')
@app.route('/_add_remote/')
@app.route('/_add_remote')

def add_remote(url ='', server='172.16.42.1:8088'):#http://192.168.0.213:8080/scholars/
        for aaarg in request.args:print(aaarg,request.args.get(aaarg))
        #print(request.host,'<===========host')
        #print(request.path,'<===========path')
        #print(str(request.query_string),'<===========query_string')
        qs = request.query_string
        q = qs.decode("utf-8")

        #print(request.user_agent,'<===========user_agent')
        a = request.args.get('a', 0, type=int)
        b = request.args.get('b', 0, type=int)
        if qs == '':qs = '_add_numbers?a='+str(a)+'&b='+str(b)
        _url = 'http://'+server+'/'+q#'/_add_numbers?a='+str(a)+'&b='+str(b)
        print(_url)
        _resp = urlopen(_url)
        resp = _resp.read().decode("utf-8")
        
        return resp
@app.route('/aj/')
@app.route('/aj')
def aj():
    return render_template('ajax_remote.html',title = title)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)
@app.route('/ajax/')
@app.route('/ajax')
def ajax():
    return render_template('ajax.html',title = title)
