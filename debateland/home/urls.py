from django.urls import path, re_path

from .views import ExerciseListView, ExerciseView

urlpatterns = [
    path("<int:id>-<slug:slug>/", ExerciseView.as_view(), name="exercise"),
    re_path("", ExerciseListView.as_view(), name="exercise_list"),
]
