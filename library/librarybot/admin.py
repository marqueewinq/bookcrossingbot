from django.contrib import admin
from librarybot.models import Book, BookAuthor, BookLanguage, BotUser, Chat, ImageUpload


class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "language", "status", "host", "current_user")
    list_filter = ("author", "language", "status", "host", "current_user")
    fields = (
        "name",
        "author",
        "language",
        "isbn",
        "host",
        ("status", "current_user"),
        "image_tag",
    )
    search_fields = ("name", "author__name", "language__name")
    raw_id_fields = ("author", "language", "host", "current_user")
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


class ImageUploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookLanguage, BookLanguageAdmin)
admin.site.register(BotUser, BotUserAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ImageUpload, ImageUploadAdmin)
