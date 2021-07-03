from logging import debug

actions = {}
services = {}
config = {}
workflows = {}

def action(key):
  def _action(func):
    actions[key] = func
    return func
  return _action

def service(key):
  def _service(func):
    services[key] = func(config)
  return _service

class Workflow:
  def __init__(self, yaml, config):
    self.yaml = yaml
    self.variables = {}
    self.config = config
     
  def execute(self):
    data = []
    for action in self.yaml:
      params = self.replace_variables(self.yaml[action])
      data.append(actions[action](params, self.variables, self.config, data))
      debug(data[-1])

  def replace_variables(self, params):
    for item in params:
      try:
        params[item] = params[item].format_map(self.variables)
      except KeyError:
        debug(params[item])
    return params
