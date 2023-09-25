from django import forms
from .models import Topic

class ChosenTopicsForm(forms.Form):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.RadioSelect(), required=False)
