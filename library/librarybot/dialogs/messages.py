msg_static = {
    "mainmenu": "Hi you are in main menu, select option below",
    "mainmenu_borrow_book_caption": "Search for a book",
    "mainmenu_reguser_caption": "Register as a user",
    "mainmenu_regbook_caption": "Register a book",
    "mainmenu_takeout_book_caption": "Take my book out",
    "unrecognized_option_crossroad": "Unrecognized option, try /start again",
    "reguser_ask_email": "Hi! What's your email?",
    "reguser_end_success": "ID {agent} registered as user {user_id} with email {email}",
    "regbook_ask_book_name": "regbook_ask_book_name?",
    "regbook_ask_book_author": "regbook_ask_book_author?",
    "regbook_ask_book_language": "regbook_ask_book_language?",
    "regbook_ask_book_hostname": "regbook_ask_book_hostname? (by email, in case it's yours, write: 'me')",
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
    "borrow_ask_search": "Enter search string",
    "borrow_search_results": "Select a book or select not found to try again",
    "borrow_search_results_notfound": "(Not found)",
    "borrow_confirm_book_available": "Book {book} available, want to borrow?",
    "borrow_confirm_book_available_Yes": "Yes",
    "borrow_confirm_book_available_No": "No",
    "borrow_confirm_book_inuse": "Book {book} is in use, [current user](tg://user?id={current_user_tg_id}).",
    "borrow_confirm_borrow_success": "Book borrowed OK, you are current user.",
    "borrow_confirm_borrow_userexit": "OK, no problem, no books borrowed",
    "borrow_confirm_book_return": "Are you sure you want to return the book {book}?",
    "borrow_confirm_book_return_Yes": "Yes",
    "borrow_confirm_book_return_No": "No",
    "borrow_confirm_book_return_success": "Book will be returned to shelf after admin approval.",
    "borrow_confirm_book_return_userexit": "OK, no problem, no books returned.",
    "takeout_ask_search": "Search for your book by name",
    "takeout_search_results": "Select a book or select not found to try again",
    "takeout_search_results_notfound": "(Not found)",
    "takeout_confirm_takeout": "Do you really want to take this book out?",
    "takeout_confirm_takeout_Yes": "Yes",
    "takeout_confirm_takeout_No": "No",
    "takeout_confirm_takeout_success": "OK, book taken out",
    "takeout_confirm_takeout_userexit": "No problem",
    "error_general": "Oops! Something wrong happened, try /start again",
}


def msg(key):
    return msg_static.get(key, key)
