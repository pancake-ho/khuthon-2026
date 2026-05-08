from django.urls import path

from .views import (
    CultureRequestDetailView,
    CultureRequestListCreateView,
    RequestClusterDetailView,
    RequestClusterListView,
    request_options_view,
    dashboard_summary_view,
)

urlpatterns = [
    path("dashboard/", dashboard_summary_view, name="dashboard-summary"),

    path("requests/", CultureRequestListCreateView.as_view(), name="request-list-create"),
    path("requests/options/", request_options_view, name="request-options"),
    path("requests/<int:pk>/", CultureRequestDetailView.as_view(), name="request-detail"),

    path("clusters/", RequestClusterListView.as_view(), name="cluster-list"),
    path("clusters/<int:pk>/", RequestClusterDetailView.as_view(), name="cluster-detail"),
]