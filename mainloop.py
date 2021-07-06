import asyncio
from flask import Flask
import importlib
import json
import logging
from logging import info, debug
import os
import strictyaml
from sys import platform
from time import sleep
from threading import Thread
from queue import SimpleQueue

import core

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
config_path = "data/config.json"
workflows_path = "data/workflows"

debug(platform)
with open(config_path) as json_data_file:
  core.config = json.load(json_data_file)

if platform == "win32":
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

core.event_queue = SimpleQueue()

info("loading modules")
importlib.import_module("modules.basic")
importlib.import_module("modules.cricbuzz")
importlib.import_module("modules.xmppservice")
info("modules loaded")

info("loading workflows")
for filename in os.listdir(workflows_path):
  if filename.endswith(".yml"):
    file_path = f"{workflows_path}/{filename}"
    with open(file_path, 'r') as f:
      wf = strictyaml.load(f.read()).data
      core.workflows[filename] = core.Workflow( wf , core.config)
info("workflows loaded")

info("available actions")
info(core.actions.keys())
info("available services")
info(core.services.keys())
info("available workflows")
info(core.workflows.keys())

def process_event(e):
  core.workflows["cricket-score.yml"].execute()
  info(e[0] + e[1] + "processed")


while True:
  try:
    while not core.event_queue.empty():
      e = core.event_queue.get()
      debug(e)
      t = Thread(target=process_event,args=(e,))
      t.start()
  except KeyboardInterrupt:
    break
  sleep(1)

# app = Flask("pibot")
# @app.route('/')
# def index():
#   return "pibot"
# app.run(port=8080)