# Generated by Django 4.1.2 on 2022-10-17 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_alter_newsarticle_time_added"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsarticle",
            name="time_added",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 10, 17, 11, 40, 46, 259237, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
