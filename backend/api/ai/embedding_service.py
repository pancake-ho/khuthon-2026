import hashlib
import random
from typing import List

from openai import OpenAI
from openai import OpenAIError

from . import config


class EmbeddingService:
    """
    사용자 요청 문장을 embedding vector로 변환한다.

    1. USE_OPENAI_EMBEDDING=true이면 OpenAI embedding 사용
    2. API 키가 없거나 오류가 나면 fallback embedding 사용
    3. 해커톤 시연 안정성을 위해 fallback을 반드시 제공
    """

    def __init__(self):
        self.client = None

        if config.USE_OPENAI_EMBEDDING and config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def clean_text(self, text: str) -> str:
        cleaned_text = (text or "").replace("\n", " ").strip()
        cleaned_text = cleaned_text.encode("utf-8", errors="ignore").decode("utf-8")
        return cleaned_text

    def get_embedding(self, text: str) -> List[float]:
        cleaned_text = self.clean_text(text)

        if not cleaned_text:
            raise ValueError("빈 문자열은 임베딩할 수 없습니다.")

        if self.client is None:
            return self._fallback_embedding(cleaned_text)

        try:
            response = self.client.embeddings.create(
                model=config.EMBED_MODEL,
                input=cleaned_text,
            )
            return response.data[0].embedding

        except OpenAIError:
            return self._fallback_embedding(cleaned_text)

        except Exception:
            return self._fallback_embedding(cleaned_text)

    def _fallback_embedding(self, text: str, dim: int = 128) -> List[float]:
        """
        OpenAI API가 안 될 때도 시연이 멈추지 않게 하는 간단한 deterministic embedding.
        같은 문장은 항상 같은 벡터가 나오게 만든다.
        """
        seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
        rng = random.Random(seed)

        vector = [rng.uniform(-1.0, 1.0) for _ in range(dim)]

        norm = sum(v * v for v in vector) ** 0.5
        if norm == 0:
            return vector

        return [v / norm for v in vector]