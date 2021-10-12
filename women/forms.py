from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    # Пример пользовательского валидатора

    def clean_title(self):
        """
        Пользовательский validator для проверки корректности данных в строке title-Заголовок
        """
        title = self.cleaned_data['title']  # cleaned_data - коллекция класса Model.Form - dict()
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title
