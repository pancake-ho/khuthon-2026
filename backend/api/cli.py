
from typing import List, Optional
import config
from clustering_service import ClusteringService
from display import print_cluster_summary, print_clusters, print_ready_candidates
from models import AppState

def choose_from_options(title: str, options: List[str]) -> Optional[str]:
    print(f"\n{title}")
    print('-' * 60)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    print('q. 취소')
    while True:
        choice = input('번호 선택: ').strip()
        if choice.lower() == 'q':
            return None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                selected = options[choice_num - 1]
                print(f"선택됨: {selected}")
                return selected
        print('잘못된 입력입니다. 목록에 있는 번호를 입력하세요.')

def choose_region() -> Optional[str]:
    selected_group = choose_from_options('권역 선택', list(config.REGION_GROUPS.keys()))
    if selected_group is None:
        return None
    return choose_from_options(f'{selected_group} 세부 지역 선택', config.REGION_GROUPS[selected_group])

def input_new_request_interactively(clustering_service: ClusteringService) -> None:
    print('\n새 문화 요청을 입력합니다.')
    print('지역은 권역 → 세부 지역 순서로 선택합니다.')
    print('시간대와 예산은 고정 선택지에서 고르고, 요청사항만 자유롭게 작성합니다.')
    region = choose_region()
    if region is None:
        print('요청 추가를 취소했습니다.')
        return
    time_slot = choose_from_options('시간대 선택', config.TIME_SLOT_OPTIONS)
    if time_slot is None:
        print('요청 추가를 취소했습니다.')
        return
    budget = choose_from_options('예산 선택', config.BUDGET_OPTIONS)
    if budget is None:
        print('요청 추가를 취소했습니다.')
        return
    print('\n요청사항은 자유롭게 작성하세요.')
    print('예시: 아이유 같은 감성 보컬 공연 보고 싶어요')
    request_text = input('원하는 문화 요청 입력: ').strip()
    if not request_text:
        print('요청사항이 비어 있습니다. 요청 추가를 취소합니다.')
        return
    try:
        clustering_service.add_request(region=region, time_slot=time_slot, budget=budget, request_text=request_text, source='manual', verbose=True)
    except Exception as e:
        print(f"[오류] 요청 추가 실패: {e}")

def run_cli(state: AppState, clustering_service: ClusteringService) -> None:
    while True:
        print('\n' + '=' * 120)
        print('문화콜 AI 군집화 시연 메뉴')
        print('=' * 120)
        print('1. 군집 요약 보기')
        print('2. 군집 상세 보기')
        print('3. 프로그램 후보 보기')
        print('4. 새 요청 직접 추가')
        print('5. 종료')
        choice = input('번호 선택: ').strip()
        if choice == '1':
            print_cluster_summary(state.clusters)
        elif choice == '2':
            print_clusters(state.clusters, show_requests=True)
        elif choice == '3':
            print_ready_candidates(state.clusters)
        elif choice == '4':
            input_new_request_interactively(clustering_service)
        elif choice == '5':
            print('종료합니다.')
            break
        else:
            print('잘못된 입력입니다. 1~5 중에서 선택하세요.')
