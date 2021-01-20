from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class NovicaPage(Page):
    date = models.DateField()
    body = RichTextField(blank=False, null=False, default='')

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full")
    ]
