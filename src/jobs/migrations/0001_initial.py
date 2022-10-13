# Generated by Django 4.1.1 on 2022-09-28 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JobArticle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.IntegerField(unique=True)),
                ("by", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=100)),
                ("time", models.IntegerField()),
                ("title", models.CharField(max_length=200)),
                ("url", models.TextField()),
                ("date", models.DateField(default=datetime.date.today)),
            ],
        ),
    ]