from slixmpp import ClientXMPP
from core import action

class SendMsgBot(ClientXMPP):
  def __init__(self, jid, password, recipient, message):
    ClientXMPP.__init__(self, jid, password)
    self.recipient = recipient
    self.msg = message
    self.add_event_handler("session_start", self.start)
    self.connect()
    self.process(forever=False)

  async def start(self, event):
    self.send_presence()
    await self.get_roster()
    self.send_message(mto=self.recipient, mbody=self.msg, mtype='chat')
    self.disconnect()

@action("xmpp-send")
def xmpp_send(params, variables, config, data):
  if "message" not in params:
    return ValueError
  message = params["message"]
  debug(message)
  from services import xmppservice
  xmppservice.SendMsgBot(config["xmpp"]["sender-jid"], config["xmpp"]["sender-pass"], config["xmpp"]["recipient-jid"], message)
  variables["status"] = "ok"
