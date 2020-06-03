from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("submit_responses", views.submit_responses, name="submit_responses"),
    path("get_student_list", views.get_student_list, name="get_student_list"),
    path("get_student_responses/<int:student_id>", views.get_student_responses, name="get_student_responses")
]
