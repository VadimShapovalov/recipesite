from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.RecipesHome.as_view(), name='index'),
    path('recipe/<int:recipe_id>/', views.ShowRecipe.as_view(), name='recipe'),
    path('category/<int:category_id>/', views.RecipeCategory.as_view(), name='category'),
    path('add_recipe/', views.AddRecipe.as_view(), name='add_recipe'),
    path('update_recipe/<int:pk>/', views.UpdateRecipe.as_view(), name='update_recipe'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),
    path('author_recipes/<int:author_id>/', views.RecipeAuthor.as_view(), name='author_recipes'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
