from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("apps/", views.app_list, name="app_list"),
    path("apps/<slug:slug>/", views.app_detail, name="app_detail"),
]
