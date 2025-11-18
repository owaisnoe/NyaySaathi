# helpers.py - Minimal, robust utilities for Nyay-Saathi
# This file is intentionally small and import-safe to avoid ImportError on startup.

import re
import json
import time
import hashlib
from typing import List, Optional, Tuple

# Streamlit is optional here; if not available, create a small dummy shim
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

# google.generativeai is optional at import time. We only import it if used at runtime.
try:
    import google.generativeai as genai
except Exception:
    genai = None

# ---------------------------------------------------------------------------
# Model factory (kept minimal and defensive)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_cached_genai_model(model_name: str):
    """
    Return a genai.GenerativeModel instance.
    This factory tries to construct the model in a way compatible with multiple SDK versions.
    genai must be configured (genai.configure(...)) before calling this.
    """
    if genai is None:
        raise RuntimeError("google.generativeai (genai) is not available. Make sure package is installed.")
    # Try simple constructor forms (some SDKs accept model_name positional, others named)
    try:
        return genai.GenerativeModel(model_name)
    except TypeError:
        return genai.GenerativeModel(model_name=model_name)

# ---------------------------------------------------------------------------
# Retry wrapper
# ---------------------------------------------------------------------------
def retry_call(func, tries: int = 2, backoff: float = 1.0, allowed_exceptions: Tuple = (Exception,)):
    """
    Simple retry, used around network/LLM calls.
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
# JSON parsing helpers (robust to code-fence wrappers)
# ---------------------------------------------------------------------------
def clean_code_fences(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"```(?:json)?", "", text).strip()

def extract_json_block(text: str) -> Optional[str]:
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
    if not text or not text.strip():
        raise ValueError("No text provided for JSON parsing.")
    t = clean_code_fences(text)
    try:
        return json.loads(t)
    except Exception:
        pass
    block = extract_json_block(t)
    if block:
        try:
            return json.loads(block)
        except Exception as e:
            raise ValueError(f"Found JSON-like block but failed to parse: {e}\nBlock: {block[:500]}")
    alt = t.strip().replace("''", '"').replace("‘", '"').replace("’", '"').replace('“', '"').replace('”', '"')
    try:
        return json.loads(alt)
    except Exception as e:
        raise ValueError(f"Unable to parse JSON: {e}\nSnippet: {t[:500]}")

def parse_genai_json_response(text: str) -> dict:
    return safe_parse_json(text)

# ---------------------------------------------------------------------------
# Small helpers
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
        src_name = meta.get("source") or meta.get("title") or "guide"
        content = (getattr(d, "page_content", "") or "")[:per_doc_chars]
        parts.append(f"SOURCE: {src_name}\n{content}...")
    return "\n\n".join(parts)

def cached_retrieve(retriever, question: str, k: int = 3):
    """
    Minimal retrieval cache using st.session_state to avoid repeated calls.
    Falls back gracefully if retriever does not provide get_relevant_documents.
    """
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
