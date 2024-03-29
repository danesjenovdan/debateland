# Generated by Django 3.2.21 on 2023-09-14 10:59

from django.db import migrations, models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_homepage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='genericpage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StreamBlock([('color_section', wagtail.blocks.StructBlock([('color', wagtail.blocks.ChoiceBlock(choices=[('white', 'White'), ('purple', 'Purple'), ('orange', 'Orange'), ('green', 'Green')], label='Background color')), ('body', wagtail.blocks.StreamBlock([('headline', wagtail.blocks.StructBlock([('title_purple', wagtail.blocks.CharBlock(label='Title - first part (purple font)')), ('title_black', wagtail.blocks.CharBlock(label='Title - second part (black font)')), ('description', wagtail.blocks.RichTextBlock(label='Description', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(label='Image', required=False)), ('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right')], label='Image position'))], icon='title', label='Headline', template='home/blocks/headline.html')), ('rich_text', wagtail.blocks.StructBlock([('position', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], label='Text alignment')), ('aligned_text', wagtail.blocks.StreamBlock([('text', wagtail.blocks.RichTextBlock(label='Text'))], label='Rich text'))], icon='pilcrow', label='Rich text', template='home/blocks/rich_text.html')), ('double_cards', wagtail.blocks.StructBlock([('title_big1', wagtail.blocks.CharBlock(label='Title 1')), ('title_small1', wagtail.blocks.CharBlock(label='Subtitle 1', required=False)), ('description1', wagtail.blocks.CharBlock(label='Description 1')), ('button1', wagtail.blocks.CharBlock(label='Button text 1', required=False)), ('page1', wagtail.blocks.PageChooserBlock(label='Link to page', required=False)), ('url1', wagtail.blocks.URLBlock(label='External link', required=False)), ('title_big2', wagtail.blocks.CharBlock(label='Title 2')), ('title_small2', wagtail.blocks.CharBlock(label='Subtitle 2', required=False)), ('description2', wagtail.blocks.CharBlock(label='Description 2')), ('button2', wagtail.blocks.CharBlock(label='Button text 2', required=False)), ('page2', wagtail.blocks.PageChooserBlock(label='Link to page', required=False)), ('url2', wagtail.blocks.URLBlock(label='External link', required=False))], icon='title', label='Two cards', template='home/blocks/double_cards.html')), ('triple_cards', wagtail.blocks.StructBlock([('title_big1', wagtail.blocks.CharBlock(label='Title 1')), ('title_small1', wagtail.blocks.CharBlock(label='Subtitle 1', required=False)), ('description1', wagtail.blocks.CharBlock(label='Description 1')), ('button1', wagtail.blocks.CharBlock(label='Button text 1', required=False)), ('page1', wagtail.blocks.PageChooserBlock(label='Link to page', required=False)), ('url1', wagtail.blocks.URLBlock(label='External link', required=False)), ('title_big2', wagtail.blocks.CharBlock(label='Title 2')), ('title_small2', wagtail.blocks.CharBlock(label='Subtitle 2', required=False)), ('description2', wagtail.blocks.CharBlock(label='Description 2')), ('button2', wagtail.blocks.CharBlock(label='Button text 2', required=False)), ('page2', wagtail.blocks.PageChooserBlock(label='Link to page', required=False)), ('url2', wagtail.blocks.URLBlock(label='External link', required=False)), ('title_big3', wagtail.blocks.CharBlock(label='Title 3')), ('title_small3', wagtail.blocks.CharBlock(label='Subtitle 3', required=False)), ('description3', wagtail.blocks.CharBlock(label='Description 3')), ('button3', wagtail.blocks.CharBlock(label='Button text 3', required=False)), ('page3', wagtail.blocks.PageChooserBlock(label='Link to page', required=False)), ('url3', wagtail.blocks.URLBlock(label='External link', required=False))], icon='title', label='Three cards', template='home/blocks/triple_cards.html'))]))]))]))], default='', use_json_field=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='header_links',
            field=wagtail.fields.StreamField([('page_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(help_text='If empty, subpage title will be used', label='Name', required=False)), ('page', wagtail.blocks.PageChooserBlock(label='Subpage'))])), ('external_link', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Name')), ('url', wagtail.blocks.URLBlock(label='URL'))]))], use_json_field=True, verbose_name='Header links'),
        ),
        migrations.AlterField(
            model_name='metasettings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ogsettings',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
