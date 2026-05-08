from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CultureRequest, RequestCluster
from .serializers import (
    CultureRequestCreateSerializer,
    CultureRequestDetailSerializer,
    CultureRequestListSerializer,
    RequestClusterDetailSerializer,
    RequestClusterListSerializer,
)


def extract_simple_keywords(text):
    """
    MVP용 간단 키워드 추출 함수입니다.

    추후 AI 담당자가 embedding 또는 LLM 기반 키워드 추출로 교체할 수 있습니다.
    지금은 요청 내용에서 문화콜 주제와 관련 있는 단어만 간단히 잡습니다.
    """

    keyword_candidates = [
        "전통",
        "공예",
        "한지",
        "국악",
        "공연",
        "전시",
        "체험",
        "클래스",
        "청년",
        "청소년",
        "고령층",
        "가족",
        "지역",
        "작가",
        "음악",
        "미술",
        "무용",
        "문화",
    ]

    found_keywords = []

    for keyword in keyword_candidates:
        if keyword in text and keyword not in found_keywords:
            found_keywords.append(keyword)

    return ",".join(found_keywords)


def find_or_create_cluster(culture_request):
    """
    MVP용 간단 군집화 함수입니다.

    기준:
    1. 같은 시/도
    2. 같은 시/군/구
    3. 같은 카테고리
    4. 같은 선호 시간대

    위 조건이 맞는 군집이 있으면 기존 군집에 연결하고,
    없으면 새 군집을 생성합니다.

    추후 AI 담당자가 이 함수를 services/ai_cluster.py로 분리하고,
    embedding 유사도 기반으로 교체하면 됩니다.
    """

    cluster = RequestCluster.objects.filter(
        sido=culture_request.sido,
        sigungu=culture_request.sigungu,
        main_category=culture_request.category,
        preferred_time=culture_request.preferred_time,
        status__in=["GATHERING", "READY"],
    ).first()

    if cluster is not None:
        return cluster

    category_display = culture_request.get_category_display()
    time_display = culture_request.get_preferred_time_display()

    title = f"{culture_request.region_label} {time_display} {category_display} 요청"

    summary = (
        f"{culture_request.region_label} 지역에서 "
        f"{time_display}에 참여 가능한 {category_display} 문화 프로그램에 대한 요청입니다."
    )

    cluster = RequestCluster.objects.create(
        title=title,
        summary=summary,
        sido=culture_request.sido,
        sigungu=culture_request.sigungu,
        region_label=culture_request.region_label,
        main_category=culture_request.category,
        target_age=culture_request.target_age,
        preferred_time=culture_request.preferred_time,
        budget_range=culture_request.budget_range,
        request_count=0,
        threshold=30,
        status="GATHERING",
    )

    return cluster


class CultureRequestListCreateView(APIView):
    """
    문화 요청 목록 조회 및 생성 API입니다.

    GET /api/requests/
    POST /api/requests/
    """

    def get(self, request):
        queryset = CultureRequest.objects.select_related("cluster").all()

        sido = request.query_params.get("sido")
        sigungu = request.query_params.get("sigungu")
        category = request.query_params.get("category")
        preferred_time = request.query_params.get("preferred_time")
        budget_range = request.query_params.get("budget_range")

        if sido:
            queryset = queryset.filter(sido=sido)

        if sigungu:
            queryset = queryset.filter(sigungu=sigungu)

        if category:
            queryset = queryset.filter(category=category)

        if preferred_time:
            queryset = queryset.filter(preferred_time=preferred_time)

        if budget_range:
            queryset = queryset.filter(budget_range=budget_range)

        serializer = CultureRequestListSerializer(queryset, many=True)

        return Response(
            {
                "count": queryset.count(),
                "requests": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CultureRequestCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": "문화 요청 등록에 실패했습니다.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        culture_request = serializer.save()

        combined_text = f"{culture_request.title} {culture_request.content}"
        culture_request.keywords = extract_simple_keywords(combined_text)

        cluster = find_or_create_cluster(culture_request)

        culture_request.cluster = cluster
        culture_request.status = "CLUSTERED"
        culture_request.save(update_fields=["keywords", "cluster", "status", "updated_at"])

        cluster.refresh_request_count()

        response_serializer = CultureRequestDetailSerializer(culture_request)

        return Response(
            {
                "message": "문화 요청이 등록되었습니다.",
                "request": response_serializer.data,
                "cluster": {
                    "id": cluster.id,
                    "title": cluster.title,
                    "summary": cluster.summary,
                    "request_count": cluster.request_count,
                    "threshold": cluster.threshold,
                    "status": cluster.status,
                    "status_display": cluster.get_status_display(),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CultureRequestDetailView(RetrieveAPIView):
    """
    문화 요청 상세 조회 API입니다.

    GET /api/requests/{id}/
    """

    queryset = CultureRequest.objects.select_related("cluster").all()
    serializer_class = CultureRequestDetailSerializer


class RequestClusterListView(ListAPIView):
    """
    요청 군집 목록 조회 API입니다.

    GET /api/clusters/
    """

    serializer_class = RequestClusterListSerializer

    def get_queryset(self):
        queryset = RequestCluster.objects.all()

        sido = self.request.query_params.get("sido")
        sigungu = self.request.query_params.get("sigungu")
        status_value = self.request.query_params.get("status")
        main_category = self.request.query_params.get("main_category")
        preferred_time = self.request.query_params.get("preferred_time")

        if sido:
            queryset = queryset.filter(sido=sido)

        if sigungu:
            queryset = queryset.filter(sigungu=sigungu)

        if status_value:
            queryset = queryset.filter(status=status_value)

        if main_category:
            queryset = queryset.filter(main_category=main_category)

        if preferred_time:
            queryset = queryset.filter(preferred_time=preferred_time)

        return queryset


class RequestClusterDetailView(RetrieveAPIView):
    """
    요청 군집 상세 조회 API입니다.

    GET /api/clusters/{id}/
    """

    queryset = RequestCluster.objects.prefetch_related("requests").all()
    serializer_class = RequestClusterDetailSerializer


@api_view(["GET"])
def request_options_view(request):
    """
    FE에서 선택지 값을 하드코딩하지 않도록 내려주는 API입니다.

    GET /api/requests/options/

    프론트가 이 API를 쓰면 백엔드 choice 값과 FE 버튼 값이 어긋나는 문제를 줄일 수 있습니다.
    """

    return Response(
        {
            "categories": [
                {"value": value, "label": label}
                for value, label in CultureRequest.CATEGORY_CHOICES
            ],
            "time_slots": [
                {"value": value, "label": label}
                for value, label in CultureRequest.TIME_SLOT_CHOICES
            ],
            "budget_ranges": [
                {"value": value, "label": label}
                for value, label in CultureRequest.BUDGET_CHOICES
            ],
            "target_ages": [
                {"value": value, "label": label}
                for value, label in CultureRequest.TARGET_AGE_CHOICES
            ],
            "cluster_statuses": [
                {"value": value, "label": label}
                for value, label in RequestCluster.STATUS_CHOICES
            ],
        },
        status=status.HTTP_200_OK,
    )