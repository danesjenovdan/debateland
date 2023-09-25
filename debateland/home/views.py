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


class ExerciseListView(View):
    def get(self, request):

        new_language = None

        lang = self.request.GET.get("lang")
        if lang and lang in VALID_LANG_IDS:
            translation.activate(lang)
            new_language = lang
        else:
            lang = translation.get_language()
            if not lang:
                lang = "en"

        collator = Collator.createInstance(Locale(lang))

        exercises = Exercise.objects.filter(language__code=lang)

        topics_form = ChosenTopicsForm(request.GET)
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

        response = render(request, "home/lesson_list_view.html", context={ 
            "exercises": page_exercises, 
            "topics_form": topics_form, 
        })

        if new_language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)
        
        return response
