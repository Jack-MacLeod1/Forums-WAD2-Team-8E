import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'forums.settings')

import django
from django.template.defaultfilters import slugify
django.setup()
from forum_app.models import Category, Post, Comment, User
from random import randint

def populate():
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
    


    for cat in cat_dict:
        create_category(cat, cat_dict[cat]["description"], cat_dict[cat]["views"], cat_dict[cat]["likes"])
    
    for cat in cat_dict:
        for post in post_dict:
            create_post(post, post_dict[post]["description"], post_dict[post]["views"], post_dict[post]["likes"], cat)

    

    

def create_category(name, desc, views, likes):
    c = Category.objects.get_or_create(name = name, description = desc,
                                        views = views, likes = likes)[0]
    c.slug = slugify(name)
    c.save()
    return c

def create_post(title, content, views, likes, category):
    p = Post.objects.get_or_create(title = title, content = content, 
                                   views = views, likes = likes, 
                                   category = category,
                                   creator = User.objects.get(username = "Jack"))[0]
    p.save()
    return p

if __name__ == "__main__":
    print("Populating forums with dummy data")
    populate()