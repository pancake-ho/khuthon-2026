import os
import json
from itertools import combinations
from typing import List, Dict, Any

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


# =========================
# 1. 환경설정
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY가 없습니다. .env 파일을 확인하세요.")

client = OpenAI(api_key=OPENAI_API_KEY)

CACHE_FILE = "embedding_cache.json"


# =========================
# 2. 테스트 데이터
# label은 정답 군집 이름이라고 생각하면 됨
# =========================
sample_requests = [
    # 1) 감성보컬 / 영월군 / 토요일 오후 / 10만원 이내
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "아이유 같은 감성 보컬 공연 보고 싶어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "조용한 발라드 라이브 공연이 있었으면 좋겠어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "어쿠스틱 보컬 공연 열어주세요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "감성적인 노래를 들을 수 있는 작은 공연이 있으면 좋겠어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "잔잔한 분위기의 싱어송라이터 공연을 보고 싶어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "주말에 듣기 좋은 발라드 공연이 있었으면 좋겠어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "감미로운 보컬 중심의 라이브 공연을 보고 싶어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "소규모 감성 음악 공연이 영월에서 열리면 좋겠어요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "편하게 앉아서 들을 수 있는 발라드 공연을 원해요",
        "label": "감성보컬_영월군_토요일오후_10만원이내",
    },

    # 2) KPOP댄스 / 영월군 / 토요일 오후 / 10만원 이내
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "청소년 K-pop 커버댄스 공연 보고 싶어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "아이돌 댄스팀 무대가 있었으면 좋겠어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "걸그룹 커버댄스 공연을 보고 싶어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "학생들이 참여하는 K-pop 댄스 무대가 열렸으면 좋겠어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "유명 아이돌 노래로 하는 커버 공연이 있었으면 좋겠어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "K-pop 안무를 즐길 수 있는 젊은 분위기 공연을 원해요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "댄스 동아리들이 나오는 K-pop 무대를 보고 싶어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "아이돌 커버 퍼포먼스 공연이 열렸으면 좋겠어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "토요일 오후",
        "budget": "10만원 이내",
        "text": "주말에 신나는 K-pop 댄스 공연을 보고 싶어요",
        "label": "KPOP댄스_영월군_토요일오후_10만원이내",
    },

    # 3) 전통체험 / 영월군 / 일요일 오후 / 5만원 이내
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "아이들과 한지 공예 체험 프로그램이 있었으면 좋겠어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "전통 매듭 만들기 수업을 듣고 싶어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "한복 입고 사진 찍는 전통문화 체험을 하고 싶어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "지역 어르신과 함께하는 전통 공예 체험이 있었으면 좋겠어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "한지나 부채를 직접 만드는 체험 수업이 열리면 좋겠어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "가족이 함께 참여할 수 있는 전통문화 체험을 원해요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "전통 소품 만들기나 공예 체험이 있었으면 좋겠어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "아이들이 재미있게 참여할 수 있는 전통 놀이 체험을 원해요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "일요일 오후",
        "budget": "5만원 이내",
        "text": "주말에 할 수 있는 전통 공예 클래스가 열리면 좋겠어요",
        "label": "전통체험_영월군_일요일오후_5만원이내",
    },

    # 4) 미술전시 / 영월군 / 평일 저녁 / 3만원 이내
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "작은 그림 전시회 보고 싶어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "지역 작가 미술 전시가 열렸으면 좋겠어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "사진 전시회가 있었으면 좋겠어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "청년 작가 작품 전시를 보고 싶어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "퇴근 후 가볍게 들를 수 있는 소규모 전시가 있으면 좋겠어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "드로잉이나 일러스트 작품을 볼 수 있는 전시를 원해요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "지역 예술가들의 그림과 사진을 볼 수 있는 전시가 필요해요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "조용히 관람할 수 있는 미술 전시 프로그램이 있으면 좋겠어요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },
    {
        "region": "영월군",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "사진 작품이나 회화를 함께 볼 수 있는 전시를 원해요",
        "label": "미술전시_영월군_평일저녁_3만원이내",
    },

    # 5) 가족뮤지컬 / 춘천시 / 토요일 오전 / 10만원 이내
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "아이와 함께 볼 수 있는 가족 뮤지컬이 있었으면 좋겠어요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "어린이도 재미있게 볼 수 있는 공연을 원해요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "가족끼리 즐길 수 있는 뮤지컬 공연이 열리면 좋겠어요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "주말 오전에 아이들 대상 공연이 있으면 좋겠어요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "동화 내용을 바탕으로 한 어린이 뮤지컬을 보고 싶어요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "부모와 아이가 같이 보기 좋은 공연 프로그램을 원해요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "어린 자녀가 있는 가족을 위한 문화 공연이 필요해요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "노래와 이야기가 있는 가족 공연이 열렸으면 좋겠어요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "토요일 오전",
        "budget": "10만원 이내",
        "text": "아이들이 집중해서 볼 수 있는 뮤지컬 형식 공연을 원해요",
        "label": "가족뮤지컬_춘천시_토요일오전_10만원이내",
    },

    # 6) 트로트공연 / 춘천시 / 평일 오후 / 5만원 이내
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "어르신들이 즐길 수 있는 트로트 공연이 있었으면 좋겠어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "중장년층이 좋아할 만한 가수 공연을 보고 싶어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "흥겨운 트로트 무대가 지역에서 열리면 좋겠어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "평일 낮에 볼 수 있는 트로트 공연이 필요해요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "어르신 복지관과 연계할 수 있는 트로트 무대를 원해요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "친숙한 노래를 함께 즐길 수 있는 공연이 있었으면 좋겠어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "지역 주민이 함께 따라 부를 수 있는 트로트 음악회를 원해요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "중년층과 어르신 대상의 가요 공연이 열렸으면 좋겠어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },
    {
        "region": "춘천시",
        "time_slot": "평일 오후",
        "budget": "5만원 이내",
        "text": "신나는 트로트 콘서트를 가까운 곳에서 보고 싶어요",
        "label": "트로트공연_춘천시_평일오후_5만원이내",
    },

    # 7) 독립영화 / 원주시 / 평일 저녁 / 3만원 이내
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "독립영화 상영회가 있었으면 좋겠어요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "상업영화 말고 독립영화를 볼 수 있는 자리가 필요해요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "작은 영화관이나 공간에서 예술영화 상영이 있었으면 좋겠어요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "평일 저녁에 독립영화 관람 프로그램을 원해요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "감독과의 대화가 함께 있는 독립영화 상영이 열리면 좋겠어요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "다양한 주제의 인디 영화 상영회를 보고 싶어요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "예술영화나 단편영화를 접할 수 있는 상영 행사가 필요해요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "원주에서 독립영화를 함께 볼 수 있는 문화 프로그램을 원해요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "평일 저녁",
        "budget": "3만원 이내",
        "text": "대형 멀티플렉스에서 보기 어려운 영화를 상영해주면 좋겠어요",
        "label": "독립영화_원주시_평일저녁_3만원이내",
    },

    # 8) 북토크 / 원주시 / 일요일 오후 / 3만원 이내
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "작가와 직접 이야기할 수 있는 북토크가 있었으면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "책을 좋아하는 사람들이 모일 수 있는 북토크 행사를 원해요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "지역 서점에서 작가 강연 같은 프로그램이 열리면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "독서 모임과 연결된 북토크 행사가 있었으면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "소설가나 에세이 작가를 초청하는 북토크를 보고 싶어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "책과 관련된 문화 행사가 주말에 열렸으면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "원주에서 작가 강연이나 독서 대화 프로그램이 있으면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "책 이야기와 질문을 나눌 수 있는 북토크 모임을 원해요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },
    {
        "region": "원주시",
        "time_slot": "일요일 오후",
        "budget": "3만원 이내",
        "text": "독립서점 분위기에서 진행하는 작은 북토크가 열리면 좋겠어요",
        "label": "북토크_원주시_일요일오후_3만원이내",
    },

    # 9) 지역축제 / 강릉시 / 토요일 오후 / 무료
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "지역 특색이 살아 있는 축제가 있었으면 좋겠어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "플리마켓이랑 공연이 같이 있는 소규모 축제를 원해요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "주민들이 같이 참여할 수 있는 동네 축제가 열리면 좋겠어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "지역 먹거리와 공연을 함께 즐길 수 있는 마을 축제를 보고 싶어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "강릉만의 분위기를 살린 문화 축제가 있으면 좋겠어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "버스킹과 체험 부스가 함께 있는 야외 축제를 원해요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "가볍게 놀러 갈 수 있는 주말 지역 행사나 축제가 있었으면 좋겠어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "시장이나 공원에서 열리는 작은 문화 축제를 보고 싶어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },
    {
        "region": "강릉시",
        "time_slot": "토요일 오후",
        "budget": "무료",
        "text": "지역 주민이 직접 참여하는 커뮤니티형 축제가 있으면 좋겠어요",
        "label": "지역축제_강릉시_토요일오후_무료",
    },

    # 10) 클래식공연 / 강릉시 / 평일 저녁 / 10만원 이내
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "소규모 클래식 공연이 있었으면 좋겠어요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "현악 사중주나 피아노 연주회를 보고 싶어요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "퇴근 후 들을 수 있는 클래식 음악회가 열리면 좋겠어요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "조용한 분위기에서 감상할 수 있는 클래식 공연을 원해요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "바이올린이나 첼로 연주를 가까이서 들을 수 있는 무대가 필요해요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "실내악 공연 같은 클래식 프로그램이 있었으면 좋겠어요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "정통 클래식 음악을 부담 없이 접할 수 있는 공연을 원해요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "피아노 독주회나 현악 연주회를 지역에서 보고 싶어요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },
    {
        "region": "강릉시",
        "time_slot": "평일 저녁",
        "budget": "10만원 이내",
        "text": "차분한 음악 감상을 할 수 있는 클래식 공연이 필요해요",
        "label": "클래식공연_강릉시_평일저녁_10만원이내",
    },

    # 11) 재즈공연 / 속초시 / 금요일 저녁 / 10만원 이내
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "재즈 밴드 공연이 있었으면 좋겠어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "분위기 좋은 라이브 재즈 공연을 보고 싶어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "색소폰과 피아노가 있는 재즈 무대가 열리면 좋겠어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "주말 시작할 때 들을 수 있는 재즈 공연이 있으면 좋겠어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "작은 바나 문화공간에서 재즈 라이브를 즐기고 싶어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "보컬 재즈나 스탠더드 재즈를 들을 수 있는 공연을 원해요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "금요일 밤에 분위기 있게 즐길 수 있는 재즈 음악회를 원해요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "즉흥 연주 느낌의 라이브 재즈 무대를 보고 싶어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "금요일 저녁",
        "budget": "10만원 이내",
        "text": "속초에서 들을 수 있는 소규모 재즈 공연이 있으면 좋겠어요",
        "label": "재즈공연_속초시_금요일저녁_10만원이내",
    },

    # 12) 공예체험 / 속초시 / 토요일 오전 / 5만원 이내
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "도자기나 머그컵을 만드는 공예 체험을 하고 싶어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "주말 오전에 참여할 수 있는 핸드메이드 체험이 있으면 좋겠어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "향초 만들기나 비누 만들기 같은 체험 수업을 원해요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "손으로 직접 만드는 공예 클래스가 열렸으면 좋겠어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "친구나 가족과 함께 참여할 수 있는 공방 체험을 하고 싶어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "초보자도 쉽게 할 수 있는 만들기 체험 프로그램이 있었으면 좋겠어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "도예나 소품 제작 같은 체험형 문화 프로그램을 원해요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "직접 만든 결과물을 가져갈 수 있는 공예 수업이 있으면 좋겠어요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
    {
        "region": "속초시",
        "time_slot": "토요일 오전",
        "budget": "5만원 이내",
        "text": "속초에서 주말에 할 수 있는 체험형 공예 클래스가 필요해요",
        "label": "공예체험_속초시_토요일오전_5만원이내",
    },
]


# =========================
# 3. 캐시 로드/저장
# OpenAI API를 매번 다시 호출하지 않기 위한 장치
# =========================
def load_cache() -> Dict[str, List[float]]:
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache: Dict[str, List[float]]) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


embedding_cache = load_cache()


# =========================
# 4. 임베딩 함수
# =========================
def get_embedding(text: str) -> List[float]:
    text = text.replace("\n", " ").strip()

    if text in embedding_cache:
        return embedding_cache[text]

    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text,
    )

    embedding = response.data[0].embedding
    embedding_cache[text] = embedding
    save_cache(embedding_cache)

    return embedding


# =========================
# 5. cosine similarity
# =========================
def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


# =========================
# 6. threshold 하나에 대해 군집화 수행
# =========================
def cluster_requests(data: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    clusters = []

    for item in data:
        embedding = item["embedding"]

        candidate_clusters = [
            cluster
            for cluster in clusters
            if cluster["region"] == item["region"]
            and cluster["time_slot"] == item["time_slot"]
            and cluster["budget"] == item["budget"]
        ]

        best_cluster = None
        best_score = -1.0

        for cluster in candidate_clusters:
            score = cosine_similarity(embedding, cluster["centroid"])

            if score > best_score:
                best_score = score
                best_cluster = cluster

        if best_cluster is not None and best_score >= threshold:
            best_cluster["items"].append(item)

            embeddings = [x["embedding"] for x in best_cluster["items"]]
            best_cluster["centroid"] = np.mean(embeddings, axis=0).tolist()

        else:
            new_cluster = {
                "id": len(clusters) + 1,
                "region": item["region"],
                "time_slot": item["time_slot"],
                "budget": item["budget"],
                "centroid": embedding,
                "items": [item],
            }

            clusters.append(new_cluster)

    return clusters


# =========================
# 7. 성능 평가
# Pairwise Precision / Recall / F1 계산
# =========================
def evaluate_clusters(data: List[Dict[str, Any]], clusters: List[Dict[str, Any]]) -> Dict[str, float]:
    # 각 요청이 어떤 cluster에 들어갔는지 기록
    predicted_cluster = {}

    for cluster in clusters:
        for item in cluster["items"]:
            predicted_cluster[item["id"]] = cluster["id"]

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for a, b in combinations(data, 2):
        true_same = a["label"] == b["label"]
        pred_same = predicted_cluster[a["id"]] == predicted_cluster[b["id"]]

        if pred_same and true_same:
            true_positive += 1
        elif pred_same and not true_same:
            false_positive += 1
        elif not pred_same and true_same:
            false_negative += 1

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive > 0 else 0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


# =========================
# 8. 추가 진단: 섞인 군집 / 쪼개진 라벨 확인
# =========================
def analyze_clusters(clusters: List[Dict[str, Any]]) -> Dict[str, int]:
    mixed_cluster_count = 0

    for cluster in clusters:
        labels = set(item["label"] for item in cluster["items"])

        if len(labels) >= 2:
            mixed_cluster_count += 1

    label_to_clusters = {}

    for cluster in clusters:
        for item in cluster["items"]:
            label = item["label"]

            if label not in label_to_clusters:
                label_to_clusters[label] = set()

            label_to_clusters[label].add(cluster["id"])

    split_label_count = sum(
        1 for cluster_ids in label_to_clusters.values()
        if len(cluster_ids) >= 2
    )

    return {
        "mixed_cluster_count": mixed_cluster_count,
        "split_label_count": split_label_count,
    }


# =========================
# 9. 스윕 실행
# =========================
def run_sweep() -> None:
    print(f"사용 모델: {EMBED_MODEL}")
    print("임베딩 생성 중... 처음 실행할 때는 시간이 조금 걸릴 수 있습니다.\n")

    # id 부여 + embedding 생성
    data = []

    for idx, item in enumerate(sample_requests):
        copied = item.copy()
        copied["id"] = idx
        copied["embedding"] = get_embedding(copied["text"])
        data.append(copied)

    thresholds = [
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.88,
    ]

    print("=" * 90)
    print("Threshold Sweep 결과")
    print("=" * 90)
    print(
        f"{'threshold':>10} | {'clusters':>8} | {'mixed':>5} | {'split':>5} | "
        f"{'precision':>9} | {'recall':>7} | {'f1':>7}"
    )
    print("-" * 90)

    results = []

    for threshold in thresholds:
        clusters = cluster_requests(data, threshold)
        metrics = evaluate_clusters(data, clusters)
        diagnosis = analyze_clusters(clusters)

        result = {
            "threshold": threshold,
            "cluster_count": len(clusters),
            **diagnosis,
            **metrics,
        }

        results.append(result)

        print(
            f"{threshold:>10.2f} | "
            f"{len(clusters):>8} | "
            f"{diagnosis['mixed_cluster_count']:>5} | "
            f"{diagnosis['split_label_count']:>5} | "
            f"{metrics['precision']:>9.3f} | "
            f"{metrics['recall']:>7.3f} | "
            f"{metrics['f1']:>7.3f}"
        )

    print("-" * 90)

    best = max(results, key=lambda x: x["f1"])

    print("\n추천 threshold")
    print(f"F1 기준 추천값: {best['threshold']}")
    print(
        f"precision={best['precision']:.3f}, "
        f"recall={best['recall']:.3f}, "
        f"f1={best['f1']:.3f}"
    )

    print("\n해석 팁")
    print("- mixed가 크면 서로 다른 요청이 한 군집에 섞인 것입니다.")
    print("- split이 크면 같은 종류의 요청이 여러 군집으로 쪼개진 것입니다.")
    print("- 문화콜은 잘못 섞이는 것보다 조금 쪼개지는 편이 더 안전합니다.")


if __name__ == "__main__":
    run_sweep()