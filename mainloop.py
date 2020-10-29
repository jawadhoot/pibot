import logging
import cricbuzz
from xmppservice import SendMsgBot
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)
print(config)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
res = cricbuzz.extractor()
SendMsgBot(config["xmpp"]["sender-jid"],config["xmpp"]["sender-pass"],config["xmpp"]["recipient-jid"], res)
