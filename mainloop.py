import asyncio
from asyncio import events
from flask import Flask
from  importlib import import_module
import json
from logging import basicConfig, INFO, info, DEBUG, debug
from os import listdir
import strictyaml
from sys import platform
from time import sleep
from threading import Thread
from queue import SimpleQueue

import core

basicConfig(level=INFO, format='%(levelname)-8s %(message)s')
config_path = "data/config.json"
workflows_path = "data/workflows"
triggers_path = "data/triggers"

debug(platform)
with open(config_path) as json_data_file:
  core.config = json.load(json_data_file)

if platform == "win32":
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

core.event_queue = SimpleQueue()

info("loading plugins")
import_module("plugins.basic")
import_module("plugins.cricbuzz")
import_module("plugins.xmppservice")
info("plugins loaded")

def remove_ext(filename):
  return filename[:-4]

info("loading workflows")
for filename in listdir(workflows_path):
  if filename.endswith(".yml"):
    file_path = f"{workflows_path}/{filename}"
    with open(file_path, 'r') as f:
      wf = strictyaml.load(f.read()).data
      name = remove_ext(filename)
      core.add_workflow(name, wf)
info("workflows loaded")

info("loading triggers")
for filename in listdir(triggers_path):
  if filename.endswith(".yml"):
    file_path = f"{triggers_path}/{filename}"
    with open(file_path, 'r') as f:
      tr = strictyaml.load(f.read()).data
      core.add_trigger(tr)
info("triggers loaded")

info("available actions")
info(core.actions.keys())
info("available eventfilters")
info(core.triggerfliters.keys())
info("available services")
info(core.services.keys())
info("available workflows")
info(core.workflows.keys())

#info("available triggers")
#info(core.triggers)

def process_event(e):
  filtered_triggers = filter(lambda c: c["trigger"] == e[0], core.triggers)
  for trigger in filtered_triggers:
    if core.triggerfliters[e[0]](e[1], trigger["params"]):
      core.start_workflow(trigger['workflow'])
      info(trigger['workflow'] + "started")
  info("(" + e[0] + "," +e[1] + ") processed ")

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