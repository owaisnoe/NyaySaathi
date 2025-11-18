# helpers.py
"""
Helpers for Nyay-Saathi.
- get_cached_genai_model: returns genai.GenerativeModel(model_name)
- retry_call: simple retry wrapper
- JSON parsing helpers: robustly extract JSON from noisy LLM output
- doc_hash: accepts bytes/str
- format_docs / cached_retrieve: small utilities used by app.py
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

# ---------------------------------------------------------------------------
# Model factory (no temperature at init; matches older/new SDKs)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_cached_genai_model(model_name: str):
    """
    Return a cached genai.GenerativeModel instance keyed by model_name.
    Do not pass per-call generation args here (some old SDKs expect generation_config at init).
    """
    if genai is None:
        raise RuntimeError("google.generativeai (genai) is not available.")
    # Construct model with minimal args — callers will not pass temperature to generate_content
    try:
        return genai.GenerativeModel(model_name)
    except TypeError:
        # older/newer oddities: try named arg
        return genai.GenerativeModel(model_name=model_name)

# ---------------------------------------------------------------------------
# Retry wrapper
# ---------------------------------------------------------------------------
def retry_call(func, tries: int = 2, backoff: float = 1.0, allowed_exceptions: Tuple = (Exception,)):
    """
    Retry wrapper with exponential-ish backoff.
    Usage: retry_call(lambda: genai_model.generate_content(...))
    """
    for attempt in range(tries):
        try:
            return func()
        except allowed_exceptions:
            if attempt == tries - 1:
                raise
            time.sleep(backoff * (attempt + 1))

# ---------------------------------------------------------------------------
# JSON parsing helpers (robust)
# ---------------------------------------------------------------------------
def clean_code_fences(text: str) -> str:
    """Strip markdown code fences like ```json and trailing fences."""
    if not text:
        return ""
    return re.sub(r"```(?:json)?", "", text).strip()

def extract_json_block(text: str) -> Optional[str]:
    """Find first balanced {...} JSON block and return it, else None."""
    if not text:
        return None
    start = None
    depth = 0
    for i, ch in enumerate(text):
        if ch == "{" and start is None:
            start = i
            depth = 1
            continue
        if start is not None:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
    return None

def safe_parse_json(text: str) -> dict:
    """
    Try to parse JSON from text. Steps:
      1) try entire text
      2) find a balanced {...} block and parse that
      3) try light quotes normalization
    Raises ValueError with helpful message on failure.
    """
    if not text or not text.strip():
        raise ValueError("No text to parse as JSON.")
    t = clean_code_fences(text)
    # attempt direct parse
    try:
        return json.loads(t)
    except Exception:
        pass
    # try block extraction
    block = extract_json_block(t)
    if block:
        try:
            return json.loads(block)
        except Exception as e:
            raise ValueError(f"Found JSON-like block but failed to parse: {e}\nBlock snippet: {block[:1000]}")
    # fallback: normalize quotes and try
    alt = t.strip().replace("''", '"').replace("‘", '"').replace("’", '"')
    alt = alt.replace("“", '"').replace("”", '"')
    try:
        return json.loads(alt)
    except Exception as e:
        raise ValueError(f"Unable to parse JSON: {e}\nSnippet: {t[:1000]}")

def parse_genai_json_response(text: str) -> dict:
    return safe_parse_json(text)

# ---------------------------------------------------------------------------
# Small helpers used by app.py
# ---------------------------------------------------------------------------
def doc_hash(text: str | bytes) -> str:
    if isinstance(text, (bytes, bytearray)):
        data = bytes(text)
    else:
        data = (text or "").encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def format_docs(docs: List, per_doc_chars: int = 1000) -> str:
    parts = []
    for d in docs:
        meta = getattr(d, "metadata", {}) or {}
        src = meta.get("source") or meta.get("title") or "guide"
        content = (getattr(d, "page_content", "") or "")[:per_doc_chars]
        parts.append(f"SOURCE: {src}\n{content}...")
    return "\n\n".join(parts)

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
