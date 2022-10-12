from django import forms

from .models import NewsArticle

class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = [
            'title',
            'url',
        ]

        labels = {
            'title': '',
            'url': '',
           
        }
   
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
        }
    

 