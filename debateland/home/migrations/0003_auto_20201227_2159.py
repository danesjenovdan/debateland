# Generated by Django 3.1.4 on 2020-12-27 21:59

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='description_text',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro_text',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]