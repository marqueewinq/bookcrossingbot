from django.contrib import admin
from librarybot.models import Book, BookAuthor, BookLanguage, BotUser


class BookAdmin(admin.ModelAdmin):
    pass


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class BookLanguageAdmin(admin.ModelAdmin):
    pass


class BotUserAdmin(admin.ModelAdmin):
    list_display = ("telegram", "phone", "email")
    fields = ("telegram", "phone", "email")


admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookLanguage, BookLanguageAdmin)
admin.site.register(BotUser, BotUserAdmin)
