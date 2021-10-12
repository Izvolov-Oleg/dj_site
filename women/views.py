from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

class WomenHome(ListView):

    model = Women
    template_name = 'women/index.html'  # изменение шаблона, по умолч. ищет шаблон women/women_list.html
    context_object_name = 'posts'  # меняем название коллекции для шаблона

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Данная функция берет коллекцию context в родительском классе, и изменяет ее.
        """
        context = super().get_context_data(**kwargs)  # вызов коллекции из родит. класса ListView
        # добавление доп. параметров
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        """
        Данная функция показывает какие записи отбирать из БД
        влияет на ---> model = Women
        """
        return Women.objects.filter(is_published=True)  # в данном случае будут отбираться только опубликованные записи

# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=context)

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # изменяем куда будет перенаправлять странца после добавления данных

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Данная функция берет коллекцию context в родительском классе, и изменяет ее.
        """
        context = super().get_context_data(**kwargs)  # вызов коллекции из родит. класса ListView
        # добавление доп. параметров
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html',
#                   {'form': form,
#                    'menu': menu,
#                    'title': 'Добавление статьи'})

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # название переменной в urls.py
    context_object_name = 'post'  # название переменной в которой будут отображаться данные из БД в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Данная функция берет коллекцию context в родительском классе, и изменяет ее.
        """
        context = super().get_context_data(**kwargs)  # контекс данных сформированный базовым классом DetailView
        context['menu'] = menu
        context['title'] = context['post']
        return context

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)

class WomenCategory(ListView):
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
        """
        Данная функция берет коллекцию context в родительском классе, и изменяет ее.
        """
        context = super().get_context_data(**kwargs)  # контекс данных сформированный базовым классом ListView
        context['menu'] = menu
        context['title'] = 'Категория' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug
#     }
#     return render(request, 'women/index.html', context=context)

