import logging

logger = logging.getLogger(__package__)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot

from librarybot.models import Book, Chat, BotUser
from librarybot.dialogs.utility import tg_handler, quick_search
from librarybot.dialogs.messages import msg


@tg_handler(state=Chat.BORROW_ASK_SEARCH)
def borrow_ask_search(bot, update, agent, chat, botuser):
    reply = msg("borrow_ask_search")
    return reply, Chat.BORROW_SEARCH_RESULTS


@tg_handler(state=Chat.BORROW_SEARCH_RESULTS)
def borrow_search_results(bot, update, agent, chat, botuser):
    search_qry = update.message.text
    results = Book.objects.filter(
        name__icontains=search_qry, status__in=[Book.AVAILABLE, Book.IN_USE]
    )
    reply = msg("borrow_search_results")
    return (
        (
            [reply],  # args
            {
                "reply_markup": ReplyKeyboardMarkup(
                    [[str(item)] for item in results]
                    + [[msg("borrow_search_results_notfound")]],
                    one_time_keyboard=True,
                )
            },  # kwargs
        ),
        Chat.BORROW_SEARCH_RESULT_CONFIRM,
    )


@tg_handler(state=Chat.BORROW_SEARCH_RESULT_CONFIRM)
def borrow_search_result_confirm(bot, update, agent, chat, botuser):
    search_results_response = update.message.text
    if search_results_response == msg("borrow_search_results_notfound"):
        return msg("borrow_ask_search"), Chat.BORROW_SEARCH_RESULTS
    selected_book = quick_search(search_results_response, Book).first()
    if selected_book.status == Book.AVAILABLE:
        reply = msg("borrow_confirm_book_available").format(book=selected_book.name)
        return (
            (
                [reply],
                {
                    "reply_markup": ReplyKeyboardMarkup(
                        [
                            [
                                msg("borrow_confirm_book_available_Yes"),
                                msg("borrow_confirm_book_available_No"),
                            ]
                        ],
                        one_time_keyboard=True,
                    )
                },
            ),
            Chat.BORROW_CONFIRM_BORROW,
            {"selected_book_id": selected_book.id},
        )
    if selected_book.current_user == botuser:
        reply = msg("borrow_confirm_book_return").format(book=selected_book.name)
        return (
            (
                [reply],
                {
                    "reply_markup": ReplyKeyboardMarkup(
                        [
                            [
                                msg("borrow_confirm_book_return_Yes"),
                                msg("borrow_confirm_book_return_No"),
                            ]
                        ],
                        one_time_keyboard=True,
                    )
                },
            ),
            Chat.BORROW_CONFIRM_RETURN,
            {"selected_book_id": selected_book.id},
        )
    reply = msg("borrow_confirm_book_inuse").format(
        book=selected_book.name, current_user_tg_id=selected_book.current_user.telegram
    )
    return reply, ConversationHandler.END


@tg_handler(state=Chat.BORROW_CONFIRM_BORROW)
def borrow_confirm_borrow(bot, update, agent, chat, botuser):
    text = update.message.text
    book_id = chat.get_meta()["selected_book_id"]
    book = Book.objects.filter(id=book_id).first()
    if book is None:
        return msg("error_general"), ConversationHandler.END
    if text == msg("borrow_confirm_book_available_Yes"):
        book.status = Book.IN_USE
        book.current_user = botuser
        book.save()
        host_url = msg("mention_user").format(telegram=book.host.telegram)
        reply = msg("borrow_confirm_borrow_success").format(host_url=host_url)
        return reply, ConversationHandler.END
    return msg("borrow_confirm_borrow_userexit"), ConversationHandler.END


@tg_handler(state=Chat.BORROW_CONFIRM_RETURN)
def borrow_confirm_return(bot, update, agent, chat, botuser):
    text = update.message.text
    book_id = chat.get_meta()["selected_book_id"]
    book = Book.objects.filter(id=book_id).first()
    if text == msg("borrow_confirm_book_return_Yes"):
        book.status = Book.AVAILABLE
        book.current_user = None
        book.save()
        return msg("borrow_confirm_book_return_success"), ConversationHandler.END
    return msg("borrow_confirm_book_return_userexit"), ConversationHandler.END


state_map = {
    "__meta__": {
        "caption": msg("mainmenu_borrow_book_caption"),
        "entry_state": Chat.BORROW_ASK_SEARCH,
        "entry_point": borrow_ask_search,
    },
    "states": {
        Chat.BORROW_ASK_SEARCH: [MessageHandler(Filters.text, borrow_ask_search)],
        Chat.BORROW_SEARCH_RESULTS: [
            MessageHandler(Filters.text, borrow_search_results)
        ],
        Chat.BORROW_SEARCH_RESULT_CONFIRM: [
            MessageHandler(Filters.text, borrow_search_result_confirm)
        ],
        Chat.BORROW_CONFIRM_BORROW: [
            MessageHandler(Filters.text, borrow_confirm_borrow)
        ],
        Chat.BORROW_CONFIRM_RETURN: [
            MessageHandler(Filters.text, borrow_confirm_return)
        ],
    },
}
