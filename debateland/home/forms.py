from django import forms
from .models import Topic

class ChosenTopicsForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)