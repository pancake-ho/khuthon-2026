# Callture 문화콜

<p align="center">
  <img src="assets/culturecall-banner.svg" alt="Callture 문화콜 배너" width="100%" />
</p>

<p align="center">
  <b>요청이 모이면, 문화가 열립니다.</b><br/>
  사용자의 문화 요청을 모아 지역 창작자와 공공공간을 연결하는 수요 기반 문화 중개 서비스
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=flat-square&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/Backend-Django%20REST-092E20?style=flat-square&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Embedding%20Clustering-FF7A7A?style=flat-square" />
</p>

---

## 1. 프로젝트 한 줄 소개

**문화콜(Callture)**은 이미 만들어진 문화행사를 보여주는 서비스가 아니라, 사용자가 직접 남긴 문화 요청을 모아 실제 지역 문화 프로그램으로 연결하는 플랫폼입니다.

사용자는 “우리 동네에서 이런 문화 활동을 하고 싶다”는 요청을 남기고, 비슷한 요청이 일정 수 이상 모이면 하나의 문화콜로 묶입니다. 이후 관리자 또는 지역 창작자가 해당 문화콜을 확인하고, 공공공간·지역 공간·소규모 창작자와 연결해 실제 프로그램 생성 가능성을 확인합니다.

> 문화는 많지만, 원하는 문화는 찾기 어렵다.  
> 문화의 부족이 아니라 **연결의 부족**을 해결한다.

---

## 2. 문제 정의

### 2.1 문화 접근의 불균형

공연, 전시, 체험, 지역 축제는 존재하지만 모든 사람이 실제로 접근할 수 있는 것은 아닙니다.

- 지역에 따라 문화 정보와 문화시설 접근성이 다름
- 이동 거리, 시간, 비용 때문에 참여가 어려움
- 청소년, 고령층, 문화 초심자는 적합한 프로그램을 찾기 어려움
- 사용자는 원하는 문화가 있어도 어디에 요청해야 하는지 모름

문화콜은 사용자가 직접 문화 수요를 표현하게 하여, 공급자 중심의 문화 제공 구조를 **수요자 중심의 문화 연결 구조**로 전환합니다.

### 2.2 문화 산업의 구조적 양극화

대형 공연, 유명 전시, 인기 콘텐츠는 반복적으로 노출되지만 지역 창작자, 신진 예술가, 전통문화 활동가, 소규모 문화 프로그램은 관객과 만날 기회가 부족합니다.

문화콜은 인기순·조회수순 추천이 아니라, 실제 지역 수요와 조건이 맞는 요청을 기준으로 프로그램 생성 가능성을 판단합니다.

### 2.3 전통문화의 지속가능성 문제

전통문화는 보존의 대상으로는 남아 있지만, 현대인의 일상 속에서 반복적으로 선택되기 어렵습니다. 문화콜은 전통문화를 단순 전시나 일회성 체험으로 다루지 않고, 사용자의 요청·지역 창작자·공간 매칭과 연결하여 현재의 문화 경험으로 재생산될 수 있도록 설계합니다.

---

## 3. 핵심 아이디어

문화콜의 핵심은 **개인의 문화 요청을 집단 수요 데이터로 전환하는 것**입니다.

```text
사용자 요청 작성
        ↓
요청 데이터 저장 및 검증
        ↓
AI/유사도 기반 요청 군집화
        ↓
요청 수 누적 및 상태 관리
        ↓
기준 인원 충족 시 READY 상태 전환
        ↓
관리자/창작자/공간 매칭
        ↓
작은 지역 문화 프로그램 생성
```

기존 문화 서비스가 “이미 있는 행사를 찾아가는 구조”라면, 문화콜은 “필요한 문화가 모이면 새로 열리는 구조”입니다.

---

## 4. 서비스 시나리오

### 예시: 문화 접근성이 낮은 지역의 전통문화 요청

1. 사용자가 “우리 동네에서 아이와 함께 갈 수 있는 전통 공예 체험이 있었으면 좋겠어요”라는 요청을 작성합니다.
2. 다른 사용자들도 비슷한 지역·시간대·예산 조건의 요청을 남깁니다.
3. 백엔드는 요청을 저장하고 AI 군집화 로직을 통해 유사 요청을 같은 문화콜로 묶습니다.
4. 요청이 기준 인원 이상 모이면 상태가 `COLLECTING`에서 `READY`로 바뀝니다.
5. 관리자는 지도와 대시보드에서 준비된 요청을 확인합니다.
6. 지역 창작자 또는 공공공간과 연결해 실제 체험 프로그램으로 확장합니다.

---

## 5. 주요 기능

### 사용자 모드

| 기능 | 설명 |
| --- | --- |
| 문화 요청 작성 | 지역, 분야, 시간대, 예산, 요청 내용을 입력 |
| 요청 목록 확인 | 다른 사용자가 남긴 문화 요청 확인 |
| 문화콜 확인 | 비슷한 요청이 모인 집단 수요 확인 |
| 내 프로그램 확인 | 생성 가능 상태가 된 문화 프로그램 확인 |
| 상세 정보 확인 | 요청의 지역성, 맥락, 진행 상태 확인 |

### 관리자 모드

| 기능 | 설명 |
| --- | --- |
| 요청 관리 | 접수된 문화 요청 목록 확인 |
| 군집 관리 | 유사 요청이 모인 문화콜 상태 확인 |
| 공간 관리 | 지역 공간 또는 공공공간 후보 관리 |
| 지도 기반 확인 | 요청이 발생한 지역과 공간 후보를 지도에서 확인 |
| 프로그램 생성 | READY 상태의 문화콜을 실제 프로그램 후보로 전환 |

### AI/로직 기능

| 기능 | 설명 |
| --- | --- |
| 요청 임베딩 | 사용자의 자유 텍스트 요청을 벡터로 변환 |
| 유사도 계산 | 코사인 유사도를 기반으로 비슷한 요청 탐색 |
| 조건 기반 후보 제한 | 지역, 분야, 시간대, 예산, 대상 연령을 함께 고려 |
| 군집 상태 관리 | 기준 인원 충족 시 READY 상태로 자동 전환 |
| 공정성 점수 | 전통문화, 청소년/고령층, 저비용 요청에 가중치 부여 |

---

## 6. 현재 구현된 백엔드 API

기본 주소는 로컬 실행 기준 `http://127.0.0.1:8000/api/`입니다.

| Method | Endpoint | 설명 |
| --- | --- | --- |
| GET | `/api/health/` | API 서버 상태 확인 |
| GET/POST | `/api/requests/` | 문화 요청 목록 조회 및 생성 |
| GET | `/api/requests/<id>/` | 문화 요청 상세 조회 |
| GET | `/api/clusters/` | 전체 문화콜 군집 조회 |
| GET | `/api/clusters/ready/` | 프로그램 생성 가능 문화콜 조회 |
| GET | `/api/clusters/<id>/` | 문화콜 상세 조회 |
| POST | `/api/clusters/<id>/create-program/` | 문화콜 기반 프로그램 생성 |
| GET | `/api/programs/` | 생성된 프로그램 목록 조회 |
| GET | `/api/system_check/` | 백엔드 서버 상태 확인 |

---

## 7. 데이터 구조

### CultureRequest

사용자가 작성한 문화 요청입니다.

| 필드 | 의미 |
| --- | --- |
| `sido` | 시/도 |
| `sigungu` | 시/군/구 |
| `region_label` | 지역 표시명 |
| `main_category` | 전통문화, 공연, 전시, 체험, 기타 |
| `target_age` | 전체, 청소년, 청년, 고령층 |
| `preferred_time` | 희망 시간대 |
| `budget_range` | 희망 예산 |
| `title` | 요청 제목 |
| `content` | 요청 상세 내용 |
| `embedding` | 요청 텍스트 임베딩 벡터 |
| `cluster` | 연결된 RequestCluster |

### RequestCluster

비슷한 요청이 모여 생성된 문화콜입니다.

| 필드 | 의미 |
| --- | --- |
| `title` | 문화콜 제목 |
| `summary` | 문화콜 요약 |
| `region_label` | 대상 지역 |
| `main_category` | 문화 분야 |
| `request_count` | 모인 요청 수 |
| `threshold` | READY 전환 기준 인원 |
| `progress_ratio` | 기준 대비 진행률 |
| `remaining_count` | 남은 요청 수 |
| `status` | `COLLECTING`, `READY`, `PROGRAM_CREATED` |
| `fair_score` | 접근성·전통문화·저비용 등을 반영한 점수 |
| `fair_reason` | 공정성 점수 근거 |

### CultureProgram

READY 상태의 문화콜에서 생성된 프로그램 후보입니다.

| 필드 | 의미 |
| --- | --- |
| `cluster` | 기반이 된 문화콜 |
| `title` | 프로그램 제목 |
| `description` | 프로그램 설명 |
| `place_name` | 장소명 |
| `address` | 주소 |
| `creator_name` | 창작자/기획자명 |
| `is_local_creator` | 지역 창작자 여부 |
| `is_small_creator` | 소규모 창작자 여부 |
| `is_traditional` | 전통문화 여부 |

---

## 8. 기술 스택

| 영역 | 기술 |
| --- | --- |
| Frontend | React, Vite, JavaScript, HTML/CSS |
| Backend | Django, Django REST Framework |
| Database | SQLite |
| AI/Logic | Python, OpenAI Embedding, Fallback Embedding, Cosine Similarity |
| Map | Naver Map API 연동 구조 |
| Collaboration | GitHub Branch, Pull Request |

---

## 9. 실행 방법

### 9.1 Backend 실행

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

패키지 설치 및 서버 실행:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

백엔드 확인:

```bash
curl http://127.0.0.1:8000/api/system_check/
curl http://127.0.0.1:8000/api/health/
```

### 9.2 Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드 접속:

```text
http://127.0.0.1:5173
```

---

## 10. 환경 변수

백엔드에서 OpenAI Embedding을 사용할 경우 `backend/.env` 파일에 다음 값을 설정합니다.

```env
OPENAI_API_KEY=sk-...
EMBED_MODEL=text-embedding-3-small
SIM_THRESHOLD=0.25
MIN_CLUSTER_SIZE=3
USE_OPENAI_EMBEDDING=true
```

API 키가 없거나 호출에 실패해도 서비스 시연이 멈추지 않도록 fallback embedding 로직이 동작합니다.

---

## 11. 폴더 구조

```text
khuthon-2026/
│
├── assets/
│   └── culturecall-banner.svg
│
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   └── api/
│       ├── ai/
│       │   ├── clustering_engine.py
│       │   ├── embedding_service.py
│       │   ├── similarity.py
│       │   └── config.py
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── README.md
└── .gitignore
```

---

## 12. 차별점

### 단순 문화행사 검색 앱이 아닙니다

일반적인 문화 서비스는 이미 만들어진 행사를 사용자가 검색합니다. 문화콜은 사용자가 먼저 수요를 만들고, 비슷한 요청이 모이면 실제 프로그램 생성 후보가 됩니다.

### 인기순 추천을 반복하지 않습니다

조회수, 좋아요, 대형 콘텐츠 중심의 노출 구조를 따르지 않습니다. 대신 지역성, 접근 가능성, 예산, 시간대, 대상 연령, 전통문화 여부를 함께 고려합니다.

### 지도 앱으로 끝나지 않습니다

지도는 장소를 보여주기 위한 보조 기능입니다. 핵심은 요청 수집 → 군집화 → 상태 전환 → 공간/창작자 매칭 → 프로그램 생성으로 이어지는 흐름입니다.

### 전통문화를 현재의 선택지로 바꿉니다

전통문화는 보존 대상에 머무르지 않고, 사용자가 요청하고 창작자가 응답하며 지역에서 반복적으로 열릴 수 있는 문화 자원으로 연결됩니다.

---

## 13. 해커톤 MVP 범위

### 필수 구현

- 문화 요청 작성
- 요청 목록 조회
- 요청 상세 조회
- AI/유사도 기반 요청 군집화
- 문화콜 목록 조회
- READY 상태 전환
- 프로그램 생성 API
- 관리자/지도 기반 확인 화면

### 선택 구현

- 장소 후보 추천 고도화
- 창작자 데이터 입력 기능
- 공정성 점수 시각화
- 전통문화 프로그램 카드 디자인 강화
- 발표용 더미 데이터 세트 확장

---

## 14. Git 협업 규칙

main 브랜치에 직접 push하지 않고, 기능별 브랜치를 생성한 뒤 Pull Request를 통해 병합합니다.

```bash
git checkout main
git pull origin main
git checkout -b feat/기능명

# 작업 후
git add .
git commit -m "feat: 작업 내용"
git push origin feat/기능명
```

브랜치 예시:

```text
feat/backend-api
feat/frontend-ui
feat/ai-clustering
fix/request-form
docs/readme
```

커밋 메시지 예시:

```text
feat: 문화 요청 생성 API 구현
feat: 요청 군집화 로직 연결
fix: 중복 요청 생성 오류 수정
docs: README 프로젝트 설명 수정
style: 관리자 지도 화면 개선
```

---

## 15. 팀 역할

| 역할 | 담당 내용 |
| --- | --- |
| Backend | Django 서버, DB 모델, API, 관리자 기능 |
| Frontend | React 화면, 요청 폼, 목록/상세/지도 화면 |
| AI/Logic | 임베딩, 유사도 계산, 군집화 로직 |
| PM/Docs | 발표 자료, README, 시연 시나리오, GitHub 관리 보조 |

---

## 16. 발표 포인트

1. **문제 제기**: 문화가 부족한 것이 아니라 원하는 문화와 사용자가 연결되지 못한다.
2. **핵심 해결**: 개인의 문화 요청을 모아 집단 수요 데이터로 만든다.
3. **서비스 흐름**: 요청 작성 → 군집화 → READY 전환 → 관리자 확인 → 프로그램 생성.
4. **기술 구현**: Django REST API, SQLite, React, embedding 기반 유사도 계산.
5. **차별성**: 단순 행사 검색이 아니라 수요 기반 문화 생성 구조다.
6. **기대 효과**: 문화 접근성 개선, 지역 창작자 노출, 전통문화 지속가능성 강화.

---

## 17. 프로젝트 목표

문화콜의 목표는 문화를 더 많이 보여주는 것이 아닙니다.

**문화가 필요한 사람에게 도달하고, 다양한 문화가 공정하게 발견되며, 지역·전통문화가 지속적으로 재생산되는 구조를 만드는 것**입니다.
