from django.contrib import admin
from librarybot.models import Book, BookAuthor, BookLanguage, BotUser, Chat


class BookAdmin(admin.ModelAdmin):
    fields = ("name", "author", "language", "isbn", "status", "host", "image_tag")
    readonly_fields = ("image_tag",)


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class BookLanguageAdmin(admin.ModelAdmin):
    pass


class BotUserAdmin(admin.ModelAdmin):
    list_display = ("telegram", "email")
    fields = ("telegram", "email")


class ChatAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookLanguage, BookLanguageAdmin)
admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Chat, ChatAdmin)
