from rest_framework import serializers

from .models import CultureRequest, RequestCluster


class CultureRequestCreateSerializer(serializers.ModelSerializer):
    """
    FE에서 문화 요청을 작성할 때 사용하는 serializer입니다.

    FE가 보내야 하는 핵심 값:
    - title
    - content
    - sido
    - sigungu
    - category
    - target_age
    - preferred_time
    - budget_range
    """

    class Meta:
        model = CultureRequest
        fields = [
            "id",
            "requester_nickname",
            "title",
            "content",
            "sido",
            "sigungu",
            "region_label",
            "category",
            "target_age",
            "preferred_time",
            "budget_range",
            "mobility_limit",
            "keywords",
            "status",
            "cluster",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "region_label",
            "keywords",
            "status",
            "cluster",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("요청 제목은 2자 이상 입력해야 합니다.")
        return value.strip()

    def validate_content(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("요청 내용은 5자 이상 입력해야 합니다.")
        return value.strip()

    def validate_sido(self, value):
        if not value.strip():
            raise serializers.ValidationError("시/도를 선택해야 합니다.")
        return value.strip()

    def validate_sigungu(self, value):
        if not value.strip():
            raise serializers.ValidationError("시/군/구를 선택해야 합니다.")
        return value.strip()


class CultureRequestListSerializer(serializers.ModelSerializer):
    """
    문화 요청 목록 조회용 serializer입니다.
    목록 화면에서는 너무 많은 내용을 보내지 않고 필요한 값만 보냅니다.
    """

    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )
    target_age_display = serializers.CharField(
        source="get_target_age_display",
        read_only=True,
    )
    preferred_time_display = serializers.CharField(
        source="get_preferred_time_display",
        read_only=True,
    )
    budget_range_display = serializers.CharField(
        source="get_budget_range_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    cluster_title = serializers.CharField(
        source="cluster.title",
        read_only=True,
    )

    class Meta:
        model = CultureRequest
        fields = [
            "id",
            "title",
            "content",
            "region_label",
            "sido",
            "sigungu",
            "category",
            "category_display",
            "target_age",
            "target_age_display",
            "preferred_time",
            "preferred_time_display",
            "budget_range",
            "budget_range_display",
            "status",
            "status_display",
            "cluster",
            "cluster_title",
            "created_at",
        ]


class CultureRequestDetailSerializer(serializers.ModelSerializer):
    """
    문화 요청 상세 조회용 serializer입니다.
    """

    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True,
    )
    target_age_display = serializers.CharField(
        source="get_target_age_display",
        read_only=True,
    )
    preferred_time_display = serializers.CharField(
        source="get_preferred_time_display",
        read_only=True,
    )
    budget_range_display = serializers.CharField(
        source="get_budget_range_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    cluster_title = serializers.CharField(
        source="cluster.title",
        read_only=True,
    )

    class Meta:
        model = CultureRequest
        fields = [
            "id",
            "requester_nickname",
            "title",
            "content",
            "sido",
            "sigungu",
            "region_label",
            "category",
            "category_display",
            "target_age",
            "target_age_display",
            "preferred_time",
            "preferred_time_display",
            "budget_range",
            "budget_range_display",
            "mobility_limit",
            "keywords",
            "status",
            "status_display",
            "cluster",
            "cluster_title",
            "created_at",
            "updated_at",
        ]


class RequestClusterListSerializer(serializers.ModelSerializer):
    """
    요청 군집 목록 조회용 serializer입니다.
    """

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

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
            "status",
            "status_display",
            "created_at",
            "updated_at",
        ]


class RequestClusterDetailSerializer(serializers.ModelSerializer):
    """
    요청 군집 상세 조회용 serializer입니다.
    군집에 포함된 요청 목록도 함께 내려줍니다.
    """

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    requests = CultureRequestListSerializer(
        many=True,
        read_only=True,
    )

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
            "status",
            "status_display",
            "requests",
            "created_at",
            "updated_at",
        ]