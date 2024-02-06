from django import forms
from .models import Category, Recipe


class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'cookingSteps', 'cook_time', 'image', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'ingredients': forms.Textarea(attrs={'rows': 5}),
        }

