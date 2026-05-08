"""
문화콜 AI 군집화 서비스

현재 MVP에서는 외부 AI API 없이 규칙 기반 유사도 계산으로 동작한다.
다만 views.py에서 직접 군집화하지 않고 이 서비스 계층을 호출하게 만들어서,
추후 AI 담당자가 embedding / LLM / sentence-transformer 기반 로직으로 교체하기 쉽게 만든다.

역할:
1. 문화 요청에서 키워드 추출
2. 기존 RequestCluster와 유사도 계산
3. 가장 유사한 군집이 있으면 연결
4. 없으면 새 군집 생성
"""

from dataclasses import dataclass

from django.db import transaction

from apps.places.models import CultureRequest, RequestCluster


KEYWORD_CANDIDATES = [
    "전통",
    "전통문화",
    "공예",
    "한지",
    "도자기",
    "국악",
    "한복",
    "민속",
    "공연",
    "연극",
    "뮤지컬",
    "전시",
    "체험",
    "클래스",
    "청년",
    "청소년",
    "고령층",
    "가족",
    "지역",
    "로컬",
    "작가",
    "창작자",
    "음악",
    "미술",
    "무용",
    "문화",
]


@dataclass
class ClusterResult:
    cluster: RequestCluster
    keywords: str
    score: float
    created: bool


def normalize_text(text: str) -> str:
    """
    간단한 텍스트 정규화 함수.
    추후 AI embedding을 사용할 경우 이 함수는 전처리 함수로 유지 가능하다.
    """
    if not text:
        return ""

    return text.strip().lower()


def extract_keywords_from_request(culture_request: CultureRequest) -> str:
    """
    CultureRequest의 제목, 내용, 카테고리, 지역 정보를 바탕으로 키워드를 추출한다.

    현재는 MVP용 키워드 매칭 방식이다.
    추후에는 이 함수 내부만 LLM/embedding 기반 키워드 추출로 교체하면 된다.
    """
    combined_text = normalize_text(
        f"{culture_request.title} "
        f"{culture_request.content} "
        f"{culture_request.region_label} "
        f"{culture_request.get_category_display()} "
        f"{culture_request.get_target_age_display()}"
    )

    found_keywords = []

    for keyword in KEYWORD_CANDIDATES:
        if keyword.lower() in combined_text and keyword not in found_keywords:
            found_keywords.append(keyword)

    if culture_request.category == "TRADITIONAL" and "전통문화" not in found_keywords:
        found_keywords.append("전통문화")

    if culture_request.category == "LOCAL" and "지역" not in found_keywords:
        found_keywords.append("지역")

    return ",".join(found_keywords)


def keyword_set(keyword_text: str) -> set[str]:
    if not keyword_text:
        return set()

    return {
        keyword.strip()
        for keyword in keyword_text.split(",")
        if keyword.strip()
    }


def calculate_cluster_score(
    culture_request: CultureRequest,
    cluster: RequestCluster,
    request_keywords: str,
) -> float:
    """
    기존 군집과 새 요청의 유사도를 계산한다.

    점수 기준:
    - 같은 시/도: +20
    - 같은 시/군/구: +25
    - 같은 문화 분야: +25
    - 같은 선호 시간대: +10
    - 같은 대상 연령: +10
    - 같은 예산 범위: +5
    - 키워드 겹침: 최대 +20

    총점이 높을수록 같은 군집으로 볼 가능성이 높다.
    """

    score = 0.0

    if cluster.sido == culture_request.sido:
        score += 20

    if cluster.sigungu == culture_request.sigungu:
        score += 25

    if cluster.main_category == culture_request.category:
        score += 25

    if cluster.preferred_time == culture_request.preferred_time:
        score += 10

    if cluster.target_age == culture_request.target_age:
        score += 10

    if cluster.budget_range == culture_request.budget_range:
        score += 5

    request_keyword_set = keyword_set(request_keywords)

    cluster_text = normalize_text(
        f"{cluster.title} {cluster.summary} {cluster.main_category}"
    )

    cluster_keywords = {
        keyword
        for keyword in KEYWORD_CANDIDATES
        if keyword.lower() in cluster_text
    }

    if request_keyword_set and cluster_keywords:
        intersection_count = len(request_keyword_set & cluster_keywords)
        union_count = len(request_keyword_set | cluster_keywords)

        if union_count > 0:
            keyword_score = (intersection_count / union_count) * 20
            score += keyword_score

    return round(score, 2)


def create_cluster_from_request(culture_request: CultureRequest) -> RequestCluster:
    """
    새 요청과 맞는 기존 군집이 없을 때 새 RequestCluster를 생성한다.
    """
    category_display = culture_request.get_category_display()
    time_display = culture_request.get_preferred_time_display()
    target_display = culture_request.get_target_age_display()

    title = (
        f"{culture_request.region_label} "
        f"{time_display} "
        f"{category_display} 요청"
    )

    summary = (
        f"{culture_request.region_label} 지역에서 "
        f"{target_display} 사용자가 "
        f"{time_display}에 참여 가능한 "
        f"{category_display} 문화 프로그램을 요청하고 있습니다."
    )

    return RequestCluster.objects.create(
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
        threshold=3,
        status="GATHERING",
    )


def find_best_cluster(
    culture_request: CultureRequest,
    request_keywords: str,
) -> tuple[RequestCluster | None, float]:
    """
    기존 군집 중 새 요청과 가장 유사한 군집을 찾는다.
    """
    candidate_clusters = RequestCluster.objects.filter(
        status__in=["GATHERING", "READY"],
        sido=culture_request.sido,
        sigungu=culture_request.sigungu,
    )

    best_cluster = None
    best_score = 0.0

    for cluster in candidate_clusters:
        score = calculate_cluster_score(
            culture_request=culture_request,
            cluster=cluster,
            request_keywords=request_keywords,
        )

        if score > best_score:
            best_score = score
            best_cluster = cluster

    return best_cluster, best_score


@transaction.atomic
def analyze_and_cluster_request(culture_request: CultureRequest) -> ClusterResult:
    """
    BE에서 호출하는 대표 AI 군집화 함수.

    views.py는 이 함수 하나만 호출하면 된다.
    추후 AI 담당자는 이 함수 내부 구현만 교체하면 된다.
    """
    request_keywords = extract_keywords_from_request(culture_request)

    best_cluster, best_score = find_best_cluster(
        culture_request=culture_request,
        request_keywords=request_keywords,
    )

    # MVP 기준: 60점 이상이면 같은 군집으로 연결
    if best_cluster is not None and best_score >= 60:
        cluster = best_cluster
        created = False
    else:
        cluster = create_cluster_from_request(culture_request)
        created = True
        best_score = 100.0

    culture_request.keywords = request_keywords
    culture_request.cluster = cluster
    culture_request.status = "CLUSTERED"
    culture_request.save(
        update_fields=[
            "keywords",
            "cluster",
            "status",
            "updated_at",
        ]
    )

    cluster.refresh_request_count()

    return ClusterResult(
        cluster=cluster,
        keywords=request_keywords,
        score=best_score,
        created=created,
    )