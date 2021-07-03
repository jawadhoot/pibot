from asyncio.events import new_event_loop
from slixmpp import ClientXMPP
from core import action, service
from core import services
from time import sleep
from threading import Thread
import asyncio
from sys import platform

class XMPPService(Thread):
  def __init__(self, jid, password, recipient):
    super().__init__()
    self.connected = False
    self.recipient = recipient

    self.client = ClientXMPP(jid, password)
    self.client.register_plugin('xep_0030') # Service Discovery
    self.client.register_plugin('xep_0199') # XMPP Ping

    self.client.add_event_handler('session_start', self.session_start)
    self.client.add_event_handler("message", self.message)
 
  def send_message(self, message):
    print(message)
    print(self.client.get_roster())
    print(self.client.send_message(mto=self.recipient, mbody="msg", mtype='chat'))
    print("message sent")

  async def session_start(self, event):
    self.client.send_presence()
    await self.client.get_roster()
    self.connected = True

  def message(self, msg):
    if msg['type'] in ('chat', 'normal'):
      msg.reply("Thanks for sending\n%(body)s" % msg).send()

  def run(self):
    while True:
      self.client.process()
      sleep(1)
  
@action("xmpp-send")
def xmpp_send(params, variables, config, data):
  if "message" not in params:
    return ValueError 
  message = params["message"]
  services["xmpp-service"].send_message(message)
  variables["status"] = "ok"

@service("xmpp-service")
def xmpp_start(config):
  config = config["xmpp"]
  t = XMPPService(config["sender-jid"],config["sender-pass"],config["recipient-jid"])
  t.client.connect()
  t.daemon = True
  t.start()
  while not t.connected:
    sleep(1)
  print("XMPPService started")
  return t
  