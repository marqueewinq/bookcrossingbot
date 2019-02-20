from django.contrib import admin
from librarybot.models import Book, BookAuthor, BookLanguage, BotUser


class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)


class BookAuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookAuthor, BookAuthorAdmin)


class BookLanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookLanguage, BookLanguageAdmin)


class BotUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(BotUser, BotUserAdmin)
