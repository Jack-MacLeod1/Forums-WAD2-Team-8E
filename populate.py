import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'forums.settings')

import django
from django.template.defaultfilters import slugify
django.setup()
from forum_app.models import Category, Post, Comment, User, UserProfile
from django.contrib.auth import get_user_model
from random import randint

def populate():
    create_sample_user_and_profile()
    cat_dict = {"UK News" : {"description": "Current news stories of the UK",
                "views": 50,
                "likes": 51},
                "UofG": {"description": "Everything University of Glasgow",
                "views": 52,
                "likes": 53},
                "Sport": {"description": "Latest stories in Sport",
                "views": 54,
                "likes": 55}}
    
    post_dict = {"post1": {"description": "This is some sample text describing the post content",
                "views": 56,
                "likes": 57},
                "post2": {"description": "This is some more sample text describing the post content",
                "views": 58,
                "likes": 59},
                "post3": {"description": "This is some more sample text describing the post content",
                "views": 60,
                "likes": 61}}
    
    comment_dict = {"c1": {"content": "This is some sample text describing c1 content",
                           "likes": 12},
                    "c2": {"content": "This is some sample text describing c2 comment content",
                           "likes": 13},
                    "c3": {"content": "This is some sample text describing c3 comment content",
                           "likes": 18},
    }

    for cat in cat_dict:
        create_category(cat, cat_dict[cat]["description"], cat_dict[cat]["views"], cat_dict[cat]["likes"])
    
    for cat in cat_dict:
        for post in post_dict:
            create_post(post, post_dict[post]["description"], post_dict[post]["views"], 
                        post_dict[post]["likes"], Category.objects.get(name=cat))
    
    for comment in comment_dict:
        for post in Post.objects.all():
            create_comment(post, content = comment_dict[comment]["content"],
                            likes = comment_dict[comment]["likes"])

def create_sample_user_and_profile():
    User = get_user_model()
    if not User.objects.filter(username = "Sample User").exists():
        user = User.objects.create_user(username = "Sample User",
                                        email = "example@example.com",
                                        password = "Glasgow-Dundee-Edinburgh")
        user.save()
    else:
        user = User.objects.get(username = "Sample User")
        
    user_profile = UserProfile.objects.get_or_create(user = user,
                                        bio = "Sample User bio")[0]
    user_profile.save()
    

def create_category(name, desc, views, likes):
    c = Category.objects.get_or_create(name = name, description = desc,
                                        views = views, likes = likes)[0]
    c.slug = slugify(name)
    c.save()
    return c

def create_post(title, content, views, likes, category):
    p = Post.objects.get_or_create(category = category,
                                   creator = User.objects.get(username = "Sample User"),
                                   title = title, content = content, 
                                   views = views, likes = likes, 
                                   )[0]
    p.save()
    return p

def create_comment(post, content, likes):
    c = Comment.objects.get_or_create(post = post,
                                      creator = User.objects.get(username = "Sample User"),
                                      content = content,
                                      likes = likes
                                      )[0]
    c.save()
    return c
    

if __name__ == "__main__":
    print("Populating forums with dummy data")
    populate()