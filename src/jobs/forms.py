from django import forms

from .models import JobArticle

class JobsCreateForm(forms.ModelForm):
    class Meta:
        model = JobArticle
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
    

 