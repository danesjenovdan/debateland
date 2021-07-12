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
from wagtail.images.blocks import ImageChooserBlock
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


class ContentBlock(blocks.StreamBlock):
    headline = blocks.StructBlock(
        [
            ('title_purple', blocks.CharBlock(label=_('Title - first part (purple font)'))),
            ('title_black', blocks.CharBlock(label=_('Title - second part (black font)'))),
            ('description', blocks.RichTextBlock(required=False, label=_('Description'))),
            ('image', ImageChooserBlock(required=False, label=_('Image'))),
            ('position', blocks.ChoiceBlock(
                choices=[
                    ('left', 'Left'),
                    ('right', 'Right'),
                ],
                label=_('Image position')
            )),
        ],
        label=_('Headline'),
        template='home/blocks/headline.html',
        icon='title',
    )
    rich_text = blocks.StructBlock(
        [
            ('position', blocks.ChoiceBlock(
                choices=[
                    ('left', 'Left'),
                    ('center', 'Center'),
                    ('right', 'Right'),
                ],
                label=_('Text alignment')
            )),
            ('aligned_text', blocks.StreamBlock(
                [
                    ('text', blocks.RichTextBlock(
                        label=_('Text'),
                    )),
                ],
                label=_('Rich text'),
            )),
        ],
        label=_('Rich text'),
        template='home/blocks/rich_text.html',
        icon='pilcrow',
    )
    double_cards  = blocks.StructBlock(
        [
            ('text1', blocks.CharBlock(label=_('Text in left card'))),
            ('image1', ImageChooserBlock(label=_('Image in left card'))),
            ('text2', blocks.CharBlock(label=_('Text in right card'))),
            ('image2', ImageChooserBlock(label=_('Image in right card'))),
        ],
        label=_('Two cards'),
        template='home/blocks/double_cards.html',
        icon='title',
    )
    triple_cards  = blocks.StructBlock(
        [
            ('title_big1', blocks.CharBlock(label=_('Title 1'))),
            ('title_small1', blocks.CharBlock(required=False, label=_('Subtitle 1'))),
            ('description1', blocks.CharBlock(label=_('Description 1'))),
            ('page1', blocks.PageChooserBlock(
                required=False,
                label=_('Link to page'),
            )),
            ('url1', blocks.URLBlock(
                required=False,
                label=_('External link'),
            )),
            ('title_big2', blocks.CharBlock(label=_('Title 2'))),
            ('title_small2', blocks.CharBlock(required=False, label=_('Subtitle 2'))),
            ('description2', blocks.CharBlock(label=_('Description 2'))),
            ('page2', blocks.PageChooserBlock(
                required=False,
                label=_('Link to page'),
            )),
            ('url2', blocks.URLBlock(
                required=False,
                label=_('External link'),
            )),
            ('title_big3', blocks.CharBlock(label=_('Title 3'))),
            ('title_small3', blocks.CharBlock(required=False, label=_('Subtitle 3'))),
            ('description3', blocks.CharBlock(label=_('Description 3'))),
            ('page3', blocks.PageChooserBlock(
                required=False,
                label=_('Link to page'),
            )),
            ('url3', blocks.URLBlock(
                required=False,
                label=_('External link'),
            )),
        ],
        label=_('Three cards'),
        template='home/blocks/triple_cards.html',
        icon='title',
    )

    class Meta:
        label = _('Content')
        icon = 'snippet'


class ColorSectionBlock(blocks.StructBlock):
    color = blocks.ChoiceBlock(
        choices=[
            ('white', 'White'),
            ('purple', 'Purple'),
            ('orange', 'Orange'),
            ('green', 'Green'),
        ],
        label=_('Background color'),
    )
    body = ContentBlock()

    class Meta:
        label = _('Content section with color')
        template = 'home/blocks/color_section.html'
        icon = 'snippet'


class SectionBlock(blocks.StreamBlock):
    color_section = ColorSectionBlock()

    class Meta:
        label = _('Content section')
        template = 'home/blocks/section.html'
        icon = 'snippet'


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
    body = StreamField(
        [('section', SectionBlock())],
        verbose_name=_('Content'),
        default='',
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
