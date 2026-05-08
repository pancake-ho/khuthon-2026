"""
DB 없이 바로 테스트 가능하도록 구현된 코드
"""


import os
from typing import Dict, List, Any

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


# =========================
# 1. 환경설정 읽기
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
SIM_THRESHOLD = float(os.getenv("SIM_THRESHOLD", "0.82"))
MIN_CLUSTER_SIZE = int(os.getenv("MIN_CLUSTER_SIZE", "3"))

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY가 없습니다. .env 파일을 만들고 OPENAI_API_KEY=너의_API키 를 넣어주세요."
    )

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# 2. 임시 저장소
#    실제 서비스에서는 나중에 DB로 교체
# =========================
clusters: List[Dict[str, Any]] = []


# =========================
# 3. OpenAI 임베딩 생성 함수
# =========================
def get_embedding(text: str) -> List[float]:
    """
    사용자의 자유 요청 문장을 OpenAI embedding vector로 변환한다.
    """
    cleaned_text = text.replace("\n", " ").strip()

    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=cleaned_text,
    )

    return response.data[0].embedding


# =========================
# 4. 코사인 유사도 계산 함수
# =========================
def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    두 embedding vector가 얼마나 비슷한지 계산한다.
    1에 가까울수록 의미가 비슷하다.
    """
    vec_a = np.array(a)
    vec_b = np.array(b)

    denominator = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)

    if denominator == 0:
        return 0.0

    return float(np.dot(vec_a, vec_b) / denominator)


# =========================
# 5. 대표 요청문 갱신 함수
# =========================
def update_representative_text(cluster: Dict[str, Any]) -> None:
    """
    군집 centroid와 가장 가까운 요청을 대표 문장으로 선택한다.
    """
    centroid = cluster["centroid"]

    best_request = None
    best_score = -1.0

    for request in cluster["requests"]:
        score = cosine_similarity(request["embedding"], centroid)

        if score > best_score:
            best_score = score
            best_request = request

    if best_request is not None:
        cluster["representative_text"] = best_request["request_text"]


# =========================
# 6. 새 요청을 기존 군집에 넣거나 새 군집 생성
# =========================
def add_request(region: str, time_slot: str, budget: str, request_text: str) -> Dict[str, Any]:
    """
    사용자 요청을 받아서 다음 중 하나를 수행한다.

    1. 같은 지역/시간/예산 조건의 기존 군집 중 가장 유사한 군집 찾기
    2. 유사도가 threshold 이상이면 기존 군집에 추가
    3. threshold 미만이면 새 군집 생성
    """
    embedding = get_embedding(request_text)

    new_request = {
        "region": region,
        "time_slot": time_slot,
        "budget": budget,
        "request_text": request_text,
        "embedding": embedding,
    }

    # 위치/시간/예산이 같은 군집만 비교한다.
    candidate_clusters = [
        cluster
        for cluster in clusters
        if cluster["region"] == region
        and cluster["time_slot"] == time_slot
        and cluster["budget"] == budget
    ]

    best_cluster = None
    best_score = -1.0

    for cluster in candidate_clusters:
        score = cosine_similarity(embedding, cluster["centroid"])

        if score > best_score:
            best_score = score
            best_cluster = cluster

    # 기존 군집에 추가
    if best_cluster is not None and best_score >= SIM_THRESHOLD:
        best_cluster["requests"].append(new_request)

        embeddings = [request["embedding"] for request in best_cluster["requests"]]
        best_cluster["centroid"] = np.mean(embeddings, axis=0).tolist()

        update_representative_text(best_cluster)

        if len(best_cluster["requests"]) >= MIN_CLUSTER_SIZE:
            best_cluster["status"] = "ready"

        return {
            "action": "assigned",
            "cluster_id": best_cluster["id"],
            "similarity": round(best_score, 4),
            "status": best_cluster["status"],
            "representative_text": best_cluster["representative_text"],
            "request_count": len(best_cluster["requests"]),
        }

    # 새 군집 생성
    new_cluster = {
        "id": len(clusters) + 1,
        "region": region,
        "time_slot": time_slot,
        "budget": budget,
        "centroid": embedding,
        "requests": [new_request],
        "representative_text": request_text,
        "status": "collecting",
    }

    clusters.append(new_cluster)

    return {
        "action": "created",
        "cluster_id": new_cluster["id"],
        "similarity": None if best_score < 0 else round(best_score, 4),
        "status": new_cluster["status"],
        "representative_text": new_cluster["representative_text"],
        "request_count": len(new_cluster["requests"]),
    }


# =========================
# 7. 현재 군집 출력 함수
# =========================
def print_clusters() -> None:
    print("\n" + "=" * 60)
    print("현재 문화 요청 군집 목록")
    print("=" * 60)

    if not clusters:
        print("아직 군집이 없습니다.")
        return

    for cluster in clusters:
        print(f"\n[군집 {cluster['id']}]")
        print(f"지역: {cluster['region']}")
        print(f"시간: {cluster['time_slot']}")
        print(f"예산: {cluster['budget']}")
        print(f"상태: {cluster['status']}")
        print(f"요청 수: {len(cluster['requests'])}")
        print(f"대표 요청: {cluster['representative_text']}")
        print("요청 목록:")

        for request in cluster["requests"]:
            print(f"  - {request['request_text']}")


# =========================
# 8. 테스트 실행
# =========================
def run_demo() -> None:
    """
    VS Code에서 python main.py로 실행하면 아래 샘플 요청들이 자동으로 군집화된다.
    """
    sample_requests = [
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "아이유 같은 감성 보컬 공연 보고 싶어요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "조용한 발라드 라이브 공연이 있었으면 좋겠어요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "어쿠스틱 보컬 공연 열어주세요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "청소년 K-pop 커버댄스 공연 보고 싶어요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "아이돌 댄스팀 무대가 있었으면 좋겠어요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "아이들과 한지 공예 체험 프로그램이 있었으면 좋겠어요",
        },
        {
            "region": "영월군",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "전통 매듭 만들기 수업을 듣고 싶어요",
        },
        {
            "region": "춘천시",
            "time_slot": "토요일 오후",
            "budget": "10만원 이내",
            "request_text": "아이유 같은 감성 보컬 공연 보고 싶어요",
        },
    ]

    print(f"사용 모델: {EMBED_MODEL}")
    print(f"유사도 기준값 SIM_THRESHOLD: {SIM_THRESHOLD}")
    print(f"프로그램 후보 기준 MIN_CLUSTER_SIZE: {MIN_CLUSTER_SIZE}")

    for item in sample_requests:
        result = add_request(
            region=item["region"],
            time_slot=item["time_slot"],
            budget=item["budget"],
            request_text=item["request_text"],
        )

        print("\n요청:", item["request_text"])
        print("결과:", result)

    print_clusters()


if __name__ == "__main__":
    run_demo()