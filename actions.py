from logging import debug
from services import cricbuzz
actions = {}

def action(key):
    def _action(func):
        actions[key] = func
        return func
    return _action

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
  
@action("xmpp-send")
def xmpp_send(params, variables, config, data):
  if "message" not in params:
    return ValueError
  message = params["message"]
  debug(message)
  from services import xmppservice
  xmppservice.SendMsgBot(config["xmpp"]["sender-jid"], config["xmpp"]["sender-pass"], config["xmpp"]["recipient-jid"], message)
  variables["status"] = "ok"

@action("cricket-score")
def cricket_score(params, variables, config, data):
  res =cricbuzz.extractor()
  print(res)
  filters = params["filters"]
  filtered_matches = cricbuzz.filter_matches(filters, res)
  variables["status"] = "ok"
  return filtered_matches
