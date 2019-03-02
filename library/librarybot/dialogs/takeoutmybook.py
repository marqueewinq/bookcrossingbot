import logging

logger = logging.getLogger(__package__)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot

from librarybot.models import Book, Chat, BotUser
from librarybot.dialogs.utility import tg_handler, quick_search
from librarybot.dialogs.messages import msg


@tg_handler(state=Chat.TAKEOUT_ASK_SEARCH)
def takeout_ask_search(bot, update, agent, chat, botuser):
    reply = msg("takeout_ask_search")
    return reply, Chat.TAKEOUT_SEARCH_RESULTS


@tg_handler(state=Chat.TAKEOUT_SEARCH_RESULTS)
def takeout_search_results(bot, update, agent, chat, botuser):
    search_qry = update.message.text
    results = Book.objects.filter(name__icontains=search_qry, host=botuser)
    reply = msg("takeout_search_results")
    return (
        (
            [reply],  # args
            {
                "reply_markup": ReplyKeyboardMarkup(
                    [[str(item)] for item in results]
                    + [[msg("takeout_search_results_notfound")]],
                    one_time_keyboard=True,
                )
            },  # kwargs
        ),
        Chat.TAKEOUT_SEARCH_RESULT_CONFIRM,
    )


@tg_handler(state=Chat.TAKEOUT_SEARCH_RESULT_CONFIRM)
def takeout_search_result_confirm(bot, update, agent, chat, botuser):
    search_results_response = update.message.text
    if search_results_response == msg("takeout_search_results_notfound"):
        return msg("takeout_ask_search"), Chat.TAKEOUT_SEARCH_RESULTS
    selected_book = quick_search(search_results_response, Book).first()

    reply = msg("takeout_confirm_takeout").format(book=selected_book.name)
    return (
        (
            [reply],
            {
                "reply_markup": ReplyKeyboardMarkup(
                    [
                        [
                            msg("takeout_confirm_takeout_Yes"),
                            msg("takeout_confirm_takeout_No"),
                        ]
                    ],
                    one_time_keyboard=True,
                )
            },
        ),
        Chat.TAKEOUT_CONFIRM_TAKEOUT,
        {"selected_book_id": selected_book.id},
    )


@tg_handler(state=Chat.TAKEOUT_CONFIRM_TAKEOUT)
def takeout_confirm_takeout(bot, update, agent, chat, botuser):
    text = update.message.text
    book_id = chat.get_meta()["selected_book_id"]
    book = Book.objects.filter(id=book_id).first()
    if book is None:
        return msg("error_general"), ConversationHandler.END
    if text == msg("takeout_confirm_takeout_Yes"):
        book.status = Book.TAKEN_OUT
        book.current_user = botuser
        book.save()
        return msg("takeout_confirm_takeout_success"), ConversationHandler.END
    return msg("takeout_confirm_takeout_userexit"), ConversationHandler.END


state_map = {
    "__meta__": {
        "caption": msg("mainmenu_takeout_book_caption"),
        "entry_state": Chat.TAKEOUT_ASK_SEARCH,
        "entry_point": takeout_ask_search,
    },
    "states": {
        Chat.TAKEOUT_ASK_SEARCH: [MessageHandler(Filters.text, takeout_ask_search)],
        Chat.TAKEOUT_SEARCH_RESULTS: [
            MessageHandler(Filters.text, takeout_search_results)
        ],
        Chat.TAKEOUT_SEARCH_RESULT_CONFIRM: [
            MessageHandler(Filters.text, takeout_search_result_confirm)
        ],
        Chat.TAKEOUT_CONFIRM_TAKEOUT: [
            MessageHandler(Filters.text, takeout_confirm_takeout)
        ],
    },
}
