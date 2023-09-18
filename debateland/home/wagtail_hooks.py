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



# --- HELPERS


class CopyView(InstanceSpecificView):
    page_title = gettext_lazy("Copy")

    def check_action_permitted(self, user):
        return self.permission_helper.user_can_edit_obj(user, self.instance)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_action_permitted(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_meta_title(self):
        return _("Confirm copying of %(object)s") % {"object": self.verbose_name}

    def confirmation_message(self):
        return _("Are you sure you want to copy this %(object)s?") % {
            "object": self.verbose_name
        }

    def copy_instance(self):
        return self.model_admin.copy(self.instance)

    def post(self, request, *args, **kwargs):
        msg = _("%(model_name)s '%(object)s' copied.") % {
            "model_name": self.verbose_name,
            "object": self.instance,
        }
        with transaction.atomic():
            new_instance = self.copy_instance()
        messages.success(request, msg)
        return redirect(self.url_helper.get_action_url("edit", quote(new_instance.pk)))

    def get_template_names(self):
        ma = self.model_admin
        if hasattr(ma, "copy_template_name") and ma.copy_template_name:
            return ma.copy_template_name
        return ma.get_templates("copy")


class ModelAdminCopyMixin:
    copy_view_class = CopyView

    def copy(self, instance):
        raise NotImplementedError(
            "The copy() method must be implemented for each model admin"
        )

    def copy_view(self, request, instance_pk):
        kwargs = {"model_admin": self, "instance_pk": instance_pk}
        view_class = self.copy_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self, parent=None):
        urls = super().get_admin_urls_for_registration()

        urls = urls + (
            re_path(
                self.url_helper.get_action_url_pattern("copy"),
                self.copy_view,
                name=self.url_helper.get_action_url_name("copy"),
            ),
        )

        return urls


# class ExerciseButtonHelper(ButtonHelper):
#     view_button_classnames = ["button", "button-secondary", "button-small"]

#     def view_button(self, obj):
#         return {
#             "url": reverse("lesson", kwargs={"id": obj.id, "slug": slugify(obj.title)}),
#             "label": _("View live"),
#             "classname": self.finalise_classname(self.view_button_classnames),
#             "title": _("View live"),
#         }

#     def copy_button(self, pk):
#         return {
#             "url": self.url_helper.get_action_url("copy", quote(pk)),
#             "label": _("Copy"),
#             "classname": self.finalise_classname(self.view_button_classnames),
#             "title": _("Copy this %(object)s") % {"object": self.verbose_name},
#         }

#     def get_buttons_for_obj(
#         self,
#         obj,
#         exclude=None,
#         classnames_add=None,
#         classnames_exclude=None,
#     ):
#         btns = super().get_buttons_for_obj(
#             obj,
#             exclude,
#             classnames_add,
#             classnames_exclude,
#         )

#         ph = self.permission_helper
#         usr = self.request.user
#         pk = getattr(obj, self.opts.pk.attname)

#         if "copy" not in (exclude or []) and ph.user_can_edit_obj(usr, obj):
#             btns.append(self.copy_button(pk))

#         if "view" not in (exclude or []):
#             btns.append(self.view_button(obj))

#         return btns


# --- MODEL ADMIN


class ExerciseAdmin(ModelAdminCopyMixin, ModelAdmin):
    model = Exercise
    menu_icon = "clipboard-list"
    list_display = ("title", "language", "topic")
    list_filter = ("language", "topic")
    search_fields = ("title")
    # button_helper_class = ExerciseButtonHelper


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


# --- HOOKS


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom_admin.css")
    )


class UserbarEditExerciseItem:
    def render(self, request):
        if "exercise" not in request.resolver_match.url_name:
            return ""

        try:
            exercise_id = request.resolver_match.kwargs["id"]
        except KeyError:
            return ""

        if not exercise_id:
            return ""

        edit_url = exercise_admin.url_helper.get_action_url("edit", exercise_id)
        return format_html(
            """
            <li class="w-userbar__item " role="presentation">
                <a href="{}" target="_parent" role="menuitem" tabindex="-1">
                    <svg class="icon icon-edit w-action-icon" aria-hidden="true"><use href="#icon-edit"></use></svg>
                    Edit this lesson
                </a>
            </li>
            """,
            edit_url,
        )


@hooks.register("construct_wagtail_userbar")
def add_edit_lesson_item(request, items):
    return items.insert(1, UserbarEditExerciseItem())

