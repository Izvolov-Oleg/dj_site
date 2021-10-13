from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import DataMixin, menu


class WomenHome(DataMixin, ListView):

    model = Women
    template_name = 'women/index.html'  # изменение шаблона, по умолч. ищет шаблон women/women_list.html
    context_object_name = 'posts'  # меняем название коллекции для шаблона

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # вызов коллекции из родит. класса ListView
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Данная функция показывает какие записи отбирать из БД
        влияет на ---> model = Women
        """
        return Women.objects.filter(is_published=True)  # в данном случае будут отбираться только опубликованные записи

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})

class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # изменяем куда будет перенаправлять странца после добавления данных

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # название переменной в urls.py
    context_object_name = 'post'  # название переменной в которой будут отображаться данные из БД в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # генерируют ошибку 404 если нет данных, например в категории нет никаких постов.

    def get_queryset(self):
        """
        Данная функция показывает какие записи отбирать из БД
        влияет на ---> model = Women
        """
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

