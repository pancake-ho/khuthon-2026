
from typing import Any, Dict, Optional
import numpy as np
import config
from display import print_add_result
from embedding_service import EmbeddingService
from models import AppState
from similarity import cosine_similarity

class ClusteringService:
    """요청 추가, 기존 군집 배정, 새 군집 생성, centroid 갱신을 담당한다."""
    def __init__(self, state: AppState, embedding_service: EmbeddingService):
        self.state = state
        self.embedding_service = embedding_service

    def update_representative_text(self, cluster: Dict[str, Any]) -> None:
        centroid = cluster['centroid']
        best_request = None
        best_score = -1.0
        for request in cluster['requests']:
            score = cosine_similarity(request['embedding'], centroid)
            if score > best_score:
                best_score = score
                best_request = request
        if best_request is not None:
            cluster['representative_text'] = best_request['request_text']

    def update_cluster_status(self, cluster: Dict[str, Any]) -> None:
        cluster['status'] = 'ready' if len(cluster['requests']) >= config.MIN_CLUSTER_SIZE else 'collecting'

    def add_request(self, region: str, time_slot: str, budget: str, request_text: str, source: str = 'manual', verbose: bool = True) -> Dict[str, Any]:
        region = region.strip()
        time_slot = time_slot.strip()
        budget = budget.strip()
        request_text = request_text.strip()
        request_text = request_text.encode("utf-8", errors="ignore").decode("utf-8")
        if not region or not time_slot or not budget or not request_text:
            raise ValueError('region, time_slot, budget, request_text는 모두 필요합니다.')

        embedding = self.embedding_service.get_embedding(request_text)
        new_request = {'region': region, 'time_slot': time_slot, 'budget': budget, 'request_text': request_text, 'embedding': embedding, 'source': source}
        candidate_clusters = [cluster for cluster in self.state.clusters if cluster['region'] == region and cluster['time_slot'] == time_slot and cluster['budget'] == budget]
        best_cluster: Optional[Dict[str, Any]] = None
        best_score = -1.0
        for cluster in candidate_clusters:
            score = cosine_similarity(embedding, cluster['centroid'])
            if score > best_score:
                best_score = score
                best_cluster = cluster

        if best_cluster is not None and best_score >= config.SIM_THRESHOLD:
            best_cluster['requests'].append(new_request)
            embeddings = [request['embedding'] for request in best_cluster['requests']]
            best_cluster['centroid'] = np.mean(embeddings, axis=0).tolist()
            self.update_representative_text(best_cluster)
            self.update_cluster_status(best_cluster)
            result = {'action': 'assigned', 'cluster_id': best_cluster['id'], 'similarity': round(best_score, 4), 'status': best_cluster['status'], 'request_count': len(best_cluster['requests']), 'representative_text': best_cluster['representative_text']}
            if verbose:
                print_add_result(request_text, result)
            return result

        new_cluster = {'id': len(self.state.clusters) + 1, 'region': region, 'time_slot': time_slot, 'budget': budget, 'centroid': embedding, 'requests': [new_request], 'representative_text': request_text, 'status': 'collecting'}
        self.state.clusters.append(new_cluster)
        result = {'action': 'created', 'cluster_id': new_cluster['id'], 'similarity': None if best_score < 0 else round(best_score, 4), 'status': new_cluster['status'], 'request_count': len(new_cluster['requests']), 'representative_text': new_cluster['representative_text']}
        if verbose:
            print_add_result(request_text, result)
        return result
