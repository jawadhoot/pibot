from asyncio.events import new_event_loop
from logging import info
from slixmpp import ClientXMPP
from time import sleep
from threading import Thread

from core import action, service, eventfilter
from core import services
from core import put_event

class XMPPService(Thread):
  def __init__(self, jid, password, recipient):
    super().__init__()
    self.connected = False
    self.failure = False
    self.recipient = recipient

    self.client = ClientXMPP(jid, password)
    self.client.register_plugin('xep_0030')
    self.client.register_plugin('xep_0060') # PubSub
    self.client.register_plugin('xep_0199')
    self.client.add_event_handler('session_start', self.session_start)
    self.client.add_event_handler("message", self.message)
    self.client.add_event_handler("connection_failed", self.failed)
    self.client.connect()
 
  def send_message(self, message):
    self.client.send_message(mto=self.recipient, mbody=message, mtype='chat')

  async def session_start(self, event):
    self.client.send_presence()
    await self.client.get_roster()
    self.connected = True
  
  def failed(self, event):
    self.failure = True

  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      put_event(("xmpp-call",msg["body"]))
 
  def run(self):
    self.client.process(forever=True)
    # TODO - find a way to keep connection alive

@service("xmpp-service")
def xmpp_start(config):
  info("starting XMPPService")
  t = XMPPService(config["sender-jid"],config["sender-pass"],config["recipient-jid"])
  t.daemon = True
  t.start()
  timeout = 10
  while not t.connected  and not t.failure and timeout:
    sleep(1)
    timeout -= 1
  if not timeout or t.failure:
    raise Exception("Connection failed or Timedout")
  info("XMPPService started")
  return t

@action("xmpp-send")
def xmpp_send(params, variables):
  if "message" not in params:
    return ValueError 
  message = params["message"]
  services["xmpp-service"].send_message(message)
  variables["status"] = "ok"

@eventfilter("xmpp-call")
def xmpp_filter(args_list, params):
  if args_list[0] == params["calltext"]:
    return True
  return False
