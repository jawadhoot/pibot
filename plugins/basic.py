from logging import debug
from core import action

@action("write-variable")
def write_variable(params, variables):
  if "name" not in params:
    return ValueError
  if "value" not in params:
    return ValueError
  name = params["name"]
  value = params["value"]
  variables[name] = value
  return "ok"

@action("http-request")
def http_request(params, variables):
  if "url" not in params:
    return ValueError
  url = params["url"]
  debug(url)
  import requests
  res = requests.get(url)
  variables["res"] = res
  return "ok"