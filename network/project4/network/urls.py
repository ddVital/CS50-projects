
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_post", views.new_post, name="new_post"),
    path("user/<str:username>", views.profile, name="profile"),
    path("edit/user/<str:username>", views.edit_user, name="edit_user"),
    path("edit/post/<int:id>", views.edit, name="edit"),
    path("following", views.following, name="following"),
    path("like/<str:post>/<str:user>", views.like, name="like"),
    path("unlike/<str:post>/<str:user>", views.unlike, name="unlike"),
    path("follow/<str:username>", views.follow , name="follow"),
    path("unfollow/<str:username>", views.unfollow , name="unfollow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
