import logging

logger = logging.getLogger(__package__)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot

from librarybot.models import Chat, BotUser
from librarybot.dialogs.utility import tg_handler
from librarybot.dialogs.messages import msg


@tg_handler(state=Chat.REGUSER_ASK_EMAIL)
def reguser_ask_email(bot, update, agent, chat, botuser):
    reply = msg("reguser_ask_email")
    return reply, Chat.REGUSER_END


@tg_handler(state=Chat.REGUSER_END)
def reguser_end(bot, update, agent, chat, botuser):
    text = update.message.text
    botuser = BotUser.objects.create(telegram=agent, email=text)

    reply = msg("reguser_end_success").format(
        agent=agent, email=text, user_id=botuser.pk
    )
    return reply, Chat.MAINMENU


state_map = {
    "__meta__": {
        "caption": msg("mainmenu_reguser_caption"),
        "entry_state": Chat.REGUSER_ASK_EMAIL,
        "entry_point": reguser_ask_email,
    },
    "states": {
        Chat.REGUSER_ASK_EMAIL: [MessageHandler(Filters.text, reguser_ask_email)],
        Chat.REGUSER_END: [MessageHandler(Filters.text, reguser_end)],
    },
}
