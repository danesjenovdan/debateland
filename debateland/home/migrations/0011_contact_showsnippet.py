# Generated by Django 3.1.5 on 2021-01-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='showSnippet',
            field=models.BooleanField(default=False),
        ),
    ]