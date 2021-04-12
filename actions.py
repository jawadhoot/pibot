actions = {}

def action(key):
    def _action(func):
        actions[key] = func
        return func
    return _action

@action("read-variable")
def read_variable(params, variables):
    if "name" not in params:
      return ValueError
    name = params["name"]
    if "default" not in params:
      default = 0
    else:
      default = params["default"]
    
    if name in variables:
      return variables[name]
    else:
      return default


@action("write-variable")
def write_variable(params, variables):
  variables[params.name] = params.value

@action("http-request")
def http_request(params, variables):
  if "url" not in params:
    return ValueError
  url = params["url"]
  import requests
  a =  requests.get(url)
  print(a)