from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel, ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtailautocomplete.edit_handlers import AutocompletePanel


class TranslatableName(models.Model):
    name = models.CharField(max_length=255, default="", blank=True, verbose_name="English")
    name_es = models.CharField(max_length=255, default="", blank=True, verbose_name="Spanish")
    name_it = models.CharField(max_length=255, default="", blank=True, verbose_name="Italian")
    name_sl = models.CharField(max_length=255, default="", blank=True, verbose_name="Slovenian")
    name_lt = models.CharField(max_length=255, default="", blank=True, verbose_name="Lithuanian")
    name_fi = models.CharField(max_length=255, default="", blank=True, verbose_name="Finnish")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Topic(TranslatableName):
    pass


class Answer(Orderable):
    exercise = ParentalKey("Exercise", on_delete=models.CASCADE, related_name="answers")
    title = models.TextField(blank=True, null=True)
    body = RichTextField()


class Exercise(ClusterableModel):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    title = models.TextField()
    description = RichTextField()

    panels = [
        FieldPanel("topic"),
        FieldPanel("language"),
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("answers", heading="Answers", label="Answer"),
    ]

    def __str__(self):
        return f"{self.title}"

