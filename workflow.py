from logging import debug
from core import actions

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


if __name__ == "__main__":
  wf = Workflow("")
  wf.variables = {"a":12, "b":14}
  params = {"txt":"this is {c} this ia b"}
  wf.replace_variables(params)
  print(params)