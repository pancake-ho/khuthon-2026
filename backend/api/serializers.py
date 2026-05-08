from rest_framework import serializers

from .models import CultureRequest, RequestCluster, CultureProgram


class RequestClusterSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(read_only=True)
    status_message = serializers.CharField(read_only=True)
    is_ready = serializers.BooleanField(read_only=True)

    class Meta:
        model = RequestCluster
        fields = [
            "id",
            "title",
            "summary",
            "sido",
            "sigungu",
            "region_label",
            "main_category",
            "target_age",
            "preferred_time",
            "budget_range",
            "request_count",
            "threshold",
            "progress_ratio",
            "remaining_count",
            "is_ready",
            "status",
            "status_display",
            "status_message",
            "fair_score",
            "fair_reason",
            "representative_text",
            "created_at",
            "updated_at",
        ]


class CultureRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureRequest
        fields = [
            "id",
            "sido",
            "sigungu",
            "region_label",
            "main_category",
            "target_age",
            "preferred_time",
            "budget_range",
            "title",
            "content",
            "created_at",
        ]
        read_only_fields = ["id", "region_label", "created_at"]


class CultureRequestDetailSerializer(serializers.ModelSerializer):
    cluster = RequestClusterSerializer(read_only=True)

    class Meta:
        model = CultureRequest
        fields = [
            "id",
            "sido",
            "sigungu",
            "region_label",
            "main_category",
            "target_age",
            "preferred_time",
            "budget_range",
            "title",
            "content",
            "cluster",
            "created_at",
        ]


class CultureRequestCreateResponseSerializer(serializers.Serializer):
    request = CultureRequestDetailSerializer()
    cluster = RequestClusterSerializer()


class CultureProgramSerializer(serializers.ModelSerializer):
    cluster = RequestClusterSerializer(read_only=True)

    class Meta:
        model = CultureProgram
        fields = [
            "id",
            "cluster",
            "title",
            "description",
            "place_name",
            "address",
            "creator_name",
            "is_local_creator",
            "is_small_creator",
            "is_traditional",
            "created_at",
        ]