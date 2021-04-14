from logging import debug
import actions
import re

class Workflow:
  def __init__(self, yaml):
    self.yaml = yaml
    self.variables = {}
    
  def execute(self):
    data = []
    for action in self.yaml:
      params = self.replace_variables(self.yaml[action])
      data.append(actions.actions[action](params, self.variables, data))
      print(data[-1])

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