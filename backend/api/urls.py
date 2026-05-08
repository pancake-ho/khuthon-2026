from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health_check),

    path("requests/", views.culture_request_list_create),
    path("requests/<int:pk>/", views.culture_request_detail),

    path("clusters/", views.cluster_list),
    path("clusters/ready/", views.ready_cluster_list),
    path("clusters/<int:pk>/", views.cluster_detail),

    path("clusters/<int:pk>/create-program/", views.create_program_from_cluster),

    path("programs/", views.program_list),
]