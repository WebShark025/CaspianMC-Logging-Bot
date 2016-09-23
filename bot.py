#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

print "[System] Bot has started."

user = [line.rstrip('\n') for line in open('user.txt','rt')]


import telebot
import random
import json
import time
from pprint import pprint

API_TOKEN = 'YOUR TOKEN'

bot = telebot.TeleBot(API_TOKEN)

with open('loggingids.json') as f:
    loggingIDs = json.load(f)

@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(m):
	cid = m.chat.id
	inviter = m.from_user.first_name
	if m.content_type == 'new_chat_participant':
		if m.new_chat_participant.id == bot.get_me().id:
			chatid = m.chat.id
			if str(cid) not in user:
				user.append(str(cid))
				with open('user.txt', 'a') as f:
					f.write(str(cid)+"\n")
			bot.send_message(cid, "WOAAH! That was a very fast transport! 😨\nHi! My Name is Logging Bot clone! \n" + str(inviter) + " has invited me into this group!\n\nIf you want to Setup me type /setup into the Chat.\nI will try to bridge all your messages to another group! 😉\nIf you want to see all the cute guys behind the Bot type /credits 😇")
			print "New group received."
			userwhogotadded = m.new_chat_participant.first_name
			username = m.new_chat_participant.username
			groupname = m.chat.title
			groupid = m.chat.id
			bot.send_message(164017979, "# DEBUG # " + "Bot got invited to the group " + str(groupname) + "(" + str(groupid) + ")", parse_mode="HTML")



@bot.message_handler(commands=['yes'])
def yes(m):
	cid = m.chat.id
	user = m.from_user.first_name
	bot.send_message(164017979, str(user)  + " had Problems in setting up." , parse_mode="Markdown")
	bot.send_message(cid, "Thank you very much for making our Bot better!")
	
@bot.message_handler(commands=['no'])
def no(m):
	cid = m.chat.id
	user = m.from_user.first_name
	bot.send_message(164017979, str(user) + " had no Problems in setting the Bot up." , parse_mode="Markdown")
	bot.send_message(cid, "Thank you very much for making our Bot better!")

@bot.message_handler(commands=['credits'])
def credits(m):
	cid = m.chat.id
	bot.send_message(cid, "_بات لاگ چتهای گروه وبشارک_ \n *صرفا جهت لاگ گرفتن از چت های پاک شده* \n *فورک پراجکت aRandomStranger*", parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def help(m):
	cid = m.chat.id
	bot.send_message(cid, "*Bot Help Page*\n\n/setup - Start setup the Bot in this group\n/setloggingid <Group-ID> - Sets a group ID to log all messages and send it into the group\n/id - Gets the current group-id\n /nobroadcasts - Opts you from Broadcasts out.", parse_mode="Markdown")
	
@bot.message_handler(commands=['setloggingid'])
def setloginggid(m):
    idA, cid = m.chat.id, m.chat.id
    if len(m.text.split()) != 2:
        bot.send_message(cid, "Usage: /setloggingid <ID>")
        return
    try:
        idB = int(m.text.split()[1])
    except:
        bot.send_message(cid, "Usage: /setloggingid <ID>")
        return
    bot.send_message(cid, "Group {} messages will be sent to {}".format(idA,idB))
    loggingIDs[str(idA)] = str(idB)
    with open('loggingids.json','w') as f:
        json.dump(loggingIDs, f)
		
	
@bot.message_handler(commands=['setup'])
def welcome(m):
	cid = m.chat.id
	bot.send_message(cid, "*Welcome to this group!*\n *1)* Create a *new* Group and add the Bot into the Group.\n *2)* Type /id and copy the group-ID.\n *3)* Finish the setup by type /setloggingid <ID of other Group> in the group where the messages shall get noticed. Make sure you set the id WITH the minus ( - ) sign.\n* 4)* You are *finished!* _The Bot will start collecting and sending messages into the Logging Group!_\n", parse_mode="Markdown")

def handle_messages(messages):
    for m in messages:
        prcs_msg(m)

def prcs_msg(m):
    cid = m.chat.id
    if str(cid) in loggingIDs:
        try:
            bot.forward_message(int(loggingIDs[str(cid)]), cid, m.message_id)
        except:
            pass

@bot.message_handler(commands=['id'])
def id(m):
    cid = m.chat.id
    uid = m.from_user.id
    if cid > 0:
        bot.send_message( cid, "This feature is only in group chats available!")
    else:
        bot.send_message( cid, "Hi %s , The group ID is %s.\nUse it to setup a logging group!" %(m.from_user.first_name, cid))
        print "ID command received"

		
bot.set_update_listener(handle_messages)

bot.polling(none_stop=True, interval=0, timeout=3)

