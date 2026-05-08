
import csv
import os
from clustering_service import ClusteringService

def load_requests_from_csv(file_path: str, clustering_service: ClusteringService) -> int:
    if not os.path.exists(file_path):
        print(f"[안내] {file_path} 파일이 없습니다. 초기 데이터 없이 시작합니다.")
        return 0
    loaded_count = 0
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        required_columns = {'region', 'time_slot', 'budget', 'request_text'}
        current_columns = set(reader.fieldnames or [])
        missing = required_columns - current_columns
        if missing:
            raise ValueError(f"CSV 파일에 필요한 컬럼이 없습니다: {missing}\n필수 컬럼: region,time_slot,budget,request_text")
        for row in reader:
            region = row['region'].strip()
            time_slot = row['time_slot'].strip()
            budget = row['budget'].strip()
            request_text = row['request_text'].strip()
            if not request_text:
                continue
            clustering_service.add_request(region=region, time_slot=time_slot, budget=budget, request_text=request_text, source='csv', verbose=False)
            loaded_count += 1
    print(f"[완료] CSV 초기 요청 {loaded_count}개를 불러와 군집화했습니다.")
    return loaded_count
