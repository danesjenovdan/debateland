# Generated by Django 3.2.21 on 2023-09-14 10:59

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('novice', '0003_auto_20210708_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novicapage',
            name='body',
            field=wagtail.fields.StreamField([('paragraph', wagtail.blocks.RichTextBlock())], use_json_field=True),
        ),
    ]