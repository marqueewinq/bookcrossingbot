import json, os

from django.db import models
from django.utils.html import mark_safe
from django.conf import settings


class ImageUpload(models.Model):
    image = models.ImageField(upload_to=settings.MEDIA_ROOT_RELATIVE)


class Book(models.Model):

    (AVAILABLE, IN_USE) = range(2)
    STATUS_CHOICES = ((AVAILABLE, "AVAILABLE"), (IN_USE, "IN USE"))
    name = models.CharField(max_length=1000)
    author = models.ForeignKey(
        "BookAuthor", on_delete=models.CASCADE, null=True, blank=True
    )
    language = models.ForeignKey(
        "BookLanguage", on_delete=models.CASCADE, null=True, blank=True
    )
    isbn = models.CharField(max_length=1000)
    image = models.ForeignKey(
        ImageUpload, on_delete=models.CASCADE, null=True, blank=True
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=AVAILABLE)
    host = models.ForeignKey("BotUser", on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.status == self.AVAILABLE:
            status = "AVAILABLE"
        else:
            status = f"IN USE ({self.host})"
        return f"{status} | {self.author}, '{self.name}' {self.isbn}"

    def url(self):
        return os.path.join(
            settings.HOSTNAME,
            settings.MEDIA_URL,
            os.path.basename(str(self.image.image)),
        )

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        # return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()))
        return "<span> Image: {}</span>".format(self.url())

    image_tag.short_description = "Image"


class BookAuthor(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class BookLanguage(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class BotUser(models.Model):
    name = models.CharField(max_length=1000, null=True)
    telegram = models.CharField(max_length=1000)
    email = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"@{self.telegram} ({self.email})"


class Chat(models.Model):
    """
    Telegram chat state.
    """

    # fmt: off
    (
        IDLE, 
        END,
        MAINMENU,
        REGUSER_ASK_EMAIL,
        REGUSER_END,
        REGBOOK_ASK_INFO,
        REGBOOK_ASK_AUTHOR,
        REGBOOK_ASK_LANGUAGE,
        REGBOOK_ASK_HOSTNAME,
        REGBOOK_ASK_PHOTO,
        REGBOOK_ASK_ISBN,
        REGBOOK_END,
    ) = range(12)

    # for verbosity
    CHAT_STATES = (
        (IDLE, "<<Idle>>"),
        (END, "<<Chat ended>>"),
        (MAINMENU, "/main"),
        (REGUSER_ASK_EMAIL, "/registration/email"),
        (REGUSER_END, "/registration/end"),
        (REGBOOK_ASK_INFO, "/regbook/ASK_NAME"),
        (REGBOOK_ASK_AUTHOR, "/regbook/ASK_AUTHOR"),
        (REGBOOK_ASK_LANGUAGE, "/regbook/ASK_LANGUAGE"),
        (REGBOOK_ASK_HOSTNAME, "/regbook/ASK_HOSTNAME"),
        (REGBOOK_ASK_PHOTO, "/regbook/ASK_PHOTO"),
        (REGBOOK_ASK_ISBN, "/regbook/ASK_ISBN"),
        (REGBOOK_END, "/regbook/end"),

    )
    # fmt: on

    state = models.IntegerField(choices=CHAT_STATES, default=IDLE)
    agent = models.CharField(max_length=255)
    meta = models.CharField(max_length=255, default="{}")

    def __str__(self):
        return "chat with @{} on state {}".format(self.agent, self.state)

    def update_meta(self, new_meta):
        meta = self.get_meta()
        meta.update(new_meta)
        self.save_meta(meta)
        return self.get_meta()

    def get_meta(self):
        meta = self.meta
        if meta is None or meta == "":
            return {}
        loaded = json.loads(meta)
        if type(loaded) != dict:
            return {}
        return loaded

    def save_meta(self, data):
        strdata = json.dumps(data)
        self.meta = strdata
        self.save()
        return strdata
