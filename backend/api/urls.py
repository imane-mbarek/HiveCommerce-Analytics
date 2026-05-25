from django.urls import path

from . import views


urlpatterns = [
    path("health/", views.health_check, name="health-check"),
    path("project/", views.project_info, name="project-info"),
]

