#!/usr/bin/env python
from PyInquirer import prompt, Separator, Validator
from os.path import isfile
import os
from litescale import *

def clear():
    os.system('cls')
    os.system('clear')

question_main = [
    {
        'type': 'list',
        'name': 'main',
        'message': 'Welcome to Litescale',
        'choices': [
            {'name':'Start/continue annotation',
             'value':'start',
             'short':'start'},
            {'name':'Generate gold standard',
             'value':'gold',
             'short':'gold'},
            {'name':'Create a new annotation project',
             'value':'new',
             'short':'new'},
            {'name':'Log out',
             'value':'logout',
             'short':'logout'},
             Separator(),
            {'name':'Exit',
             'value':'exit',
             'short':'exit'}
        ]
    }
]

questions_start = [
    {
        'type': 'list',
        'name': 'project_name',
        'message': 'Name of the project',
        'choices': project_list
    }
]

questions_new = [
    {
        'type': 'input',
        'name': 'project_name',
        'message': 'Name of the project'
    },
    {
        'type': 'input',
        'name': 'description',
        'message': 'Enter a description for the project'
    },
    {
        'type': 'input',
        'name': 'phenomenon',
        'message': 'Enter the phenomenon to annotate (e.g., offensive, positive)'
    },
    {
        'type': 'input',
        'name': 'tuple_size',
        'message': 'Dimension of the tuples',
        'validate': lambda val: val.isdigit(),
        'default': '4',
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'replication',
        'message': 'Replication of the instances',
        'validate': lambda val: val.isdigit(),
        'default': '4',
        'filter': lambda val: int(val)
    },
    {
        'type': 'input',
        'name': 'instance_file',
        'message': 'Read instances from file',
        'validate': lambda val: isfile(val),
        'default': 'example.tsv'
    }
]

def prompt_bws(tup, phenomenon, best=True, exclude=[]):
    clear()
    if best:
        message = 'which is the MOST {0}?'.format(phenomenon)
    else:
        message = 'which is the LEAST {0}?'.format(phenomenon)
    questions_bws = [
        {
            'type': 'list',
            'name': 'value',
            'message': message,
            'choices': [{"name":x["text"], "value":x["id"], "short":x["text"]} for x in tup if not x["id"] in exclude]+[Separator(),"PROGRESS","EXIT"]
        }
    ]

    return prompt(questions_bws)['value']

def prompt_progress(project_name, user_name):
    done, total = progress(project_name, user_name)
    message = "progress: {0}/{1} {2:.1f}%".format(done, total, 100.0*(done/total))
    question_progress = [
        {
            'type': 'confirm',
            'message': message,
            'name': 'continue',
            'default': True
        }
    ]
    prompt(question_progress)

# login
def login():
    clear()
    try:
        with open(".login") as f:
            default = f.read()
    except:
        default = ""

    question_login = [
        {
            'type': 'input',
            'name': 'user_name',
            'message': 'Username:',
            'default': default
        }
    ]
    user_name = ""
    while user_name == "":
        user_name = prompt(question_login)['user_name']
    with open(".login", "w") as fo:
        fo.write(user_name)
    return user_name

user_name = login()

# main loop
while True:
    main_choice = prompt(question_main)['main']
    if main_choice == 'start':
        if len(project_list()) == 0:
            print ("there are no projects")
            continue
        project_name = prompt(questions_start)['project_name']
        project_dict = get_project(project_name)
        while True:
            tup_id, tup = next_tuple(project_name, user_name)
            if tup_id is None:
                print ("there is no tuple to annotate, exiting")
                break
            answer_best = prompt_bws(tup, project_dict["phenomenon"])
            if answer_best=="EXIT":
                break
            if answer_best=="PROGRESS":
                prompt_progress(project_name, user_name)
                continue
            answer_worst = prompt_bws(tup, project_dict["phenomenon"], False, exclude=[answer_best])
            if answer_worst=="EXIT":
                break
            if answer_worst=="PROGRESS":
                done, total = progress(project_name, user_name)
                print ("progress: {0}/{1} {2:.1f}%".format(done, total, 100.0*(done/total)))
                continue
            annotate(project_name, user_name, tup_id, answer_best, answer_worst)
    elif main_choice == 'gold':
        if len(project_list()) == 0:
            print ("there are no projects")
            continue
        project_name = prompt(questions_start)['project_name']
        gold(project_name)
    elif main_choice == 'new':
        answers = prompt(questions_new)
        new_project(
            answers['project_name'],
            answers['description'],
            answers['phenomenon'],
            answers['tuple_size'],
            answers['replication'],
            answers['instance_file']
            )
    elif main_choice == 'logout':
        user_name = login()
    elif main_choice == 'exit':
        break
