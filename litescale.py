from glob import glob
from os.path import join, basename, isfile, isdir
from os import mkdir
import csv
from math import floor, gcd
import json

PROJECT_ROOT = 'projects/'

def project_dir(project_name):
    return join(PROJECT_ROOT, project_name)

def project_file(project_name):
    return join(project_dir(project_name), "tuples.json")

def annotation_dir(project_name):
    return join(PROJECT_ROOT, project_name, "annotations")

def annotation_file(project_name, user_name):
    return join(annotation_dir(project_name), user_name+".json")

def gold_file(project_name):
    return join(project_dir(project_name), "gold.tsv")

def make_tuples(instances, k, p):
    n = len(instances)

    while gcd(n, k) != 1:
    	instances = instances[:-1]
    	n = len(instances)

    tuples = dict()
    tuple_id = 0
    for j in range(p):
    	for x in range(int(floor(n/k))):
    		t = [(x*(k**(j+1)) + (i*(k**j))) % n for i in range(k)]
    		tuples[tuple_id] = [instances[x] for x in t]
    		tuple_id += 1
    return tuples

def project_list(answers=None):
    return [basename(filename) for filename in glob(PROJECT_ROOT+"*")]

def get_project(project_name):
    with open(project_file(project_name)) as f:
        project_dict = json.load(f)
        return project_dict

def get_annotations(project_name, user_name):
    project_dict = get_project(project_name)

    if not isfile(annotation_file(project_name, user_name)):
        with open(annotation_file(project_name, user_name), "w") as fo:
            json.dump({} ,fo)

    with open(annotation_file(project_name, user_name)) as f:
        try:
            annotations = json.load(f)
        except:
            annotations = {}
    return annotations

def next_tuple(project_name, user_name):
    project_dict = get_project(project_name)
    annotations = get_annotations(project_name, user_name)

    for tup_id, tup in project_dict["tuples"].items():
        if tup_id in annotations:
            continue
        return tup_id, tup
    return None, None

def annotate(project_name, user_name, tup_id, answer_best, answer_worst):
    annotations = get_annotations(project_name, user_name)

    annotations[tup_id] = {
        "best": answer_best,
        "worst": answer_worst
    }

    project_dict = get_project(project_name)
    with open(annotation_file(project_name, user_name), "w") as fo:
        json.dump(annotations, fo)
    progress(project_name, user_name)

def progress(project_name, user_name):
    project_dict = get_project(project_name)
    annotations = get_annotations(project_name, user_name)
    return len(annotations), len(project_dict["tuples"])

def new_project(project_name, phenomenon, tuple_size, replication, instance_file):
    project_dict = {
        "project_name": project_name,
        "phenomenon": phenomenon,
        "tuple_size": tuple_size,
        "replication": replication,
        "tuples": []
        }

    instances = []
    with open(instance_file) as f:
    	for line in f:
    		id, text = line.strip().split("\t")
    		instances.append({"id": id, "text": text})
    project_dict['tuples'] = make_tuples(
        instances,
        tuple_size,
        replication
    )

    if not isdir(PROJECT_ROOT):
        mkdir(PROJECT_ROOT)
    if not isdir(project_dir(project_name)):
        mkdir(project_dir(project_name))
    with open(project_file(project_name), "w") as fo:
        json.dump(project_dict, fo)
    if not isdir(annotation_dir(project_name)):
        mkdir(annotation_dir(project_name))

def gold(project_name):
    project_dict = get_project(project_name)
    ids = set()
    texts = dict()
    for tup_id, tup in project_dict["tuples"].items():
        for item in tup:
            ids.add(item["id"])
            texts[item["id"]] = item["text"]
    count_best = {id:0 for id in ids}
    count_worst = {id:0 for id in ids}

    for annotation_file in glob(join(annotation_dir(project_name), "*.json")):
        user_name = basename(annotation_file).replace(".json", "")
        annotations = get_annotations(project_name, user_name)
        for tup_id, annotation in annotations.items():
            count_best[annotation["best"]] += 1
            count_worst[annotation["worst"]] += 1

    scores = {id:count_best[id]-count_worst[id] for id in ids}
    max_score = max(list(scores.values()))
    min_score = min(list(scores.values()))
    scores_normalized = {id:(s-min_score)/(max_score-min_score) for id, s in scores.items()}

    with open(gold_file(project_name), "w") as fo:
        for id in ids:
            fo.write("{0}\t{1}\t{2}\n".format(id, texts[id], scores_normalized[id]))
