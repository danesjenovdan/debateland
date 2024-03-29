# Generated by Django 3.1.8 on 2021-07-09 13:14

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20210708_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericpage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StreamBlock([('color_section', wagtail.core.blocks.StructBlock([('color', wagtail.core.blocks.ChoiceBlock(choices=[('white', 'White'), ('purple', 'Purple'), ('orange', 'Oranžna'), ('green', 'Zelena')], label='Color')), ('body', wagtail.core.blocks.StreamBlock([('headline', wagtail.core.blocks.StructBlock([('title_purple', wagtail.core.blocks.CharBlock(label='Title purple font')), ('title_black', wagtail.core.blocks.CharBlock(label='Title black font')), ('description', wagtail.core.blocks.RichTextBlock(label='Description', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=False)), ('position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')], label='Image position'))], icon='title', label='Headline', template='home/blocks/headline.html')), ('rich_text', wagtail.core.blocks.StructBlock([('position', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], label='Text alignment')), ('aligned_text', wagtail.core.blocks.StreamBlock([('text', wagtail.core.blocks.RichTextBlock(label='Text'))], label='Rich text'))], icon='pilcrow', label='Rich text', template='home/blocks/rich_text.html')), ('double_cards', wagtail.core.blocks.StructBlock([('text1', wagtail.core.blocks.CharBlock(label='Besedilo 1')), ('image1', wagtail.images.blocks.ImageChooserBlock(label='Ikona 1')), ('text2', wagtail.core.blocks.CharBlock(label='Besedilo 2')), ('image2', wagtail.images.blocks.ImageChooserBlock(label='Ikona 2'))], icon='title', label='Dve kartici', template='home/blocks/double_cards.html')), ('triple_cards', wagtail.core.blocks.StructBlock([('title_big1', wagtail.core.blocks.CharBlock(label='Title 1')), ('title_small1', wagtail.core.blocks.CharBlock(label='Subtitle 1', required=False)), ('description1', wagtail.core.blocks.CharBlock(label='Description 1')), ('page1', wagtail.core.blocks.PageChooserBlock(label='Povezava do strani', required=False)), ('url1', wagtail.core.blocks.URLBlock(help_text='Če je prazno se uporabi povezava do strani.', label='Zunanja povezava', required=False)), ('title_big2', wagtail.core.blocks.CharBlock(label='Title 2')), ('title_small2', wagtail.core.blocks.CharBlock(label='Subtitle 2', required=False)), ('description2', wagtail.core.blocks.CharBlock(label='Description 2')), ('page2', wagtail.core.blocks.PageChooserBlock(label='Povezava do strani', required=False)), ('url2', wagtail.core.blocks.URLBlock(help_text='Če je prazno se uporabi povezava do strani.', label='Zunanja povezava', required=False)), ('title_big3', wagtail.core.blocks.CharBlock(label='Title 3')), ('title_small3', wagtail.core.blocks.CharBlock(label='Subtitle 3', required=False)), ('description3', wagtail.core.blocks.CharBlock(label='Description 3')), ('page3', wagtail.core.blocks.PageChooserBlock(label='Povezava do strani', required=False)), ('url3', wagtail.core.blocks.URLBlock(help_text='Če je prazno se uporabi povezava do strani.', label='Zunanja povezava', required=False))], icon='title', label='Three cards', template='home/blocks/triple_cards.html'))]))]))]))], default='', verbose_name='Content'),
        ),
    ]
