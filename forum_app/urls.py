from django.urls import path
from forum_app import views

app_name = 'forum_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_post/', views.add_post, name='add_post'),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("post/<int:post_id>/", views.show_post, name="show_post"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
]