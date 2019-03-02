import logging
import uuid

logger = logging.getLogger(__package__)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from django.conf import settings
from django_telegrambot.apps import DjangoTelegramBot

from librarybot.models import Book, BookAuthor, BookLanguage, Chat, BotUser, ImageUpload
from librarybot.dialogs.utility import tg_handler, quick_search
from librarybot.dialogs.messages import msg


def _save_photo(bot_photo_file):
    fn = "uploads/{}.jpg".format(uuid.uuid4())
    bot_photo_file.download(fn)
    iu = ImageUpload.objects.create(image=fn)
    return iu.id


@tg_handler(state=Chat.REGBOOK_ASK_INFO)
def regbook_ask_book_name(bot, update, agent, chat, botuser):
    reply = msg("regbook_ask_book_name")  # enter book name
    return reply, Chat.REGBOOK_ASK_AUTHOR


@tg_handler(state=Chat.REGBOOK_ASK_AUTHOR)
def regbook_ask_book_author(bot, update, agent, chat, botuser):
    reply = msg("regbook_ask_book_author")
    return reply, Chat.REGBOOK_ASK_LANGUAGE, {"book_name": update.message.text}


@tg_handler(state=Chat.REGBOOK_ASK_LANGUAGE)
def regbook_ask_book_language(bot, update, agent, chat, botuser):
    reply = msg("regbook_ask_book_language")
    return reply, Chat.REGBOOK_ASK_HOSTNAME, {"book_author": update.message.text}


@tg_handler(state=Chat.REGBOOK_ASK_HOSTNAME)
def regbook_ask_book_hostname(bot, update, agent, chat, botuser):
    reply = msg("regbook_ask_book_hostname")
    return reply, Chat.REGBOOK_ASK_PHOTO, {"book_language": update.message.text}


@tg_handler(state=Chat.REGBOOK_ASK_PHOTO)
def regbook_ask_book_photo(bot, update, agent, chat, botuser):
    reply = msg("regbook_ask_book_photo")
    return reply, Chat.REGBOOK_ASK_ISBN, {"book_hostname": update.message.text}


@tg_handler(state=Chat.REGBOOK_ASK_ISBN)
def regbook_ask_book_isbn(bot, update, agent, chat, botuser):
    photo = bot.get_file(update.message.photo[-1].file_id)
    photo_id = _save_photo(photo)
    reply = msg("regbook_ask_book_isbn")
    return reply, Chat.REGBOOK_END, {"book_photo_id": photo_id}


@tg_handler(state=Chat.REGBOOK_END)
def regbook_end(bot, update, agent, chat, botuser):
    book_meta = chat.get_meta()
    isbn = update.message.text
    book_meta.update({"book_isbn": isbn})
    reply = msg("regbook_summary").format(**book_meta)

    author = quick_search(book_meta["book_author"], BookAuthor).first()
    if author is None:
        author = BookAuthor.objects.create(name=book_meta["book_author"])

    language = quick_search(book_meta["book_language"], BookLanguage).first()
    if language is None:
        language = BookLanguage.objects.create(name=book_meta["book_language"])

    if "me" in book_meta["book_hostname"]:
        host = botuser
    else:
        host = quick_search(book_meta["book_hostname"], BotUser, "email").first()
        if host is None:
            host = botuser

    Book.objects.create(
        name=book_meta["book_name"],
        author=author,
        language=language,
        host=host,
        image=ImageUpload.objects.get(id=book_meta["book_photo_id"]),
        isbn=book_meta["book_isbn"],
    )
    return reply, Chat.MAINMENU


state_map = {
    "__meta__": {
        "caption": msg("mainmenu_regbook_caption"),
        "entry_state": Chat.REGBOOK_ASK_INFO,
        "entry_point": regbook_ask_book_name,
    },
    "states": {
        Chat.REGBOOK_ASK_INFO: [MessageHandler(Filters.text, regbook_ask_book_name)],
        Chat.REGBOOK_ASK_AUTHOR: [
            MessageHandler(Filters.text, regbook_ask_book_author)
        ],
        Chat.REGBOOK_ASK_LANGUAGE: [
            MessageHandler(Filters.text, regbook_ask_book_language)
        ],
        Chat.REGBOOK_ASK_HOSTNAME: [
            MessageHandler(Filters.text, regbook_ask_book_hostname)
        ],
        Chat.REGBOOK_ASK_PHOTO: [MessageHandler(Filters.text, regbook_ask_book_photo)],
        Chat.REGBOOK_ASK_ISBN: [MessageHandler(Filters.photo, regbook_ask_book_isbn)],
        Chat.REGBOOK_END: [MessageHandler(Filters.text, regbook_end)],
    },
}

# remember that Filters filter the response to previous chain element :(
