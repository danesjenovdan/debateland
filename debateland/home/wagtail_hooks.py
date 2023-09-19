from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.contrib.admin.utils import quote
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape, format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _, gettext_lazy

from wagtail import hooks
from wagtail.admin import messages
# from wagtail.admin.panels import FieldPanel
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler

from wagtail.core.rich_text import LinkHandler
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.contrib.modeladmin.views import InstanceSpecificView

from draftjs_exporter.dom import DOM
# from taggit.models import Tag


from .models import (
    Language,
    Topic,
    Answer,
    Exercise,
)


class NewTabExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs['href']
        return '<a href="%s" target="_blank">' % escape(href)


def header_with_name(props):
    type_ = props.get('block', {}).get('type', '')
    text = props.get('block', {}).get('text', '')
    tag = 'div'
    if type_ == 'header-two':
        tag = 'h2'
    if type_ == 'header-three':
        tag = 'h3'
    if type_ == 'header-four':
        tag = 'h4'
    return DOM.create_element(tag, {}, DOM.create_element('a', {'id': slugify(text)}), props['children'])


# Run hook with order=1 so it runs after admin is loaded (default order=0) and overrides rules
@hooks.register('register_rich_text_features', order=1)
def register_extra_rich_text_features(features):
    features.default_features.append('blockquote')

    features.register_link_type(NewTabExternalLinkHandler)

    features.register_converter_rule('contentstate', 'h2', {
        'from_database_format': {
            'h2': BlockElementHandler('header-two'),
        },
        'to_database_format': {
            'block_map': {'header-two': header_with_name}
        }
    })
    features.register_converter_rule('contentstate', 'h3', {
        'from_database_format': {
            'h3': BlockElementHandler('header-three'),
        },
        'to_database_format': {
            'block_map': {'header-three': header_with_name}
        }
    })
    features.register_converter_rule('contentstate', 'h4', {
        'from_database_format': {
            'h4': BlockElementHandler('header-four'),
        },
        'to_database_format': {
            'block_map': {'header-four': header_with_name}
        }
    })


# --- MODEL ADMIN


class ExerciseAdmin(ModelAdmin):
    model = Exercise
    menu_icon = "clipboard-list"
    list_display = ("title", "language", "topic")
    list_filter = ("language", "topic")
    search_fields = ("title")


exercise_admin = ExerciseAdmin()


class LanguageAdmin(ModelAdmin):
    model = Language
    menu_icon = "list-ul"
    list_display = ("name", "code")


class TopicAdmin(ModelAdmin):
    model = Topic
    menu_icon = "list-ul"
    list_display = ("name",)


# class AnswerAdmin(ModelAdmin):
#     model = Answer
#     menu_icon = "list-ul"
#     list_display = ("name",)



class ExercisesGroup(ModelAdminGroup):
    menu_label = "Exercises"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        ExerciseAdmin,
        LanguageAdmin,
        TopicAdmin,
        # AnswerAdmin,
    )


modeladmin_register(ExercisesGroup)
