from django.contrib import admin

from .models import (
    CultureRequest,
    RequestCluster,
    Creator,
    PublicSpace,
    ProgramProposal,
)


@admin.register(CultureRequest)
class CultureRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "region_label",
        "category",
        "target_age",
        "preferred_time",
        "budget_range",
        "status",
        "cluster",
        "created_at",
    )
    list_filter = (
        "category",
        "target_age",
        "preferred_time",
        "budget_range",
        "status",
        "sido",
    )
    search_fields = (
        "title",
        "content",
        "region_label",
        "keywords",
    )
    readonly_fields = (
        "region_label",
        "keywords",
        "status",
        "cluster",
        "created_at",
        "updated_at",
    )


@admin.register(RequestCluster)
class RequestClusterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "region_label",
        "main_category",
        "preferred_time",
        "request_count",
        "threshold",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "main_category",
        "preferred_time",
        "sido",
    )
    search_fields = (
        "title",
        "summary",
        "region_label",
    )
    readonly_fields = (
        "request_count",
        "created_at",
        "updated_at",
    )
    actions = ["mark_ready"]

    def mark_ready(self, request, queryset):
        queryset.update(status="READY")
    mark_ready.short_description = "선택한 문화콜을 프로그램 생성 가능 상태로 변경"


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "region_label",
        "category",
        "is_local_creator",
        "is_traditional",
        "created_at",
    )
    list_filter = (
        "category",
        "region_label",
        "is_local_creator",
        "is_traditional",
    )
    search_fields = (
        "name",
        "description",
        "region_label",
    )


@admin.register(PublicSpace)
class PublicSpaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "region_label",
        "capacity",
        "available_time",
        "good_for",
        "created_at",
    )
    list_filter = (
        "region_label",
        "available_time",
    )
    search_fields = (
        "name",
        "address",
        "description",
        "good_for",
    )


@admin.register(ProgramProposal)
class ProgramProposalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "cluster",
        "creator",
        "space",
        "expected_fee",
        "expected_time",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "expected_fee",
        "expected_time",
    )
    search_fields = (
        "title",
        "description",
        "cultural_context",
        "accessibility_note",
    )