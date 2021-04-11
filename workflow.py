import actions

class Workflow:
  def __init__(self, yaml):
    self.yaml = yaml
    self.variables = {}
    
  def execute(self):
    data = {}
    for action in self.yaml:
      params = self.yaml[action]
      actions.actions[action](params, self.variables)
    

    