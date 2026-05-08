from django.contrib import admin

from .models import CultureRequest, RequestCluster, CultureProgram


@admin.register(CultureRequest)
class CultureRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "region_label",
        "main_category",
        "target_age",
        "preferred_time",
        "budget_range",
        "cluster",
        "created_at",
    ]
    list_filter = [
        "sido",
        "main_category",
        "target_age",
        "preferred_time",
        "budget_range",
        "created_at",
    ]
    search_fields = ["content", "title", "region_label"]


@admin.register(RequestCluster)
class RequestClusterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "region_label",
        "main_category",
        "request_count",
        "threshold",
        "progress_ratio",
        "status",
        "fair_score",
        "updated_at",
    ]
    list_filter = [
        "status",
        "sido",
        "main_category",
        "target_age",
        "preferred_time",
        "budget_range",
    ]
    search_fields = ["title", "summary", "representative_text", "region_label"]


@admin.register(CultureProgram)
class CultureProgramAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "place_name",
        "creator_name",
        "is_local_creator",
        "is_small_creator",
        "is_traditional",
        "created_at",
    ]
    list_filter = [
        "is_local_creator",
        "is_small_creator",
        "is_traditional",
        "created_at",
    ]
    search_fields = ["title", "description", "creator_name", "place_name"]