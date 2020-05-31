from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("submit_responses", views.submit_responses, name="submit_responses")
]
