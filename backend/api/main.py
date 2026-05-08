
import config
from cli import run_cli
from clustering_service import ClusteringService
from csv_loader import load_requests_from_csv
from display import print_cluster_summary, print_ready_candidates
from embedding_service import EmbeddingService
from models import AppState

def print_startup_info() -> None:
    print('=' * 120)
    print('문화콜 AI 군집화 시연용 main.py')
    print('=' * 120)
    print(f"사용 모델: {config.EMBED_MODEL}")
    print(f"SIM_THRESHOLD: {config.SIM_THRESHOLD}")
    print(f"MIN_CLUSTER_SIZE: {config.MIN_CLUSTER_SIZE}")
    print(f"초기 CSV 경로: {config.DEMO_CSV_PATH}")
    print(f"임베딩 캐시 파일: {config.CACHE_FILE}")
    print('\n[입력 구조]')
    print('- 지역: 권역 선택 후 세부 시/군/구 선택')
    print('- 시간대: 고정 선택지')
    print('- 예산: 고정 선택지')
    print('- 요청사항: 자유 입력')
    print('- 임베딩 대상: 요청사항 텍스트만')
    print('- 군집 비교 조건: 지역/시간대/예산이 같은 군집만 비교')

def main() -> None:
    print_startup_info()
    state = AppState()
    embedding_service = EmbeddingService(state)
    embedding_service.load_cache()
    clustering_service = ClusteringService(state=state, embedding_service=embedding_service)
    load_requests_from_csv(config.DEMO_CSV_PATH, clustering_service)
    print_cluster_summary(state.clusters)
    print_ready_candidates(state.clusters)
    run_cli(state, clustering_service)

if __name__ == '__main__':
    main()
