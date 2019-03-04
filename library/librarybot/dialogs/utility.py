import logging
from random import randint
import json

logger = logging.getLogger(__package__)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler
from functools import wraps

from librarybot.models import Chat, BotUser


def get_update_context(update, state):
    logger.debug(f"getting context for state={state}")
    agent = update.message.from_user.id
    chat = Chat.objects.filter(agent=agent, state=state).first()
    botuser = BotUser.objects.filter(telegram=agent).first()
    if botuser is None:
        botuser = BotUser.objects.create(telegram=agent)
    return agent, chat, botuser


def tg_handler(state):
    def deco(f):
        @wraps(f)
        def f_dec(bot, update):
            agent, chat, botuser = get_update_context(update, state=state)

            logger.debug(f"context= agent:{agent} chat:{chat} botuser:{botuser}")
            retval = f(bot, update, agent, chat, botuser)
            if type(retval) == str:
                update.message.reply_text(retval)
                chat.delete()
                return ConversationHandler.END

            if len(retval) == 2:
                msg, new_state = retval
                update_meta = None
            elif len(retval) == 3:
                msg, new_state, update_meta = retval

            if update_meta is not None:
                chat.update_meta(update_meta)
            chat.state = new_state
            chat.save()

            if new_state is None:
                return ConversationHandler.END

            if type(msg) == str:
                update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            else:
                args, kwargs = msg
                update.message.reply_text(*args, **kwargs)

            return new_state

        return f_dec  # true decorator

    return deco


def quick_search(target, model, field="name"):
    # FIXME: migrate to PostgreSQL and make td-idf search instead
    qry = {field + "__icontains": target}
    results = _ask_db(model, qry)
    if results.first() is not None:
        return results
    possiblebookname = sorted(target.split(",")[-1].split("'"))[-1]
    return _ask_db(model, {field + "__icontains": possiblebookname})


def _ask_db(model, qry):
    return model.objects.filter(**qry)
