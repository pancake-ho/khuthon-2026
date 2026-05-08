
from typing import Any, Dict, List
import config

def print_add_result(request_text: str, result: Dict[str, Any]) -> None:
    print('\n' + '-' * 100)
    print(f"요청: {request_text}")
    print('결과: 기존 군집에 추가됨' if result['action'] == 'assigned' else '결과: 새 군집 생성됨')
    print(f"군집 ID: {result['cluster_id']}")
    print(f"유사도: {result['similarity']}")
    print(f"요청 수: {result['request_count']}")
    print(f"상태: {result['status']}")
    print(f"대표 요청: {result['representative_text']}")
    print('-' * 100)

def print_cluster_summary(clusters: List[Dict[str, Any]]) -> None:
    print('\n' + '=' * 120)
    print('군집 요약')
    print('=' * 120)
    if not clusters:
        print('아직 군집이 없습니다.')
        return
    print(f"{'ID':>3} | {'상태':^10} | {'요청수':>5} | {'지역':^12} | {'시간':^12} | {'예산':^12} | 대표 요청")
    print('-' * 120)
    for cluster in sorted(clusters, key=lambda c: c['id']):
        print(f"{cluster['id']:>3} | {cluster['status']:^10} | {len(cluster['requests']):>5} | {cluster['region']:^12} | {cluster['time_slot']:^12} | {cluster['budget']:^12} | {cluster['representative_text']}")

def print_clusters(clusters: List[Dict[str, Any]], show_requests: bool = True) -> None:
    print('\n' + '=' * 120)
    print('현재 문화 요청 군집 상세')
    print('=' * 120)
    if not clusters:
        print('아직 군집이 없습니다.')
        return
    for cluster in sorted(clusters, key=lambda c: (c['region'], c['time_slot'], c['budget'], c['id'])):
        print(f"\n[군집 {cluster['id']}]")
        print(f"지역: {cluster['region']}")
        print(f"시간: {cluster['time_slot']}")
        print(f"예산: {cluster['budget']}")
        print(f"상태: {cluster['status']}")
        print(f"요청 수: {len(cluster['requests'])}")
        print(f"대표 요청: {cluster['representative_text']}")
        if show_requests:
            print('요청 목록:')
            for request in cluster['requests']:
                print(f"  - {request['request_text']}")

def print_ready_candidates(clusters: List[Dict[str, Any]]) -> None:
    ready_clusters = [cluster for cluster in clusters if cluster['status'] == 'ready']
    print('\n' + '=' * 120)
    print('프로그램 후보 목록')
    print('=' * 120)
    if not ready_clusters:
        print(f"아직 ready 상태의 군집이 없습니다. MIN_CLUSTER_SIZE={config.MIN_CLUSTER_SIZE}")
        return
    for cluster in sorted(ready_clusters, key=lambda c: len(c['requests']), reverse=True):
        print(f"\n[프로그램 후보 / 군집 {cluster['id']}]")
        print(f"지역: {cluster['region']}")
        print(f"시간: {cluster['time_slot']}")
        print(f"예산: {cluster['budget']}")
        print(f"요청 수: {len(cluster['requests'])}")
        print(f"대표 요청: {cluster['representative_text']}")
