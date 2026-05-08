
from typing import List
import numpy as np

def cosine_similarity(a: List[float], b: List[float]) -> float:
    vec_a = np.array(a)
    vec_b = np.array(b)
    denominator = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denominator == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denominator)
