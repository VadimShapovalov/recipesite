from django import template
import app1.views as views
from app1.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()
