from openai import OpenAI
from app.core.config import settings

SYSTEM_PROMPT = """
You are a document-grounded AI knowledge assistant.
Answer the user's question using ONLY the supplied retrieved document context and conversation history.
If the retrieved context does not contain enough evidence, say that the documents do not provide enough information.
Do not invent facts, citations, page numbers, specifications, or quotations.
When useful, synthesize information across multiple sources.
Keep answers clear and practical.
At the end, cite sources in the format [Source: filename, page N].
""".strip()


class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def answer(self, question: str, context: list[dict], history: list[dict]) -> str:
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        context_text = "\n\n".join(
            f"SOURCE: {c['source']} | PAGE: {c['page']}\n{c['text']}" for c in context
        )
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for item in history[-settings.max_history_turns * 2:]:
            if item.get("role") in {"user", "assistant"}:
                messages.append({"role": item["role"], "content": item["content"]})
        messages.append({
            "role": "user",
            "content": f"Retrieved document context:\n\n{context_text}\n\nQuestion: {question}",
        })
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            temperature=0.1,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
