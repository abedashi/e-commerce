from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createList", views.createList, name="createList"),
    path("categories", views.categories, name="categories"),
    path("watchList", views.watchList, name="watchList"),
    path("addWatchList/<int:list_id>", views.addWatchList, name="addWatchList"),
    path("watchList/delete/<int:list_id>", views.deleteWatchList, name="deleteWatchList"),
    path("view/<int:list_id>", views.view, name="view"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("comment/<int:list_id>", views.comment, name="comment")
]
