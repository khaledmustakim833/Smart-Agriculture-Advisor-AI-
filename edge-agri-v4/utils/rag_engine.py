# utils/rag_engine.py
# RAG engine — BRRI KB (scored search) + Gemini AI

import os
import json
import urllib.request
from utils.database import search_knowledge, log_query

QUICK_QUESTIONS = {
    "bn": [
        "ধানে ব্লাস্ট রোগ হলে কী করবো?",
        "বোরো ধানে কতটুকু সার দিতে হবে?",
        "আমন ধান কখন রোপণ করবো?",
        "মাজরা পোকা দমনের উপায় কী?",
        "AWD পদ্ধতিতে সেচ কীভাবে দেবো?",
        "ধান কাটার সঠিক সময় কখন?",
    ],
    "zh": [
        "水稻稻瘟病怎么处理?",
        "博罗水稻需要多少肥料?",
        "阿曼水稻何时移栽?",
        "如何防治螟虫?",
        "如何进行AWD灌溉?",
        "水稻收割的正确时间是什么时候?",
    ],
    "en": [
        "What to do if rice has blast disease?",
        "How much fertilizer for Boro rice?",
        "When to transplant Aman rice?",
        "How to control stem borer?",
        "How to do AWD irrigation?",
        "When is the right time to harvest rice?",
    ],
}

NO_RESULT_MSG = {
    "bn": "দুঃখিত, এই বিষয়ে আমার জ্ঞানভাণ্ডারে তথ্য নেই। অনুগ্রহ করে কৃষি হেল্পলাইন **16123** এ কল করুন।",
    "zh": "抱歉，我的知识库中没有相关信息。请拨打农业热线 **16123**。",
    "en": "Sorry, I don't have information on this topic. Please call the agricultural helpline **16123**.",
}

GREETING_MSG = {
    "bn": "আসসালামুয়ালাইকুম! 🌾 আমি **Edge-Agri চ্যাটবট**। আপনার কৃষি সমস্যা জানান, আমি BRRI জ্ঞানভাণ্ডার থেকে পরামর্শ দেবো।",
    "zh": "您好！🌾 我是 **Edge-Agri 聊天机器人**。请告诉我您的农业问题，我将从BRRI知识库为您提供建议。",
    "en": "Hello! 🌾 I am the **Edge-Agri Chatbot**. Tell me your agricultural problem and I'll provide BRRI-validated advice.",
}


def _get_api_key() -> str:
    """Get Gemini API key from env var or Streamlit secrets."""
    # 1. Environment variable (local dev / Docker)
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    # 2. Streamlit secrets (Streamlit Cloud deployment)
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return ""


def _call_gemini(prompt: str, api_key: str) -> str:
    """Call Gemini 1.5 Flash and return the answer text."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-1.5-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 800,
            "topP": 0.8,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    candidates = result.get("candidates", [])
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        if parts:
            return parts[0].get("text", "").strip()
    return ""


def _build_prompt(query: str, lang: str, kb_results: list, district: str = "") -> str:
    """Build RAG prompt: KB context + user question."""
    lang_instruction = {
        "bn": "বাংলায় উত্তর দিন। সহজ ও স্পষ্ট ভাষায় কৃষকের উপযোগী পরামর্শ দিন।",
        "zh": "请用中文回答。用简单清晰的语言提供适合农民的建议。",
        "en": "Answer in English. Give practical, clear advice suitable for a farmer.",
    }.get(lang, "Answer in English.")

    district_info = f"Farmer's district: {district}\n" if district else ""

    kb_context = ""
    if kb_results:
        kb_context = "\n=== BRRI Knowledge Base (use as primary reference) ===\n"
        for i, row in enumerate(kb_results, 1):
            if lang == "bn":
                q = row.get("question_bn", "")
                a = row.get("answer_bn", "")
            elif lang == "zh":
                q = row.get("question_bn", "")
                a = row.get("answer_zh") or row.get("answer_bn", "")
            else:
                q = row.get("question_en") or row.get("question_bn", "")
                a = row.get("answer_en") or row.get("answer_bn", "")
            src = row.get("source", "BRRI Manual")
            kb_context += f"[{i}] Source: {src}\nQ: {q}\nA: {a}\n\n"

    return f"""You are Edge-Agri AI — an expert agricultural assistant for Bangladesh rice and crop farming. You give accurate, practical advice based on BRRI (Bangladesh Rice Research Institute) guidelines.

{lang_instruction}
{district_info}
{kb_context}
=== Farmer's Question ===
{query}

=== Rules ===
- Use the BRRI KB above as your primary reference when relevant to the question
- If the question is about something NOT in the KB (e.g. tomato, vegetable, other crops), use your general agricultural knowledge to answer correctly — do NOT give a rice-related answer for non-rice questions
- Always give specific, actionable advice (quantities, timing, exact methods)
- Keep the answer concise (3-6 sentences or bullet points)
- If recommending pesticides/chemicals, include safety tips
- Never say "I don't know" — always provide the best agricultural guidance

Answer:"""


def answer_query(query: str, lang: str = "bn", district: str = "") -> dict:
    """
    RAG pipeline:
    1. Scored KB search → best matching entries as context
    2. Gemini AI → intelligent, context-aware answer
    3. Fallback to KB direct answer if Gemini unavailable
    """
    if not query.strip():
        return {
            "answer": GREETING_MSG.get(lang, GREETING_MSG["en"]),
            "source": "", "confidence": 1.0, "kb_id": None, "found": True,
        }

    # Step 1: Scored KB retrieval
    kb_results = search_knowledge(query, lang, top_k=3)
    best_kb_id = kb_results[0]["id"] if kb_results else None
    best_source = kb_results[0].get("source", "BRRI Manual") if kb_results else "BRRI Manual"

    # Step 2: Try Gemini AI
    api_key = _get_api_key()
    gemini_answer = ""
    if api_key:
        try:
            prompt = _build_prompt(query, lang, kb_results, district)
            gemini_answer = _call_gemini(prompt, api_key)
        except Exception:
            gemini_answer = ""

    # Step 3: Choose best answer
    if gemini_answer:
        answer = gemini_answer
        confidence = 0.92
        source_label = f"Gemini AI + {best_source}" if kb_results else "Gemini AI"
        found = True
    elif kb_results:
        # Fallback: direct KB answer
        best = kb_results[0]
        if lang == "zh" and best.get("answer_zh"):
            answer = best["answer_zh"]
        elif lang == "en" and best.get("answer_en"):
            answer = best["answer_en"]
        else:
            answer = best["answer_bn"]
        words = set(query.lower().split())
        keywords = set((best.get("keywords") or "").lower().split(","))
        overlap = len(words & keywords) / max(len(words), 1)
        confidence = min(0.85, 0.55 + overlap * 0.35)
        source_label = best_source
        found = True
    else:
        answer = NO_RESULT_MSG.get(lang, NO_RESULT_MSG["en"])
        confidence = 0.0
        source_label = ""
        found = False

    # Related questions from KB results 2 & 3
    related = []
    for r in kb_results[1:]:
        q = r.get("question_en") or r["question_bn"] if lang == "en" else r["question_bn"]
        related.append(q)

    log_query(query, lang, answer, best_kb_id, confidence, district)

    return {
        "answer": answer,
        "source": source_label,
        "category": kb_results[0].get("category", "") if kb_results else "",
        "confidence": round(confidence, 2),
        "kb_id": best_kb_id,
        "found": found,
        "related": related,
    }
