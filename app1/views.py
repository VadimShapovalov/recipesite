from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import Category, Recipe
from .forms import AddRecipeForm
from random import choices

from .utils import DataMixin


class RecipesHome(DataMixin, ListView):
    model = Recipe
    template_name = 'app1/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.order_by('?')[:6]
        context['title'] = 'Главная страница'
        return context


def login(request):
    return render(request, 'app1/login.html')


class ShowRecipe(DataMixin, DetailView):
    model = Recipe
    template_name = 'app1/recipe.html'
    pk_url_kwarg = 'recipe_id'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Рецепт')

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe, pk=self.kwargs[self.pk_url_kwarg])


class RecipeCategory(DataMixin, ListView):  # не заработал... потом заработал
    model = Category
    template_name = 'app1/category.html'
    context_object_name = 'recipes'  # ?

    def get_queryset(self):
        return Recipe.objects.filter(categories=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория'
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['recipes'] = Recipe.objects.filter(categories=self.kwargs['category_id'])
        return self.get_mixin_context(context)


class RecipeAuthor(LoginRequiredMixin, DataMixin, ListView):
    model = User
    template_name = 'app1/author_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author_id=self.kwargs['author_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши рецепты'
        context['recipes'] = Recipe.objects.filter(author_id=self.kwargs['author_id'])
        context['author'] = User.username

        return self.get_mixin_context(context)


class AddRecipe(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddRecipeForm
    template_name = 'app1/add_recipe.html'
    title_page = 'Добавление рецепта'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        r = form.save(commit=False)
        r.author = self.request.user
        return super().form_valid(form)


class UpdateRecipe(DataMixin, UpdateView):
    model = Recipe
    fields = ['name', 'description', 'ingredients', 'cookingSteps', 'cook_time', 'image', 'categories']
    template_name = 'app1/add_recipe.html'
    success_url = reverse_lazy('index')
    title_page = 'Редактирование рецепта'


def all_recipes(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app1/all_recipes.html',
                  {'title': 'Все рецепты', 'page_obj': page_obj})


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'name': recipe.name
    }
    recipe.delete()
    return render(request, 'app1/delete_recipe.html', context)
