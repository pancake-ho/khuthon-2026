import json
import os
from typing import List

from openai import OpenAI
from openai import OpenAIError

import config
from models import AppState


class EmbeddingService:
    """
    OpenAI embedding 생성과 embedding cache 저장/로드를 담당한다.
    """

    def __init__(self, state: AppState):
        if not config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY가 없습니다. .env 파일에 OPENAI_API_KEY=sk-... 형태로 입력하세요."
            )

        self.state = state
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def load_cache(self) -> None:
        """
        embedding_cache.json 파일을 읽어 기존 임베딩 캐시를 불러온다.
        """
        if not os.path.exists(config.CACHE_FILE):
            self.state.embedding_cache = {}
            return

        try:
            with open(config.CACHE_FILE, "r", encoding="utf-8") as f:
                self.state.embedding_cache = json.load(f)
        except json.JSONDecodeError:
            print(f"[경고] {config.CACHE_FILE} 파일이 깨져 있어서 새 캐시로 시작합니다.")
            self.state.embedding_cache = {}

    def save_cache(self) -> None:
        """
        현재 임베딩 캐시를 embedding_cache.json 파일에 저장한다.
        """
        with open(config.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state.embedding_cache, f, ensure_ascii=False)

    def clean_text(self, text: str) -> str:
        """
        터미널/복붙 과정에서 들어올 수 있는 깨진 유니코드 문자를 제거한다.
        """
        cleaned_text = text.replace("\n", " ").strip()
        cleaned_text = cleaned_text.encode("utf-8", errors="ignore").decode("utf-8")
        return cleaned_text

    def get_embedding(self, text: str) -> List[float]:
        """
        사용자의 자유 요청 문장을 OpenAI embedding vector로 변환한다.
        이미 캐시에 있는 문장이면 OpenAI API를 다시 호출하지 않는다.
        """
        cleaned_text = self.clean_text(text)

        if not cleaned_text:
            raise ValueError("빈 문자열은 임베딩할 수 없습니다.")

        if cleaned_text in self.state.embedding_cache:
            return self.state.embedding_cache[cleaned_text]

        try:
            response = self.client.embeddings.create(
                model=config.EMBED_MODEL,
                input=cleaned_text,
            )
        except OpenAIError as e:
            raise RuntimeError(
                "OpenAI 임베딩 API 호출 중 오류가 발생했습니다. "
                "API 키, quota, 인터넷 연결을 확인하세요.\n"
                f"원본 오류: {e}"
            )

        embedding = response.data[0].embedding
        self.state.embedding_cache[cleaned_text] = embedding
        self.save_cache()

        return embedding