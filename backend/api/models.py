
from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class AppState:
    """실행 중 임시 데이터를 저장한다. 실제 서비스에서는 DB로 대체한다."""
    clusters: List[Dict[str, Any]] = field(default_factory=list)
    embedding_cache: Dict[str, List[float]] = field(default_factory=dict)
