# Generated by Django 4.1.1 on 2022-10-01 07:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_alter_newsarticle_time_utc"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsarticle",
            name="time_utc",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]