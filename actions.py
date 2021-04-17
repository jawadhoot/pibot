from logging import debug
from services import cricbuzz
actions = {}

def action(key):
    def _action(func):
        actions[key] = func
        return func
    return _action

@action("read-variable")
def read_variable(params, variables, data):
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
def write_variable(params, variables, data):
  if "name" not in params:
    return ValueError
  if "value" not in params:
    return ValueError
  name = params["name"]
  value = params["value"]
  variables[name] = value

@action("http-request")
def http_request(params, variables, data):
  if "url" not in params:
    return ValueError
  url = params["url"]
  debug(url)
  import requests
  res = requests.get(url)
  return {
    "status": res.status_code,
    "text": res.text,
    "headers": res.headers
  }
  
@action("xmpp-send")
def xmpp_send(params, variables, data):
  if "url" not in params:
    return ValueError
  url = params["url"]
  debug(url)
  from services import xmppservice

@action("cricket-score")
def cricket_score(params, variables, data):
  res =cricbuzz.extractor()
  print(res)
  filters = params["filters"]
  filtered_matches = cricbuzz.filter_matches(filters, res)
  return filtered_matches
