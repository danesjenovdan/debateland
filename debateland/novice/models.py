from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


class NovicaPage(Page):
    date = models.DateField()
    preview_text = RichTextField(blank=False, null=False, default='')
    body = StreamField([
            ('paragraph', blocks.RichTextBlock()),
        ])

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('preview_text', classname="full"),
        StreamFieldPanel('body', classname="full")
    ]
