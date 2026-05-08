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
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    progress_ratio = serializers.SerializerMethodField()
    remaining_count = serializers.SerializerMethodField()
    is_ready = serializers.SerializerMethodField()
    status_message = serializers.SerializerMethodField()
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
            "progress_ratio",
            "remaining_count",
            "is_ready",
            "status",
            "status_display",
            "status_message",
            "requests",
            "created_at",
            "updated_at",
        ]

    def get_progress_ratio(self, obj):
        if obj.threshold <= 0:
            return 0
        return min(round((obj.request_count / obj.threshold) * 100, 1), 100)

    def get_remaining_count(self, obj):
        return max(obj.threshold - obj.request_count, 0)

    def get_is_ready(self, obj):
        return obj.request_count >= obj.threshold or obj.status == "READY"

    def get_status_message(self, obj):
        remaining = max(obj.threshold - obj.request_count, 0)

        if obj.status == "READY":
            return "문화 프로그램으로 제안 가능한 상태입니다."

        if remaining == 0:
            return "문화 프로그램 생성 기준에 도달했습니다."

        return f"{remaining}명의 요청이 더 모이면 문화 프로그램으로 제안됩니다."


class RequestClusterListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    fair_score = serializers.SerializerMethodField()
    fair_reason = serializers.SerializerMethodField()
    progress_ratio = serializers.SerializerMethodField()
    remaining_count = serializers.SerializerMethodField()
    is_ready = serializers.SerializerMethodField()
    status_message = serializers.SerializerMethodField()

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
            "created_at",
            "updated_at",
        ]

    def get_progress_ratio(self, obj):
        if obj.threshold <= 0:
            return 0
        return min(round((obj.request_count / obj.threshold) * 100, 1), 100)

    def get_remaining_count(self, obj):
        return max(obj.threshold - obj.request_count, 0)

    def get_is_ready(self, obj):
        return obj.request_count >= obj.threshold or obj.status == "READY"

    def get_status_message(self, obj):
        remaining = max(obj.threshold - obj.request_count, 0)

        if obj.status == "READY":
            return "문화 프로그램으로 제안 가능한 상태입니다."

        if remaining == 0:
            return "문화 프로그램 생성 기준에 도달했습니다."

        return f"{remaining}명의 요청이 더 모이면 문화 프로그램으로 제안됩니다."
    
    def get_fair_score(self, obj):
        score = 0

        # 1. 활성화 임박도
        if obj.threshold > 0:
            progress = obj.request_count / obj.threshold
            score += min(progress * 40, 40)

        # 2. 전통문화 가중치
        if obj.main_category == "TRADITIONAL":
            score += 20

        # 3. 지역문화 가중치
        if obj.main_category == "LOCAL":
            score += 15

        # 4. 소규모 요청도 보호
        if 5 <= obj.request_count < obj.threshold:
            score += 15

        # 5. 새 요청 부스팅
        score += 10

        return round(score, 1)


    def get_fair_reason(self, obj):
        reasons = []

        if obj.threshold > 0 and obj.request_count >= obj.threshold * 0.7:
            reasons.append("프로그램 생성 기준에 가까운 요청입니다.")

        if obj.main_category == "TRADITIONAL":
            reasons.append("전통문화 지속가능성과 연결됩니다.")

        if obj.main_category == "LOCAL":
            reasons.append("지역문화 활성화와 연결됩니다.")

        if 5 <= obj.request_count < obj.threshold:
            reasons.append("아직 작지만 발견될 필요가 있는 문화 수요입니다.")

        if not reasons:
            reasons.append("사용자 요청 기반으로 형성된 문화 수요입니다.")

        return reasons