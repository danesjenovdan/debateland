from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.base import TemplateView
from icu import Collator, Locale

from .models import Exercise
from .forms import ChosenTopicsForm

VALID_LANG_IDS = [lang[0] for lang in settings.LANGUAGES]


class ExerciseView(TemplateView):
    template_name = "home/lesson_view.html"

    def get(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercise, id=kwargs["id"])
        translation.activate(exercise.language.code)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, id, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exercise"] = get_object_or_404(Exercise, id=id)
        return context


def map_attr(objects, key):
    return list(map(lambda o: getattr(o, key), objects))


class ExerciseListView(TemplateView):
    template_name = "home/lesson_list_view.html"

    def get(self, request, *args, **kwargs):
        new_language = None
        if lang := self.request.GET.get("lang"):
            if lang in VALID_LANG_IDS:
                new_language = lang
                translation.activate(new_language)

        response = super().get(request, *args, **kwargs)

        if new_language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)

        return response
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lang = translation.get_language()
        collator = Collator.createInstance(Locale(lang))
        exercises = Exercise.objects.filter(language__code=lang)

        topics_form = ChosenTopicsForm(self.request.GET)
        if topics_form.is_valid():
            chosen_topic = topics_form.cleaned_data['topic']
            if chosen_topic:
                exercises = exercises.filter(topic=chosen_topic)

        page_number = self.request.GET.get("page")
        if not page_number:
            exercises = exercises.order_by('?')
        paginator = Paginator(exercises, 8)
        page_exercises = paginator.get_page(page_number)

        paginator.elided_page_range = paginator.get_elided_page_range(
            number=page_exercises.number,
            on_each_side=2,
            on_ends=1,
        )
    
        context["exercises"] = exercises
        context["topics_form"] = topics_form

        return context
