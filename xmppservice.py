from slixmpp import ClientXMPP

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
