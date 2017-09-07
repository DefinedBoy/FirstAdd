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
  
