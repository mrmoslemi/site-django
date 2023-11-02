from django.urls import re_path

from . import views

app_name = "resume"

urlpatterns = [
    re_path(r"^test/$", views.resume_view),
    re_path(r"^md/$", views.resume_md),
]
