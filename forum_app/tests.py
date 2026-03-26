from django.test import TestCase
from django.urls import reverse
from .models import Category, Post, Comment, UserProfile, User

# Create your tests here.

class IndexViewTests(TestCase):

    def test_index_view_no_posts_or_categories(self):
        # No posts should mean "There are no posts!" is displayed
        # No categories should mean "No categories yet!" is displayed
        response = self.client.get(reverse("forum_app:index")) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts!")
        self.assertContains(response, "No categories yet!")

    def test_index_view_with_category_no_posts(self):
        # No posts should mean "There are no posts!" is displayed
        Category.objects.create(name="Sport", description="sporting news")
        response = self.client.get(reverse("forum_app:index")) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts!")
        self.assertContains(response, "Sport")
        # Should not have the "no categories" message 
        self.assertNotContains(response, "No categories yet!")

    def test_index_view_with_category_and_post(self):
        # No posts should mean "There are no posts!" is displayed
        User.objects.create(username="user1", password="password1")
        Category.objects.create(name="Sport", description="sporting news")
        Post.objects.create(category=Category.objects.get(name="Sport"),
                            creator=User.objects.get(username="user1"),
                            title="My Post",
                            content="My post is so epic!")

        response = self.client.get(reverse("forum_app:index")) 
        self.assertEqual(response.status_code, 200)
        # Should display username
        self.assertContains(response, "user1")
        # Should display title
        self.assertContains(response, "My Post")
        # Should display post content
        self.assertContains(response, "My post is so epic!")
        # The category should be available on LHS and in the post
        self.assertContains(response, "Sport")
        # "Trending Posts" should be displayed
        self.assertContains(response, "Trending Posts")
        # "Views and likes should be 0"
        self.assertContains(response, "Views: 0")
        self.assertContains(response, "Likes: 0")
        # Should not have the "no categories" message 
        self.assertNotContains(response, "No categories yet!")


class CategoryViewTests(TestCase):

    def test_category_view_no_posts(self):
        # No posts should mean "There are no posts!" is displayed
        Category.objects.create(name="Sport", description="sporting news")

        response = self.client.get(reverse("forum_app:show_category",
                                           kwargs={"category_name_slug": "sport"} )) 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no posts in this category yet.")
        self.assertContains(response, "Sport Forums")
    

    def test_category_with_post(self):

        User.objects.create(username="user1", password="password1")
        Category.objects.create(name="Sport", description="sporting news")
        Post.objects.create(category=Category.objects.get(name="Sport"),
                            creator=User.objects.get(username="user1"),
                            title="My Post",
                            content="My post is so epic and is about sports!")

        response = self.client.get(reverse("forum_app:show_category",
                                           kwargs={"category_name_slug": "sport"})) 
        self.assertEqual(response.status_code, 200)
        # Should display username
        self.assertContains(response, "user1")
        # Should display title
        self.assertContains(response, "My Post")
        # Should display post content
        self.assertContains(response, "My post is so epic and is about sports!")
        # The category should be available on LHS and in the post
        self.assertContains(response, "Sport")
        # "Views and likes should be 0"
        self.assertContains(response, "Views: 0")
        self.assertContains(response, "Likes: 0")
        # Should not have the "no categories" message 
        self.assertNotContains(response, "No categories yet!")


class LoginViewTests(TestCase):
    
    def test_login_view_has_content_no_categories(self):
        response = self.client.get(reverse("forum_app:login"))
        # Check for form contents
        self.assertContains(response, "Welcome Back")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Remember Me?")
        self.assertContains(response, "No Account?")
        # Check for buttons
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")
        # Ensure categories sidebar displays as expected
        self.assertContains(response, "No categories yet!")

    def test_login_view_has_categories(self):
        response = self.client.get(reverse("forum_app:login"))
        Category.objects.create(name="Sport", description="sporting news")
        # Check for form contents
        self.assertContains(response, "Welcome Back")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Remember Me?")
        self.assertContains(response, "No Account?")
        # Check for buttons
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")
        # Check categories sidebar displays as expected
        self.assertContains("Sport")
        self.assertNotContains(response, "No categories yet!")


class RegisterViewTests(TestCase):

    def test_reister_view_has_content_no_categories(self):
        response = self.client.get(reverse("forum_app:register"))
        # Check for form contents
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Email Address:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Bio:")
        self.assertContains(response, "Picture:")
        # Check categories sidebar displays as expected
        self.assertContains(response, "No categories yet!")

    def test_reister_view_has_content_with_categories(self):
        response = self.client.get(reverse("forum_app:register"))
        Category.objects.create(name="Sport", description="sporting news")
        # Check for form contents
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Username:")
        self.assertContains(response, "Email Address:")
        self.assertContains(response, "Password:")
        self.assertContains(response, "Bio:")
        self.assertContains(response, "Picture:")
        # Check categories sidebar displays as expected
        self.assertContains(response, "Sport")
        self.assertNotContains(response, "No categories yet!")

