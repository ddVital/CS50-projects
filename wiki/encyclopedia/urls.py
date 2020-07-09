from django.urls import path, re_path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_title>", views.wiki_page, name="wiki_page"),
    path("wiki/", views.random_page, name="random_page"),
    path("create", views.add_entry, name="add_entry"),
    path("search", views.search, name="search"),
    path("wiki/edit/<str:page_title>", views.edit_page, name="edit_page")
]
