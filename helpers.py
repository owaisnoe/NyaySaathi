"""
helpers.py - Nyay-Saathi (focused helpers)

- get_cached_genai_model (no temperature at init)
- retry_call
- robust JSON parsing helpers
- trimming/formatting helpers
- cached_retrieve wrapper
- doc_hash that accepts bytes or str
"""

import re
import json
import time
import hashlib
from typing import List, Optional, Tuple

try:
    import streamlit as st
except Exception:
    class _DummySt:
        def cache_resource(self, *a, **k):
            def dec(f):
                return f
            return dec
        def cache_data(self, *a, **k):
            def dec(f):
                return f
            return dec
    st = _DummySt()

try:
    import google.generativeai as genai
except Exception:
    genai = None

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
except Exception:
    HuggingFaceEmbeddings = None

# ---------------------------------------------------------------------------
# GenAI model caching
# ---------------------------------------------------------------------------
@st.cache_resource
def get_cached_genai_model(model_name: str):
    """
    Return a cached genai.GenerativeModel instance keyed by (model_name).
    Do NOT pass temperature here — pass it per API call.
    """
    if genai is None:
        raise RuntimeError("google.generativeai (genai) is not available in this environment.")
    return genai.GenerativeModel(model_name)

# ---------------------------------------------------------------------------
# Retry wrapper
# ---------------------------------------------------------------------------
def retry_call(func, tries: int = 3, backoff: float = 1.5, allowed_exceptions: Tuple = (Exception,)):
    """Simple retry wrapper with exponential backoff."""
    for attempt in range(tries):
        try:
            return func()
        except allowed_exceptions as e:
            if attempt == tries - 1:
                raise
            sleep_time = backoff ** attempt
            time.sleep(sleep_time)

# ---------------------------------------------------------------------------
# JSON extraction & parsing helpers
# ---------------------------------------------------------------------------
def extract_json_block(text: str) -> Optional[str]:
    """Extract the first balanced JSON object from text using a simple stack scan."""
    if not text:
        return None
    start_idx = None
    depth = 0
    for i, ch in enumerate(text):
        if ch == "{" and start_idx is None:
            start_idx = i
            depth = 1
            continue
        if start_idx is not None:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start_idx: i + 1]
    return None

def clean_code_fences(text: str) -> str:
    """Remove markdown code fences (like ```json) commonly returned by LLMs."""
    return re.sub(r"```(?:json)?", "", text or "").strip()

def safe_parse_json(text: str) -> dict:
    """Attempt to extract and parse JSON from text robustly. Raises ValueError on failure."""
    if not text:
        raise ValueError("No text provided to parse JSON from.")
    text = clean_code_fences(text)
    try:
        return json.loads(text)
    except Exception:
        pass
    block = extract_json_block(text)
    if block:
        try:
            return json.loads(block)
        except Exception as e:
            raise ValueError(f"Found JSON-like block but failed to parse: {e}\nBlock:\n{block[:1000]}")
    try:
        alt = text.strip().replace('\"\"', '"').replace("'", '"')
        return json.loads(alt)
    except Exception as e:
        raise ValueError(f"Unable to parse JSON from text: {e}\nSnippet:\n{(text or '')[:1000]}")

def parse_genai_json_response(response_text: str) -> dict:
    cleaned = clean_code_fences(response_text)
    return safe_parse_json(cleaned)

# ---------------------------------------------------------------------------
# Context trimming & formatting
# ---------------------------------------------------------------------------
def trim_to_chars(text: Optional[str], max_chars: int = 4000) -> str:
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 100] + "\n\n...[truncated]..."

def format_docs(docs: List, per_doc_chars: int = 1000) -> str:
    parts = []
    for d in docs:
        src = getattr(d, "metadata", {})
        if isinstance(src, dict):
            src_name = src.get("source") or src.get("title") or "guide"
        else:
            src_name = "guide"
        content = (getattr(d, "page_content", "") or "")[:per_doc_chars]
        parts.append(f"SOURCE: {src_name}\n{content}...")
    return "\n\n".join(parts)

# ---------------------------------------------------------------------------
# Simple retrieval cache (uses st.session_state)
# ---------------------------------------------------------------------------
def cached_retrieve(retriever, question: str, k: int = 3):
    if not hasattr(st, "session_state"):
        try:
            return retriever.get_relevant_documents(question)[:k]
        except Exception:
            return retriever.retrieve(question)[:k]
    cache = st.session_state.setdefault("_retrieval_cache", {})
    key = "retrieval::" + hashlib.sha256(question.encode("utf-8")).hexdigest() + f"::k={k}"
    if key in cache:
        return cache[key]
    try:
        docs = retriever.get_relevant_documents(question)[:k]
    except Exception:
        docs = retriever.retrieve(question)[:k]
    cache[key] = docs
    return docs

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
def doc_hash(text: str | bytes) -> str:
    """Compute sha256 hash from str or bytes (safe for uploaded file bytes)."""
    if isinstance(text, (bytes, bytearray)):
        data = bytes(text)
    else:
        data = (text or "").encode("utf-8")
    return hashlib.sha256(data).hexdigest()
