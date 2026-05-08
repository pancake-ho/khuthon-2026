from typing import Optional

from django.db import transaction

from api.models import CultureRequest, RequestCluster
from . import config
from .embedding_service import EmbeddingService
from .similarity import cosine_similarity


class CultureCallClusteringEngine:
    """
    CultureRequest 1개가 들어왔을 때,
    기존 RequestCluster에 배정하거나 새 RequestCluster를 생성한다.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

    @transaction.atomic
    def assign_request_to_cluster(self, culture_request: CultureRequest) -> RequestCluster:
        if not culture_request.content:
            raise ValueError("요청 내용 content가 비어 있습니다.")

        embedding = culture_request.embedding

        if not embedding:
            embedding = self.embedding_service.get_embedding(culture_request.content)
            culture_request.embedding = embedding
            culture_request.save(update_fields=["embedding"])

        candidate_clusters = self._get_candidate_clusters(culture_request)

        best_cluster = None
        best_score = -1.0

        for cluster in candidate_clusters:
            if not cluster.centroid:
                continue

            score = cosine_similarity(embedding, cluster.centroid)

            if score > best_score:
                best_score = score
                best_cluster = cluster

        if best_cluster is not None and best_score >= config.SIM_THRESHOLD:
            cluster = self._assign_to_existing_cluster(
                culture_request=culture_request,
                cluster=best_cluster,
            )
        else:
            cluster = self._create_new_cluster(culture_request)

        return cluster

    def _get_candidate_clusters(self, culture_request: CultureRequest):
        """
        기존 AI 로직의 조건을 유지한다.

        기존:
        region, time_slot, budget이 같은 군집만 비교

        개선:
        sido, sigungu, preferred_time, budget_range, main_category, target_age가 같은 군집만 비교
        """
        return RequestCluster.objects.select_for_update().filter(
            sido=culture_request.sido,
            sigungu=culture_request.sigungu,
            preferred_time=culture_request.preferred_time,
            budget_range=culture_request.budget_range,
            main_category=culture_request.main_category,
            target_age=culture_request.target_age,
        ).exclude(
            status=RequestCluster.Status.PROGRAM_CREATED
        )

    def _assign_to_existing_cluster(
        self,
        culture_request: CultureRequest,
        cluster: RequestCluster,
    ) -> RequestCluster:
        culture_request.cluster = cluster
        culture_request.save(update_fields=["cluster"])

        self._refresh_cluster(cluster)
        return cluster

    def _create_new_cluster(self, culture_request: CultureRequest) -> RequestCluster:
        title = self._make_cluster_title(culture_request)
        summary = self._make_cluster_summary(culture_request)

        cluster = RequestCluster.objects.create(
            title=title,
            summary=summary,
            sido=culture_request.sido,
            sigungu=culture_request.sigungu,
            region_label=culture_request.region_label,
            main_category=culture_request.main_category,
            target_age=culture_request.target_age,
            preferred_time=culture_request.preferred_time,
            budget_range=culture_request.budget_range,
            representative_text=culture_request.content,
            centroid=culture_request.embedding,
            request_count=1,
            threshold=config.MIN_CLUSTER_SIZE,
        )

        culture_request.cluster = cluster
        culture_request.save(update_fields=["cluster"])

        self._refresh_cluster(cluster)
        return cluster

    def _refresh_cluster(self, cluster: RequestCluster) -> None:
        requests = list(cluster.requests.all())

        request_count = len(requests)
        cluster.request_count = request_count
        cluster.threshold = config.MIN_CLUSTER_SIZE
        cluster.remaining_count = max(config.MIN_CLUSTER_SIZE - request_count, 0)
        cluster.progress_ratio = min(
            round((request_count / config.MIN_CLUSTER_SIZE) * 100, 1),
            100.0,
        )

        embeddings = [
            request.embedding
            for request in requests
            if request.embedding
        ]

        if embeddings:
            cluster.centroid = self._mean_embedding(embeddings)
            cluster.representative_text = self._find_representative_text(
                requests=requests,
                centroid=cluster.centroid,
            )

        if request_count >= config.MIN_CLUSTER_SIZE:
            cluster.status = RequestCluster.Status.READY
        else:
            cluster.status = RequestCluster.Status.COLLECTING

        cluster.fair_score = self._calculate_fair_score(cluster)
        cluster.fair_reason = self._make_fair_reason(cluster)

        cluster.title = self._make_cluster_title_from_cluster(cluster)
        cluster.summary = self._make_cluster_summary_from_cluster(cluster)

        cluster.save()

    def _mean_embedding(self, embeddings):
        dim = len(embeddings[0])
        result = []

        for i in range(dim):
            value = sum(vector[i] for vector in embeddings) / len(embeddings)
            result.append(value)

        return result

    def _find_representative_text(self, requests, centroid):
        best_text = ""
        best_score = -1.0

        for request in requests:
            if not request.embedding:
                continue

            score = cosine_similarity(request.embedding, centroid)

            if score > best_score:
                best_score = score
                best_text = request.content

        return best_text

    def _calculate_fair_score(self, cluster: RequestCluster) -> float:
        """
        문화콜 주제 적합성을 위한 간단한 공정성 점수.
        전통문화, 지역성, 소규모 문화 가능성을 살짝 부스팅한다.
        """
        score = 50.0

        if cluster.main_category == CultureRequest.MainCategory.TRADITION:
            score += 20.0

        if cluster.target_age in [
            CultureRequest.TargetAge.TEEN,
            CultureRequest.TargetAge.SENIOR,
        ]:
            score += 10.0

        if cluster.budget_range in [
            CultureRequest.BudgetRange.FREE,
            CultureRequest.BudgetRange.UNDER_10000,
        ]:
            score += 10.0

        if cluster.request_count >= cluster.threshold:
            score += 10.0

        return min(score, 100.0)

    def _make_fair_reason(self, cluster: RequestCluster):
        reasons = []

        if cluster.main_category == CultureRequest.MainCategory.TRADITION:
            reasons.append("전통문화 요청이 포함되어 지속가능한 지역문화 자원으로 확장 가능합니다.")

        if cluster.target_age == CultureRequest.TargetAge.TEEN:
            reasons.append("청소년의 문화 접근성을 높이는 요청입니다.")

        if cluster.target_age == CultureRequest.TargetAge.SENIOR:
            reasons.append("고령층의 문화 접근성을 높이는 요청입니다.")

        if cluster.budget_range in [
            CultureRequest.BudgetRange.FREE,
            CultureRequest.BudgetRange.UNDER_10000,
        ]:
            reasons.append("낮은 비용으로 참여 가능한 문화 경험을 우선합니다.")

        if cluster.request_count >= cluster.threshold:
            reasons.append("요청 수가 기준을 넘어 실제 프로그램으로 제안 가능한 상태입니다.")

        if not reasons:
            reasons.append("지역 기반 문화 요청이 누적되고 있습니다.")

        return reasons

    def _make_cluster_title(self, culture_request: CultureRequest) -> str:
        return (
            f"{culture_request.region_label} "
            f"{culture_request.get_preferred_time_display()} "
            f"{culture_request.get_main_category_display()} 요청"
        )

    def _make_cluster_summary(self, culture_request: CultureRequest) -> str:
        return (
            f"{culture_request.region_label} 지역에서 "
            f"{culture_request.get_preferred_time_display()}에 참여 가능한 "
            f"{culture_request.get_main_category_display()} 문화 프로그램에 대한 요청입니다."
        )

    def _make_cluster_title_from_cluster(self, cluster: RequestCluster) -> str:
        preferred_time = self._choice_label(
            CultureRequest.PreferredTime.choices,
            cluster.preferred_time,
        )
        main_category = self._choice_label(
            CultureRequest.MainCategory.choices,
            cluster.main_category,
        )

        return f"{cluster.region_label} {preferred_time} {main_category} 요청"

    def _make_cluster_summary_from_cluster(self, cluster: RequestCluster) -> str:
        preferred_time = self._choice_label(
            CultureRequest.PreferredTime.choices,
            cluster.preferred_time,
        )
        main_category = self._choice_label(
            CultureRequest.MainCategory.choices,
            cluster.main_category,
        )

        return (
            f"{cluster.region_label} 지역에서 "
            f"{preferred_time}에 참여 가능한 "
            f"{main_category} 문화 프로그램에 대한 요청입니다."
        )

    def _choice_label(self, choices, value: str) -> str:
        for choice_value, choice_label in choices:
            if choice_value == value:
                return choice_label
        return value