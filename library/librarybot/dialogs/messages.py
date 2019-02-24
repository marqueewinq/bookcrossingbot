msg_static = {
    "mainmenu": "Hi you are in main menu, select option below",
    "unrecognized_option_crossroad": "Unrecognized option, try /start again",
    "reguser_ask_email": "Hi! What's your email?",
    "reguser_end_success": "ID {agent} registered as user {user_id} with email {email}",
    "regbook_ask_book_name": "regbook_ask_book_name?",
    "regbook_ask_book_author": "regbook_ask_book_author?",
    "regbook_ask_book_language": "regbook_ask_book_language?",
    "regbook_ask_book_hostname": "regbook_ask_book_hostname?",
    "regbook_ask_book_photo": "regbook_ask_book_photo?",
    "regbook_ask_book_isbn": "regbook_ask_book_isbn?",
    "regbook_summary": """Summary:
    
    book.name: {book_name}
    book.author: {book_author}
    book.language: {book_language}
    book.hostname: {book_hostname}
    book.photoid: {book_photo_id}
    book.isbn: {book_isbn}
    """,
}


def msg(key):
    return msg_static.get(key, "")
