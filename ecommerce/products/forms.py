from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text','stars']
        widgets = {
            'stars': forms.Select(),
            'text': forms.Textarea(attrs={})
            }
        labels = {
            'text' : '',
            'stars': 'Оценка'
            }