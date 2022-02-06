from logging import debug,warn,error,info

config = {}

services = {}
actions = {}
eventfilters = {}

workflows = {}
triggers = {}

event_queue = None

def action(key):
  def _action(func):
    if key in actions:
      warn(key + " duplicate action name, not loading")
    else:
      actions[key] = func
    return func
  return _action

def eventfilter(key):
  def _eventfilter(func):
    if key in eventfilters:
      warn(key + " duplicate trigger name, not loading")
    else:
      eventfilters[key] = func
    return func
  return _eventfilter

def service(key):
  def _service(func):
    if key in services:
      warn(key + " duplicate service name, not loading")
    try:
      services[key] = func(config[key])
    except Exception as e:
      error(e, exc_info=True)
  return _service

def validate_workflow(wf):
  return True

def add_workflow(name, wf):
  debug(name)
  debug(wf)
  if name in workflows:
      warn(name + " duplicate workflow name, not loading")
  if validate_workflow(wf):
    workflows[name] = wf

def validate_trigger(tr):
  return True

def add_trigger(name, tr):
  debug(name)
  debug(tr)
  if validate_trigger(tr):
    triggers[name] = tr

def start_workflow(name):
  wf = workflows[name]
  Workflow(wf,config).execute()

def put_event(ev):
  event_queue.put(ev)

class Workflow:
  def __init__(self, yaml, config):
    self.yaml = yaml
    self.variables = {}
    self.config = config

  def execute(self):
    data = []
    for action in self.yaml:
      debug(self.yaml)
      params = self.replace_variables(self.yaml[action])
      status = actions[action](params, self.variables)
      if status == "ko":
        break

  def replace_variables(self, params):
    for item in params:
      try:
        params[item] = params[item].format_map(self.variables)
      except KeyError:
        warn(self.variables)
        warn(params[item])
    return params
