# forms.py

from django import forms
from .models import Choice

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields[str(question.id)] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, label=question.text
            )
