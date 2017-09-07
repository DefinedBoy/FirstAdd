# -*- coding: utf-8 -*-
import sys
reload(sys)
import redis
import telebot
from telebot import types, util
sys.setdefaultencoding("utf-8")
redis = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
bot = telebot.TeleBot(token="***TOKEN***", skip_pending=True)
#---First add :D
@bot.message_handler(content_types=["text", "sticker", "photo", "video", "audio", "voice", "video_note", "document"])
def _all_(m):
  if m.chat.type == "group" or m.chat.type == "supergroup":
    chat_id = m.chat.id
    user_id = m.from_user.id
    sender_status = bot.get_chat_member(user_id, chat_id).status
    if sender_status =! ["creator", "administrator"]:
      if redis.sismember(str(chat_id) + ":allow_list", user_id) == False:
        

@bot.message_handler(content_types=["new_chat_member"])
def _add_(m):
  

bot.polling(True)
