import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'forums.settings')

import django
from django.template.defaultfilters import slugify
django.setup()
from forum_app.models import Category, Post, Comment, User, UserProfile
from django.contrib.auth import get_user_model
import requests
from django.core.files.base import ContentFile
from datetime import timedelta
from django.utils import timezone
from requests.exceptions import ProxyError

def populate():
    create_sample_user_and_profile()
    cat_dict = {"UK News" : {"description": "Current news stories of the UK",
                "views": 50,
                "likes": 2},
                "UofG": {"description": "Everything University of Glasgow",
                "views": 52,
                "likes": 10},
                "Sport": {"description": "Latest stories in Sport",
                "views": 54,
                "likes": 12},
                "Tech": {"description": "Keeping up with tech",
                "views": 54,
                "likes": 12},
                "Cars": {"description": "For the petrol (or diesel!) heads",
                "views": 54,
                "likes": 12},
                "Animals": {"description": "Awesome animals",
                "views": 54,
                "likes": 12}}
    
    post_dict = {"post1": {"description": "This is some sample text describing the post content",
                "views": 56,
                "likes": 21,
                "img_url": ""},
                "Look at this tall guy!": {"description": "I swear I just met the tallest cat I've ever seen and I'm still not over it. This cat stands like it's got somewhere important \
                         to be—long legs, upright posture, just towering over everything like a tiny, furry giraffe. When it stretches, it basically doubles in height and \
                         suddenly looks like it could reach the top shelf without even trying.What really gets me is how casual it is about the whole thing. Like, being \
                          unusually tall is just part of its daily routine. Meanwhile, I'm over here amazed that a cat can look down at a table instead of up at it 10/10 \
                          would admire again. Tall cats are elite",
                "views": 58,
                "likes": 35,
                "img_url": "https://preview.redd.it/a-tall-cat-in-a-car-v0-eapv0bmk17wb1.jpg?width=640&crop=smart&auto=webp&s=dd16531c8556849ee1bc2a959cde17416455b722"},
                "Awesome bengal cat": {"description": "I have encountered the legendary long cat. And yes—it is as incredible as it sounds.This cat just… keeps going. You think you've \
                        reached the end of it, but nope—more cat. When it stretches out, it looks like a fluffy noodle that somehow gained sentience. Picking it up must be like handling a living scarf.\
                        What amazes me is how flexible it is. It can curl up into a tiny ball when it wants, but the moment it relaxes—boom, maximum length achieved. It's like it has two modes: 'compact' \
                        and 'ridiculously extended.'Long cats are a gift to this world, and I will not be convinced otherwise.",
                "views": 60,
                "likes": 32,
                "img_url": "https://www.fourpaws.com/-/media/Project/OneWeb/FourPaws/Images/articles/cat-corner/large-cat-breeds/bengal-cat.jpg"},
                "Cubic cat??!?!?!!": {"description":"Okay, I need to talk about this absolute unit of a cat I saw—it's basically a cube. Not 'kinda chunky,' not 'a bit round'… no. This cat is \
                    geometrically square. Sitting, loafing, even walking—it somehow maintains this perfect boxy shape like it's been designed in a physics engine. \
                    You could probably measure equal height, width, and length. If you told me someone rendered this cat in a low-poly video game, I'd believe you. \
                    And the best part? It looks so content. Just a calm, perfectly cubic being, existing in all its right-angled glory. Honestly, I think we should all \
                    aspire to that level of stability.",
                          "views": 65,
                          "likes": 41,
                          "img_url": "https://pbs.twimg.com/media/FZW22-ZUYAAC22n.png",
                          "created_at": timezone.now() - timedelta(days=10)},
                "Distubance in Aberdeenshire Water": {"description": "A previously overlooked coastal village in northern Scotland has unexpectedly become the focus of \
                    international attention after residents reported a series of unusual low-frequency sounds emanating from beneath the seabed.\
                    The phenomenon, first noticed by local fishermen earlier this month, has since been recorded by independent researchers, who describe it as a 'rhythmic, almost mechanical hum'\
                    occurring at irregular intervals. While initial theories pointed to underwater geological activity, recent analyses suggest the pattern does not match known seismic or volcanic signatures.",
                        "views": 110,
                        "likes": 41,
                        "img_url": ""}}
    
    comment_dict = {"c1": {"content": "Wow this is so cool!!!",
                           "likes": 12},
                    "c2": {"content": "Thank you for sharing. Very helpful information!",
                           "likes": 13},
                    "c3": {"content": "This is super inspiring!",
                           "likes": 18},
    }

    for cat in cat_dict:
        create_category(cat, cat_dict[cat]["description"], cat_dict[cat]["views"], cat_dict[cat]["likes"])
    
    for post in post_dict:
        cat = "Animals"
        if post_dict[post]["img_url"] != "":
            try:
                image_obtainer = requests.get(post_dict[post]["img_url"])
                if image_obtainer.status_code == 200:
                    p = create_post(post, post_dict[post]["description"], post_dict[post]["views"], 
                                post_dict[post]["likes"], Category.objects.get(name=cat))
                    file_name = post_dict[post]['img_url'].split("/")[-1]
                    p.image.save(file_name, ContentFile(image_obtainer.content), save = True)
                else:
                    print("Error obtaining " + str(post["img_url"]))
                    p = create_post(post, post_dict[post]["description"], post_dict[post]["views"], 
                            post_dict[post]["likes"], Category.objects.get(name=cat))
            except ProxyError:
                print("Image searching disallowed - creating data without image.")
                p = create_post(post, post_dict[post]["description"], post_dict[post]["views"], 
                            post_dict[post]["likes"], Category.objects.get(name=cat))
            if "created_at" in post_dict[post]:
                p.created_at = post_dict[post]["created_at"]
                p.save()
        else:
            cat = "UK News"
            create_post(post, post_dict[post]["description"], post_dict[post]["views"], 
                        post_dict[post]["likes"], Category.objects.get(name=cat))
    

    post1 = Post.objects.all()[0]
    post2 = Post.objects.all()[1]
    post3 = Post.objects.all()[2]
    
    create_comment(post1, content = comment_dict["c1"]["content"],
                    likes = comment_dict["c1"]["likes"])
    create_comment(post2, content = comment_dict["c2"]["content"],
                    likes = comment_dict["c2"]["likes"])
    create_comment(post3, content = comment_dict["c3"]["content"],
                    likes = comment_dict["c3"]["likes"])

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
    p.slug = slugify(title)
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