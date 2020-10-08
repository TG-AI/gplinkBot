# import pyshorteners
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import re
from gplink_tokens import tokens

from os import environ

import aiohttp

BOT_TOKEN = environ.get('BOT_TOKEN')

def start(update, context):

    update.message.reply_text(
        f'Hi! Mr {update.message.from_user.first_name}\n\nSend Me Your Link Fr Short Your Link\n\nThis Bot Made By @Lakhac\n\nHidden Thanks To @AKHACKER47')


def help_command(update, context):

    update.message.reply_text('**Tutorial**\n\nHello This Bot Can Short Your Link\n\nSO FIRst YOU HAVE TO GET YOUR API TOKEN OF GPLINK FROM https://gplinks.in/member/tools/api \n\nAFTER THAT YOU HAVE TO PUT YOUR TOKEN TO YOUR FIRST NAME\n\nNOW YOU ARE DONE JUST SEMD LINK TO THIS BOT \nTHANKS FOR USING MY BOT \n\nit will loook like https://gplinks.in/api?api=6a4cb74d70edd86803333333333a&')


def echo(update, context):
    # if ('https://gplinks.in/api?api=' in str(update.message.text)):
    #     url = update.message.text.replace('https://gplinks.in/api?api=', '')
    #     token = re.sub("&.*", "", url)
    #     id = update.message.chat_id
    #     tokens[id] = str(token)
    #     with open('gplink_tokens.py','w') as file:
    # 	    file.write('tokens = ' + str(tokens))
    #     update.message.reply_text('chat_id : ' + str(id) + " token : " + str(token))
    if 'https://gplinks.in/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://gplinks.in/api?api=", "")
        token = re.sub("&.*", "", url)
        tokens[chat] = str(token)
        with open('gplink_tokens.py', 'w') as file:
            file.write('tokens = ' + str(tokens))
            update.message.reply_text(f'Your chat_id : {chat} is registered with gplink api token : {token}\n\n if you send again a different api url it will be reassigned to your chat_id')
    elif 'https://gplinks.in/api?api=' not in str(update.message.text) and (re.search('^http://.*', str(update.message.text)) or re.search('^https://.*', str(update.message.text))):
        try:
            chat = str(update.message.chat_id)
            gptoken = tokens[chat]
            url_convert = update.message.text
        except:
            update.message.reply_text('NOT FOUND TOKEN use /help to get it')

        req = requests.get(f'https://gplinks.in/api?api={gptoken}&url={url_convert}')
        r = json.loads(req.content)

        if r['status'] == 'success':
            update.message.reply_text(' Status : ' + r['status'])
            update.message.reply_text(' shortenedUrl : ' + r['shortenedUrl'])
        if r['status'] == 'error':
            update.message.reply_text(' Error : ' + r['message'])


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    # token = update.message.text.from_user.first_name

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
