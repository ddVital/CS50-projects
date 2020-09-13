from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<username>", views.user_page, name="user_page"),
    path("new", views.create_listing, name="create_listing"),
    path("watchlist/add/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<id>", views.view_item, name="view_item"),
    path("close/<page_id>", views.close_listing, name="close_listing")
]
