from flask import Flask, url_for
from markupsafe import escape
import logging
import json
import os
import strictyaml
import workflow

with open("config.json") as json_data_file:
    config = json.load(json_data_file)
print(config)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

path = "workflows"
workflows = []
for file in os.listdir(path):
    if file.endswith(".yml"):
        file_path = f"{path}/{file}"
        with open(file_path, 'r') as f:
            workflows.append(strictyaml.load(f.read()).data)

for wf in workflows:
    w = workflow.Workflow(wf)
    w.execute()

