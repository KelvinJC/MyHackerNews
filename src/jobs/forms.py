from django import forms

from .models import JobArticle

class JobsCreateForm(forms.ModelForm):
    class Meta:
        model = JobArticle
        fields = [
            'author',
            'title',
            'url',
        ]

        labels = {
            'author': '',
            'title': '',
            'url': '',
           
        }
   
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
        }
    

 