from logging import debug
from core import action

@action("read-variable")
def read_variable(params, variables, config, data):
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
def write_variable(params, variables, config, data):
  if "name" not in params:
    return ValueError
  if "value" not in params:
    return ValueError
  name = params["name"]
  value = params["value"]
  variables[name] = value
  variables["status"] = "ok"

@action("http-request")
def http_request(params, variables, config, data):
  if "url" not in params:
    return ValueError
  url = params["url"]
  debug(url)
  import requests
  res = requests.get(url)
  variables["status"] = "ok"
  return {
    "status": res.status_code,
    "text": res.text,
    "headers": res.headers
  }
  