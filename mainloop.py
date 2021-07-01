import logging
import json
import os
import strictyaml
import workflow
from logging import info, debug
import asyncio
from sys import platform

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

debug(platform)
if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

with open("data/config.json") as json_data_file:
    config = json.load(json_data_file)

debug(config)

info("loading services")
from modules import xmppservice
info("services loaded")

info("loading workflows")
path = "data/workflows"
workflows = []
for file in os.listdir(path):
    if file.endswith(".yml"):
        file_path = f"{path}/{file}"
        with open(file_path, 'r') as f:
            workflows.append(strictyaml.load(f.read()).data)
info("workflows loaded")

for wf in workflows:
    w = workflow.Workflow(wf, config)
    w.execute()

