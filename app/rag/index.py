from pathlib import Path
import json
import pickle
import faiss
from rank_bm25 import BM25Okapi
from .embeddings import Embedder


class HybridIndex:
    def __init__(self, index_dir: Path, embedding_model: str):
        self.index_dir = index_dir
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.embedder = Embedder(embedding_model)
        self.index = None
        self.chunks = []
        self.bm25 = None
        self.load()

    def build(self, chunks: list[dict]):
        self.chunks = chunks
        vectors = self.embedder.encode([c["text"] for c in chunks])
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        self.bm25 = BM25Okapi([c["text"].lower().split() for c in chunks])
        faiss.write_index(self.index, str(self.index_dir / "vectors.faiss"))
        (self.index_dir / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
        with open(self.index_dir / "bm25.pkl", "wb") as f:
            pickle.dump(self.bm25, f)

    def load(self):
        vector_path = self.index_dir / "vectors.faiss"
        chunks_path = self.index_dir / "chunks.json"
        bm25_path = self.index_dir / "bm25.pkl"
        if vector_path.exists() and chunks_path.exists() and bm25_path.exists():
            self.index = faiss.read_index(str(vector_path))
            self.chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
            with open(bm25_path, "rb") as f:
                self.bm25 = pickle.load(f)

    def search(self, query: str, top_k: int = 6) -> list[dict]:
        if self.index is None or not self.chunks:
            return []
        k = min(max(top_k * 3, top_k), len(self.chunks))
        qvec = self.embedder.encode([query])
        scores, ids = self.index.search(qvec, k)
        vector_scores = {int(i): float(s) for i, s in zip(ids[0], scores[0]) if i >= 0}

        bm_scores = self.bm25.get_scores(query.lower().split())
        ranked_bm = sorted(range(len(bm_scores)), key=lambda i: bm_scores[i], reverse=True)[:k]
        max_bm = max([bm_scores[i] for i in ranked_bm], default=1.0) or 1.0
        max_vec = max(vector_scores.values(), default=1.0) or 1.0

        candidates = set(vector_scores) | set(ranked_bm)
        results = []
        for i in candidates:
            hybrid = 0.65 * (vector_scores.get(i, 0.0) / max_vec) + 0.35 * (bm_scores[i] / max_bm)
            item = dict(self.chunks[i])
            item["score"] = round(float(hybrid), 4)
            results.append(item)
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
