from django.shortcuts import render
from forum_app.models import Category

def index(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    return render(request, 'forum_app/index.html', context=context_dict)