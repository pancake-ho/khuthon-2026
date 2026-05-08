from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .ai.clustering_engine import CultureCallClusteringEngine
from .models import CultureRequest, RequestCluster, CultureProgram
from .serializers import (
    CultureRequestCreateSerializer,
    CultureRequestDetailSerializer,
    RequestClusterSerializer,
    CultureProgramSerializer,
)


@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "ok",
            "message": "문화콜 API 서버가 정상 작동 중입니다.",
        }
    )


@api_view(["GET", "POST"])
def culture_request_list_create(request):
    if request.method == "GET":
        requests = CultureRequest.objects.select_related("cluster").order_by("-created_at")
        serializer = CultureRequestDetailSerializer(requests, many=True)
        return Response(serializer.data)

    serializer = CultureRequestCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    culture_request = serializer.save()

    try:
        engine = CultureCallClusteringEngine()
        cluster = engine.assign_request_to_cluster(culture_request)
    except Exception as exc:
        culture_request.delete()
        return Response(
            {
                "error": "AI 군집화 처리 중 오류가 발생했습니다.",
                "detail": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    culture_request.refresh_from_db()
    cluster.refresh_from_db()

    return Response(
        {
            "request": CultureRequestDetailSerializer(culture_request).data,
            "cluster": RequestClusterSerializer(cluster).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def culture_request_detail(request, pk):
    try:
        culture_request = CultureRequest.objects.select_related("cluster").get(pk=pk)
    except CultureRequest.DoesNotExist:
        return Response(
            {"error": "해당 문화 요청을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CultureRequestDetailSerializer(culture_request)
    return Response(serializer.data)


@api_view(["GET"])
def cluster_list(request):
    clusters = RequestCluster.objects.order_by("-updated_at")

    status_filter = request.GET.get("status")
    if status_filter:
        clusters = clusters.filter(status=status_filter)

    sido = request.GET.get("sido")
    if sido:
        clusters = clusters.filter(sido=sido)

    sigungu = request.GET.get("sigungu")
    if sigungu:
        clusters = clusters.filter(sigungu=sigungu)

    serializer = RequestClusterSerializer(clusters, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def ready_cluster_list(request):
    clusters = RequestCluster.objects.filter(
        status=RequestCluster.Status.READY
    ).order_by("-fair_score", "-updated_at")

    serializer = RequestClusterSerializer(clusters, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def cluster_detail(request, pk):
    try:
        cluster = RequestCluster.objects.get(pk=pk)
    except RequestCluster.DoesNotExist:
        return Response(
            {"error": "해당 문화콜 군집을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = RequestClusterSerializer(cluster)
    return Response(serializer.data)


@api_view(["POST"])
def create_program_from_cluster(request, pk):
    try:
        cluster = RequestCluster.objects.get(pk=pk)
    except RequestCluster.DoesNotExist:
        return Response(
            {"error": "해당 문화콜 군집을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if cluster.status != RequestCluster.Status.READY:
        return Response(
            {
                "error": "아직 프로그램으로 생성할 수 없는 군집입니다.",
                "request_count": cluster.request_count,
                "threshold": cluster.threshold,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    program, created = CultureProgram.objects.get_or_create(
        cluster=cluster,
        defaults={
            "title": cluster.title.replace("요청", "문화 프로그램"),
            "description": (
                f"{cluster.summary}\n\n"
                f"대표 요청: {cluster.representative_text}\n\n"
                "이 프로그램은 지역 주민의 반복 요청을 기반으로 생성된 문화콜 프로그램 후보입니다."
            ),
            "place_name": "",
            "address": cluster.region_label,
            "creator_name": "지역 창작자 매칭 예정",
            "is_local_creator": True,
            "is_small_creator": True,
            "is_traditional": cluster.main_category == CultureRequest.MainCategory.TRADITION,
        },
    )

    cluster.status = RequestCluster.Status.PROGRAM_CREATED
    cluster.save(update_fields=["status", "updated_at"])

    serializer = CultureProgramSerializer(program)
    return Response(
        {
            "created": created,
            "program": serializer.data,
        },
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(["GET"])
def program_list(request):
    programs = CultureProgram.objects.select_related("cluster").order_by("-created_at")
    serializer = CultureProgramSerializer(programs, many=True)
    return Response(serializer.data)