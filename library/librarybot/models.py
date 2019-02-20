from django.db import models


class Book(models.Model):

    (AVAILABLE, IN_USE) = range(2)
    STATUS_CHOICES = ((AVAILABLE, "AVAILABLE"), (IN_USE, "IN USE"))
    name = models.CharField(max_length=1000)
    author = models.ForeignKey("BookAuthor", on_delete=models.CASCADE)
    language = models.ForeignKey("BookLanguage", on_delete=models.CASCADE)
    isbn = models.CharField(max_length=1000)

    status = models.IntegerField(choices=STATUS_CHOICES, default=AVAILABLE)
    host = models.ForeignKey("BotUser", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.status == self.AVAILABLE:
            status = "AVAILABLE"
        else:
            status = f"IN USE ({self.host})"
        return f"{status} | {self.author}, '{self.name}' {self.isbn}"


class BookAuthor(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class BookLanguage(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class BotUser(models.Model):
    telegram = models.CharField(max_length=1000)
    phone = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

    def __str__(self):
        return f"@{self.name} ({self.phone}, {self.mail})"
