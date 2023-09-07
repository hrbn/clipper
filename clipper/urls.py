from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.templatetags.static import static
from django.views.generic import RedirectView
from dal import autocomplete
from taggit.models import Tag


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("clip/new", views.new, name="new"),
    path("clip/<int:clip_id>", views.edit_clip, name="edit"),
    path("add/", views.add_clip, name="add"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("about", views.about, name="about"),
    path(
        "account",
        views.account,
        name="account",
    ),
    path("favicon.ico", RedirectView.as_view(url=static("favicon.ico"))),
    re_path(
        "tagcomplete/$",
        autocomplete.Select2QuerySetView.as_view(
            queryset=Tag.objects.all(),
        ),
        name="tagcomplete",
    ),
    path("clip/<int:clip_id>/delete", views.delete, name="delete"),
]
