from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        """
        Данная функция берет коллекцию context в классе !!!!, и изменяет ее.
        """
        context = kwargs  # вызов коллекции из родит. класса ListView
        cats = Category.objects.all()
        # добавление доп. параметров
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
