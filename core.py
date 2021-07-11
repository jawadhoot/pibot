from logging import debug,warn

config = {}

actions = {}
triggerfliters = {}
services = {}
workflows = {}

triggers = []

event_queue = None

def action(key):
  def _action(func):
    if key in actions:
      warn(key + " duplicate action name, not loading")
    else:
      actions[key] = func
    return func
  return _action

def triggerfliter(key):
  def _triggerfliter(func):
    if key in triggerfliters:
      warn(key + " duplicate eventfilter name, not loading")
    else:
      triggerfliters[key] = func
    return func
  return _triggerfliter

def service(key):
  def _service(func):
    if key in services:
      warn(key + "duplicate service name, not loading")
    try:
      services[key] = func(config,event_queue)
    except Exception:
      print(Exception)
  return _service

def validate_workflow(wf):
  return True

def add_workflow(name, wf):
  debug(name)
  debug(wf)
  if validate_workflow(wf):
    workflows[name] = wf

def validate_trigger(tr):
  return True

def add_trigger(tr):
  debug(tr)
  if validate_trigger(tr):
    triggers.append(tr)

def start_workflow(name, params):
  wf = workflows[name]
  Workflow(wf,config, params).execute()

class Workflow:
  def __init__(self, yaml, config, variables):
    self.yaml = yaml
    self.variables = variables
    self.config = config

  def execute(self):
    data = []
    for action in self.yaml:
      print(self.yaml)
      params = self.replace_variables(self.yaml[action])
      status = actions[action](params, self.variables)
      if status == "ko":
        break

  def replace_variables(self, params):
    print(params)
    for item in params:
      try:
        params[item] = params[item].format_map(self.variables)
      except KeyError:
        debug(params[item])
    return params
