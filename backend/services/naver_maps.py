"""
네이버 지도 API와 통신하는 로직을 담당하는 파일
Django view나 model 안에 외부 API 호출 기능을 직접 넣지 않고,
services 폴더로 분리하여 관리
"""

from typing import Optional, Dict, Any

import requests
from django.conf import settings

NAVER_GEOCODE_URL = "https://maps.apigw.ntruss.com/map-geocode/v2/geocode"


class NaverMapAPIError(Exception):
    """
    네이버 지도 API 호출 중 발생하는 예외를 대비하는 클래스
    """


def geocode_addr(addr: str) -> Optional[Dict[str, Any]]:
    """
    주소를 위도 및 경도로 변경하는 함수
    """
    if not addr or not addr.strip():
        return None
    
    client_id = settings.NAVER_MAP_CLIENT_ID
    client_secret = settings.NAVER_MAP_CLIENT_SECRET

    if not client_id or not client_secret:
        raise NaverMapAPIError(
            "NAVER_MAP_CLIENT_ID 또는 NAVER_MAP_CLIENT_SECRET 변수가 설정되지 않았습니다."
        )
    
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }

    params = {
        "query": addr.strip(),
    }

    try:
        response = requests.get(
            NAVER_GEOCODE_URL,
            headers=headers,
            params=params,
            timeout=5,
        )
        response.raise_for_status()

    except requests.RequestException as e:
        raise NaverMapAPIError(f"네이버 지도 API 요청 실패, 원인은 다음과 같습니다: {e}") from e
    
    data = response.json()
    addresses = data.get("addresses", [])
    if not addresses:
        return None
    
    first = addresses[0]

    longitude = first.get("x")
    latitude = first.get("y")

    if longitude is None or latitude is None:
        return None
    
    return {
        "address": addr.strip(),
        "road_address": first.get("roadAddress", ""),
        "jibun_address": first.get("jibunAddress", ""),
        "latitude": float(latitude),
        "longitude": float(longitude),
        "raw": first,
    }