# Generated by Django 2.1.7 on 2019-03-02 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("librarybot", "0009_auto_20190225_1809")]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="status",
            field=models.IntegerField(
                choices=[(0, "AVAILABLE"), (1, "IN USE"), (2, "TAKEN_OUT_BY_HOST")],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="imageupload",
            name="image",
            field=models.ImageField(upload_to=""),
        ),
    ]