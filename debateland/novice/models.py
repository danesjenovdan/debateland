from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel


class NovicaPage(Page):
    class Meta:
        verbose_name = 'Newspage'

    date = models.DateField()
    preview_text = RichTextField(blank=False, null=False, default='')
    body = StreamField([
            ('paragraph', blocks.RichTextBlock()),
        ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('preview_text', classname="full"),
        FieldPanel('body', classname="full")
    ]
