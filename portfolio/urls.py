from django.urls import path, include
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("chatbot/", include("chatbot.urls")),
]
