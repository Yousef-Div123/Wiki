from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("random/", views.random, name = "random"),
    path("new/", views.new, name ="new"),
    path("edit/<str:entry>", views.edit, name = "edit")
]
