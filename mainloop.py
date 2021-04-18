import logging
import json
import os
import strictyaml
import workflow
from logging import info

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

with open("data/config.json") as json_data_file:
    config = json.load(json_data_file)
info(config)

path = "data/workflows"
workflows = []
for file in os.listdir(path):
    if file.endswith(".yml"):
        file_path = f"{path}/{file}"
        with open(file_path, 'r') as f:
            workflows.append(strictyaml.load(f.read()).data)

for wf in workflows:
    w = workflow.Workflow(wf)
    w.execute()

