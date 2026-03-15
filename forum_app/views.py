from django.shortcuts import render
from forum_app.models import Category
from forum_app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from forum_app.models import Category, Post

def index(request):
    category_list = Category.objects.order_by()
    context_dict = {'categories': category_list}
    return render(request, 'forum_app/index.html', context=context_dict)


def register(request):
    registered = False
    category_list = Category.objects.order_by()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'categories': category_list
    }

    return render(request, 'forum_app/register.html', context=context_dict)


def user_login(request):
    error_msg = ""
    category_list = Category.objects.order_by()

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        user = authenticate(username=user_name, password=pass_word)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('forum_app:index')
            else:
                error_msg = "Your account is disabled."
        else:
            error_msg = "Invalid login details supplied."

    context_dict = {
        'categories': category_list,
        'error_msg': error_msg
    }

    return render(request, 'forum_app/login.html',  context=context_dict)

def user_logout(request):
    logout(request)
    return redirect(reverse('forum_app:index'))


def show_category(request, category_name_slug):
    category_list = Category.objects.order_by()
    context_dict = {'categories': category_list}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category

        posts = Post.objects.filter(category=category)
        context_dict['posts'] = posts

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['posts'] = None

    return render(request, 'forum_app/category.html', context_dict)

