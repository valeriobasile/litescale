#!/usr/bin/env python

from bottle import route, get, post, run, template, request, response, redirect, TEMPLATE_PATH, static_file
from litescale import *
from glob import glob
import os
TEMPLATE_PATH.append('web/views')

@route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='web')

@get('/login')
def login():
    return template('login.tpl')

@post('/login')
def do_login():
    response.set_cookie("user_name", request.forms.get('user_name'))
    redirect("/")

@route('/logout')
def logout():
    response.set_cookie("user_name", "", expires=0)
    redirect("/")

@route('/start')
def start():
    return template('projects.tpl', action='project', project_list=project_list())

@get('/new')
def new_get():
    return template('new.tpl')
@post('/new')
def new_post():
    try:
        os.remove("tmp.tsv")
    except:
        pass
    request.files.get('instance_file').save("tmp.tsv")
    new_project(
        request.forms.get('project_name'),
        request.forms.get('phenomenon'),
        eval(request.forms.get('tuple_size')),
        eval(request.forms.get('replication')),
        "tmp.tsv"
        )
    try:
        os.remove("tmp.tsv")
    except:
        pass
    redirect("/")

@route('/project/<project_name>')
def project(project_name):
    user_name = request.get_cookie('user_name')
    tup_id, tup = next_tuple(project_name, user_name)
    project_dict = get_project(project_name)
    if tup is None:
        return template('finished.tpl', error="no_tuple")
    else:
        done, total = progress(project_name, user_name)
        progress_string = "progress: {0}/{1} {2:.1f}%".format(done, total, 100.0*(done/total))
        return template('project.tpl', project_name=project_name, phenomenon=project_dict["phenomenon"], tup_id=tup_id, tup=tup, progress=progress_string)

@post('/save/<project_name>')
def save(project_name):
    user_name = request.get_cookie('user_name')
    annotate(project_name, user_name, request.forms['tup_id'], request.forms['best'], request.forms['worst'])
    redirect("/project/"+project_name)

@route("/goldmenu")
def goldmenu():
    return template('projects.tpl', action='gold', project_list=project_list())

@route('/gold/<project_name>')
def goldpage(project_name):
    if not empty_annotation(project_name):
        return template('finished.tpl', error="no_tuple")
    else:
        gold(project_name)
        return static_file("gold.tsv", root='projects/{0}/'.format(project_name), download="gold-{0}.tsv".format(project_name))

@route('/')
def index():
    user_name = request.get_cookie('user_name')
    if user_name is None:
        redirect("/login")
    else:
        return template('index.tpl', user_name=user_name)

run(host='localhost', port=8088)
