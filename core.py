from logging import debug,warn

config = {}

actions = {}
eventfilters = {}
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

def eventfilter(key):
  def _eventfilter(func):
    if key in eventfilters:
      warn(key + " duplicate eventfilter name, not loading")
    else:
      eventfilters[key] = func
    return func
  return _eventfilter

def service(key):
  def _service(func):
    if key in services:
      warn(key + "duplicate service name, not loading")
    try:
      services[key] = func(config,event_queue)
    except Exception:
      print(Exception)
  return _service

class Workflow:
  def __init__(self, yaml, config):
    self.yaml = yaml
    self.variables = {}
    self.config = config

  def execute(self):
    data = []
    for action in self.yaml:
      print(self.yaml)
      params = self.replace_variables(self.yaml[action])
      result = actions[action](params, self.variables, self.config, data)
      data.append(result)
      #debug(data[-1])

  def replace_variables(self, params):
    print(params)
    for item in params:
      try:
        params[item] = params[item].format_map(self.variables)
      except KeyError:
        debug(params[item])
    return params
