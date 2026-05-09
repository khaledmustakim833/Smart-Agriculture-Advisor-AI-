# 🌾 Edge-Agri v4
### Multilingual Agricultural Advisory System — Powered by Gemini AI + BRRI Knowledge Base

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> Bangladesh's AI advisory system for smallholder farmers — powered by Gemini AI + RAG with BRRI knowledge base.

**Languages:** বাংলা 🇧🇩 | 中文 🇨🇳 | English 🇬🇧

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 💬 **Gemini AI Chatbot** | Intelligent answers using BRRI KB as context |
| 🔬 **Disease Detection** | PlantVillage-based plant disease identification |
| 🌐 **Trilingual** | বাংলা / 中文 / English |
| 🏠 **Live Dashboard** | KPI cards, weather widget, seasonal tips |
| 📊 **Market Prices** | Agricultural commodity prices |
| 🗓️ **Crop Calendar** | Boro/Aman/Aus seasonal calendar |
| 🔐 **Admin Panel** | Secure admin dashboard |

---

## 🤖 Chatbot Architecture (RAG + Gemini)

```
User Question
     │
     ▼
BRRI Knowledge Base (SQLite)
   keyword search → top 3 relevant entries
     │
     ▼
Gemini 1.5 Flash API
   context-aware prompt with KB entries
     │
     ▼
Intelligent Answer (in Bengali / English / Chinese)
     │
  Fallback: if no API key → use KB answer directly
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/edge-agri.git
cd edge-agri
pip install -r requirements.txt

# Set your Gemini API key (see below)
export GEMINI_API_KEY=your_key_here

streamlit run app.py
```

---

## 🔑 Gemini API Key Setup

The chatbot uses **Gemini 1.5 Flash** (free tier available).

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Click **"Create API key"** → copy your key
3. Set it as an environment variable:

**Local development:**
```bash
export GEMINI_API_KEY=AIza...your_key_here
```

**Streamlit Cloud:**
- Go to your app → **Settings → Secrets**
- Add:
```toml
GEMINI_API_KEY = "AIza...your_key_here"
```

> ⚠️ Without a Gemini API key, the chatbot still works using keyword-based KB matching (fallback mode).

---

## 📊 Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit |
| AI Chatbot | Gemini 1.5 Flash (Google) |
| RAG | SQLite KB + Gemini context prompt |
| Disease AI | PlantVillage heuristic model |
| Database | SQLite |
| Auth | bcrypt |

---

## 🔐 Admin Access

| Username | Password |
|----------|----------|
| `admin` | `admin123` |

---

## 📞 Agricultural Helpline: **16123**
## 📄 License: MIT
