import asyncio
import logging
from logging import info, debug
import json
import os
import strictyaml
import workflow
from sys import platform
from time import sleep
import importlib

import core

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
config_path = "data/config.json"
workflows_path = "data/workflows"

debug(platform)
with open(config_path) as json_data_file:
    core.config = json.load(json_data_file)

if platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
info("loading modules")
importlib.import_module("modules.xmppservice")
info("modules loaded")

info("loading workflows")
for filename in os.listdir(workflows_path):
    if filename.endswith(".yml"):
        file_path = f"{workflows_path}/{filename}"
        with open(file_path, 'r') as f:
            wf = strictyaml.load(f.read()).data
            core.workflows[filename] = workflow.Workflow( wf , core.config) 
info("workflows loaded")
