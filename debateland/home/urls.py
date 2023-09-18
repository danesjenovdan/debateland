from django.urls import path, re_path

from .views import ExerciseListPartialView, ExerciseListView, ExerciseView

urlpatterns = [
    path("<int:id>-<slug:slug>/", ExerciseView.as_view(), name="exercise"),
    path("filter-list", ExerciseListPartialView.as_view(), name="exercise_list_partial"),
    re_path("", ExerciseListView.as_view(), name="exercise_list"),
]
