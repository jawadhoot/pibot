from slixmpp import ClientXMPP
from core import action, Service
from queue import Queue

class XMPPService(Service):

  def __init__(self, config):
    super().__init__(config)
    self.jid = self.config["xmpp"]["sender-jid"]
    self.password = self.config["xmpp"]["sender-pass"]
    self.recipient = self.config["xmpp"]["recipient-jid"]
    self.client = ClientXMPP(self.jid, self.password)

  def run(self):
    self.client.add_event_handler("session_start", self.start)
    self.client.connect()
    self.client.process(forever=False)

  async def start(self, event):
    self.client.send_presence()
    await self.client.get_roster()
    
  @action("xmpp-send")
  def xmpp_send(self, params, variables, data):
    if "message" not in params:
      return ValueError 
    message = params["message"]
    self.client.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
    variables["status"] = "ok"
