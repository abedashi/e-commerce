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
    path("watchList/view/<int:list_id>", views.viewWatchList, name="viewWatchList"),
    path("view/<int:list_id>", views.view, name="view"),
    path("addWatchList/<int:list_id>", views.addWatchList, name="addWatchList")
]
