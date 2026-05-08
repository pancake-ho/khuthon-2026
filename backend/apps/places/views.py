from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CultureRequest,
    RequestCluster,
    Creator,
    PublicSpace,
    ProgramProposal,
)
from .serializers import (
    CultureRequestCreateSerializer,
    CultureRequestDetailSerializer,
    CultureRequestListSerializer,
    RequestClusterDetailSerializer,
    RequestClusterListSerializer,
    CreatorSerializer,
    PublicSpaceSerializer,
    ProgramProposalSerializer,
)

from django.db import transaction
from apps.places.services.ai_cluster import analyze_and_cluster_request

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

        with transaction.atomic():
            culture_request = serializer.save()
            cluster_result = analyze_and_cluster_request(culture_request)

        response_serializer = CultureRequestDetailSerializer(culture_request)

        return Response(
            {
                "message": "문화 요청이 등록되었습니다.",
                "request": response_serializer.data,
                "ai_result": {
                    "keywords": cluster_result.keywords,
                    "similarity_score": cluster_result.score,
                    "cluster_created": cluster_result.created,
                    "method": "MVP_RULE_BASED_AI_CLUSTERING",
                },
                "cluster": {
                    "id": cluster_result.cluster.id,
                    "title": cluster_result.cluster.title,
                    "summary": cluster_result.cluster.summary,
                    "request_count": cluster_result.cluster.request_count,
                    "threshold": cluster_result.cluster.threshold,
                    "status": cluster_result.cluster.status,
                    "status_display": cluster_result.cluster.get_status_display(),
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

        sort = self.request.query_params.get("sort", "fair")
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

        if sort == "latest":
            queryset = queryset.order_by("-created_at")

        elif sort == "ready":
            queryset = queryset.order_by("-request_count", "-created_at")

        elif sort == "traditional":
            queryset = queryset.order_by("-created_at").filter(main_category="TRADITIONAL")

        else:
            # fair 기본값
            # 아직 DB에서 fair_score 계산 정렬은 안 하므로,
            # MVP에서는 READY 우선 + 요청 수 + 최신순으로 공정 노출 느낌을 줌
            queryset = queryset.order_by("-request_count", "-created_at")

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


@api_view(["GET"])
def dashboard_summary_view(request):
    """
    홈 화면 및 발표용 지표 API입니다.

    GET /api/dashboard/
    """

    total_requests = CultureRequest.objects.count()
    total_clusters = RequestCluster.objects.count()
    ready_clusters = RequestCluster.objects.filter(status="READY").count()
    traditional_requests = CultureRequest.objects.filter(category="TRADITIONAL").count()
    local_requests = CultureRequest.objects.filter(category="LOCAL").count()

    top_regions = (
        CultureRequest.objects
        .values("region_label")
        .order_by("region_label")
    )

    region_count_map = {}
    for item in top_regions:
        region = item["region_label"] or "미지정"
        region_count_map[region] = region_count_map.get(region, 0) + 1

    sorted_regions = sorted(
        region_count_map.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:5]
    

    return Response(
        {
            "total_requests": total_requests,
            "total_clusters": total_clusters,
            "ready_clusters": ready_clusters,
            "traditional_requests": traditional_requests,
            "local_requests": local_requests,
            "top_regions": [
                {"region": region, "count": count}
                for region, count in sorted_regions
            ],
            "message": "문화콜은 사용자의 요청을 모아 지역 문화 프로그램으로 연결합니다.",
        },
        status=status.HTTP_200_OK,
    )


class CreatorListView(ListAPIView):
    """
    지역 창작자 목록 조회 API입니다.

    GET /api/creators/
    """

    serializer_class = CreatorSerializer

    def get_queryset(self):
        queryset = Creator.objects.all()

        region_label = self.request.query_params.get("region_label")
        category = self.request.query_params.get("category")
        is_traditional = self.request.query_params.get("is_traditional")

        if region_label:
            queryset = queryset.filter(region_label__icontains=region_label)

        if category:
            queryset = queryset.filter(category__icontains=category)

        if is_traditional in ["true", "True", "1"]:
            queryset = queryset.filter(is_traditional=True)

        return queryset


class PublicSpaceListView(ListAPIView):
    """
    공공공간 목록 조회 API입니다.

    GET /api/spaces/
    """

    serializer_class = PublicSpaceSerializer

    def get_queryset(self):
        queryset = PublicSpace.objects.all()

        region_label = self.request.query_params.get("region_label")
        good_for = self.request.query_params.get("good_for")

        if region_label:
            queryset = queryset.filter(region_label__icontains=region_label)

        if good_for:
            queryset = queryset.filter(good_for__icontains=good_for)

        return queryset


class ProgramProposalListView(ListAPIView):
    """
    프로그램 후보 목록 조회 API입니다.

    GET /api/programs/
    """

    serializer_class = ProgramProposalSerializer

    def get_queryset(self):
        queryset = ProgramProposal.objects.select_related(
            "cluster",
            "creator",
            "space",
        ).all()

        status_value = self.request.query_params.get("status")
        region_label = self.request.query_params.get("region_label")

        if status_value:
            queryset = queryset.filter(status=status_value)

        if region_label:
            queryset = queryset.filter(cluster__region_label__icontains=region_label)

        return queryset