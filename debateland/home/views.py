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
        if lang := self.request.GET.get("lang"):
            if lang in VALID_LANG_IDS:
                new_language = lang
                translation.activate(new_language)

        if not new_language:
            lang = translation.get_language()

        collator = Collator.createInstance(Locale(lang))
        name_attr = "name" if lang == "en" else f"name_{lang}"

        exercises = Exercise.objects.filter(language__code=lang)

        topics_form = ChosenTopicsForm(request.GET)
        if topics_form.is_valid():
            chosen_topics = topics_form.cleaned_data['topics']
            if chosen_topics:
                exercises = exercises.filter(topic__in=chosen_topics)


        sorted_exercises = sorted(
            exercises.distinct(), key=lambda o: collator.getSortKey(o.title)
        )

        paginator = Paginator(sorted_exercises, 8)
        page_number = self.request.GET.get("page")
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
