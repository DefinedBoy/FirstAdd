# -*- coding: utf-8 -*-
import sys
reload(sys)
import redis
import telebot
from telebot import types, util
sys.setdefaultencoding("utf-8")
redis = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
token = "**Here***"
bot = telebot.TeleBot(token=token, skip_pending=True)
#---First add :D
key = bot.get_me().username + "|"

def panel(chat_id):
	cid = chat_id
	status = redis.get(key + str(cid) + ":status") or "off"
	show = str(redis.get(key+ str(cid) + ":max_add") or 3)
	markup = types.InlineKeyboardMarkup()
	a = types.InlineKeyboardButton(text="➖", callback_data="---")
	b = types.InlineKeyboardButton(text=show, callback_data="show")
	c = types.InlineKeyboardButton(text="➕", callback_data="+++")
	d = types.InlineKeyboardButton(text="➖➖➖➖➖", callback_data="demo")
	if status == "on":
		e_ = "✅"
	else:
		e_ = "❌"
	e = types.InlineKeyboardButton(text=e_, callback_data="status")
	f = types.InlineKeyboardButton(text="قفل اجباری:", callback_data="demo:1")
	markup.add(a, b, c)
	markup.add(d)
	markup.add(e, f)
	return markup

@bot.message_handler(content_types=["new_chat_members"])
def _add_(m):
	cid = m.chat.id
	bot_id = bot.get_me().id
	if m.new_chat_member.id == bot_id:
		text = "با دکمه های زیر حد اکثر تعداد دعوت ممبر ها را تایین کنید🎈😁"
		bot.send_message(cid, text, reply_markup=panel(cid))

@bot.message_handler(content_types=["text", "sticker", "photo", "video", "audio", "voice", "video_note", "document"])
def _all_(m):
	if m.chat.type == "group" or m.chat.type == "supergroup":
		uid = m.from_user.id
		cid = m.chat.id
		uname = m.from_user.first_name or "ادمین"
		status = redis.get(key + str(cid) + ":status") or "off"
		if bot.get_chat_member(cid, uid).status == "member":
			if status == "on":
				if redis.sismember(key + str(cid) + ":allow_list", uid) == False:
					bot.delete_message(cid, m.message_id)
					max_add = redis.get(key + str(cid) + ":max_add") or 3
					if redis.sismember(key + str(cid) + ":warn_list", uid) == False:
						text = """کاربر [{}](tg://user?id={}):

برای چت کردن در این گروه باید 3 نفر را به گروه دعوت کنید!""".format(uname, uid, max_add)
						bot.send_message(cid, text, parse_mode="Markdown")
						redis.sadd(key + str(cid) + ":warn_list", uid)
		else:
			if m.text == "/panel":
				bot.delete_message(cid, m.message_id)
				text = "[{}](tg://user?id={}):\nبا دکمه های زیر حد اکثر تعداد دعوت ممبر ها را تایین کنید🎈😁".format(uname, uid)
				bot.send_message(cid, text, parse_mode="Markdown", reply_markup=panel(cid))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	cid = call.message.chat.id
	uid = call.from_user.id
	uname = call.from_user.first_name or "ادمین"
	panel_text = "[{}](tg://user?id={}):\nبا دکمه های زیر حد اکثر تعداد دعوت ممبر ها را تایین کنید🎈😁".format(uname, uid)
	if call.message:
		if bot.get_chat_member(cid, uid).status in ["creator", "administrator"]:
			if call.data == "status":
				db = redis.get(key + str(cid) + ":status") or "off"
				if db == "off":
					redis.set(key + str(cid) + ":status", "on")
				else:
					redis.set(key + str(cid) + ":status", "off")
				bot.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=panel_text, reply_markup=panel(cid), parse_mode="Markdown")
			elif call.data == "+++":
				db = redis.get(key + str(cid) + ":max_add") or 3
				redis.set(key + str(cid) + ":max_add", int(db) + 1)
				bot.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=panel_text, reply_markup=panel(cid), parse_mode="Markdown")
			elif call.data == "---":
				db = redis.get(key + str(cid) + ":max_add") or 3
				if int(db) - 1 == 0:
					text = "0؟😱😂 مگه میشه؟ مگه داریم؟\nخب قفل رو خاموش کن دیگه :)"
					bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=text)
				else:
					redis.set(key + str(cid) + ":max_add", int(db) - 1)
					bot.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=panel_text, reply_markup=panel(cid), parse_mode="Markdown")
			
bot.polling(True)
