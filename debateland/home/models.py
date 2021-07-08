from django.db import models
from django.utils.translation import gettext_lazy as _
from novice.models import NovicaPage
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


class ExternalLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(label=_("Name"))
    url = blocks.URLBlock(label=_("URL"))

    class Meta:
        label = _("External link")
        icon = "link"


class PageLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=False,
        label=_("Name"),
        help_text=_("If empty, subpage title will be used"),
    )
    page = blocks.PageChooserBlock(label=_("Subpage"))

    class Meta:
        label = _("Link to a subpage")
        icon = "link"


@register_setting(icon="cog")
class MetaSettings(BaseSetting):
    header_links = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name=_("Header links"),
    )

    panels = [
        StreamFieldPanel("header_links"),
    ]


@register_snippet
class Contact(models.Model):
    title = models.TextField()
    text = RichTextField()
    showSnippet = models.BooleanField(default=False)

    panels = [
        FieldPanel('showSnippet', heading="Should this snippet be visible on the page?"),
        FieldPanel('title'),
        FieldPanel('text', classname="full")
    ]

    def __str__(self):
        return self.title + ' ' + ('[VISIBLE]' if self.showSnippet else '[HIDDEN]')

@register_snippet
class Newsletter(models.Model):
    title = models.TextField()
    text = RichTextField()
    showSnippet = models.BooleanField(default=False)

    panels = [
        FieldPanel('showSnippet', heading="Should this snippet be visible on the page?"),
        FieldPanel('title'),
        FieldPanel('text', classname="full"),
    ]

    def __str__(self):
        return self.title + ' ' + ('[VISIBLE]' if self.showSnippet else '[HIDDEN]')


@register_setting
class OgSettings(BaseSetting):
    og_title = models.CharField(max_length=255)
    og_description = models.CharField(max_length=255)
    og_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('og_title'),
        FieldPanel('og_description'),
        ImageChooserPanel('og_image'),
    ]


class HomePage(Page):
    intro_text = RichTextField(blank=True, null=True)
    description_text = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text', classname="full"),
        FieldPanel('description_text', classname="full")
    ]

    parent_page_types = []

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        novice = NovicaPage.objects.all().live().order_by('-first_published_at')
        context['novice'] = novice
        return context


class GenericPage(Page):
    body = StreamField([
        ('heading', blocks.StructBlock([
            ('part_one', blocks.CharBlock(required=False)),
            ('part_two', blocks.CharBlock(required=False)),
            ('intro_text', blocks.RichTextBlock(required=False)),
        ], icon='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('DonationEmbed', blocks.StaticBlock(admin_text='Donation embed'))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
