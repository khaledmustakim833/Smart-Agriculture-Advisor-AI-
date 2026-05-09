"""
Edge-Agri v4 — World-Class Multilingual Agricultural Advisory
Professional upgrade: glassmorphism dark UI, live dashboard, weather widget,
seasonal crop calendar, market prices, 5-tab navigation, enhanced chat.
"""
import streamlit as st, sys, os, datetime
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from utils.database import init_db, get_stats
from utils.translations import t

st.set_page_config(
    page_title="Edge-Agri v4 🌾 | কৃষি AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_db()

DEFAULTS = {
    "page": "landing",
    "lang": "bn",
    "user_name": "",
    "user_district": "",
    "chat_history": [],
    "admin_logged_in": False,
    "last_detection": None,
    "user_tab": "dashboard",
    "voice_text": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

lang = st.session_state.lang

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
:root{--g9:#003d24;--g7:#006a4e;--g6:#00853f;--g4:#4ade80;--g3:#86efac;--red:#f42a41;--gold:#d4a017;--blue:#1565c0;--glass:rgba(255,255,255,0.06);--gb:rgba(255,255,255,0.12);}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans','Hind Siliguri','Noto Sans SC',sans-serif!important;}
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDeployButton"],[data-testid="stSidebar"]{display:none!important;}
.main .block-container{padding:0!important;max-width:100%!important;}
.stApp{background:#070d08;}

.topbar{position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(4,10,5,0.95);backdrop-filter:blur(20px);height:62px;display:flex;align-items:center;justify-content:space-between;padding:0 32px;border-bottom:1px solid rgba(74,222,128,0.18);box-shadow:0 4px 32px rgba(0,0,0,0.6);}
.t-brand{display:flex;align-items:center;gap:12px;}
.t-logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#006a4e,#00853f);display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 20px rgba(74,222,128,0.25);}
.t-name{color:#fff;font-size:17px;font-weight:800;letter-spacing:-.3px;}
.t-sub{color:rgba(74,222,128,0.7);font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;}
.t-right{display:flex;align-items:center;gap:10px;}
.ubadge{display:flex;align-items:center;gap:8px;background:rgba(0,106,78,0.25);border:1px solid rgba(74,222,128,0.25);border-radius:20px;padding:6px 14px;color:#fff;font-size:13px;font-weight:600;}
.udot{width:8px;height:8px;background:#4ade80;border-radius:50%;animation:pd 2s infinite;}
@keyframes pd{0%,100%{opacity:1}50%{opacity:.4}}

.hero-wrap{min-height:100vh;background:radial-gradient(ellipse at 15% 25%,rgba(0,106,78,.3) 0%,transparent 50%),radial-gradient(ellipse at 85% 75%,rgba(0,106,78,.18) 0%,transparent 50%),linear-gradient(160deg,#040c06 0%,#070f08 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:90px 24px 60px;position:relative;overflow:hidden;}
.hero-grid-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(74,222,128,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(74,222,128,.025) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;}
.eyebrow{display:inline-flex;align-items:center;gap:8px;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);border-radius:20px;padding:6px 18px;margin-bottom:24px;font-size:12px;font-weight:700;color:#4ade80;letter-spacing:1px;text-transform:uppercase;}
.hero-h1{font-size:clamp(34px,6vw,72px);font-weight:800;line-height:1.05;letter-spacing:-2px;color:#fff;text-align:center;margin-bottom:18px;}
.hero-accent{background:linear-gradient(135deg,#4ade80 0%,#22d3ee 50%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:clamp(14px,2vw,18px);color:rgba(255,255,255,.5);max-width:560px;margin:0 auto 36px;line-height:1.75;text-align:center;}
.flags-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:44px;}
.flag-pill{background:var(--glass);border:1px solid var(--gb);border-radius:12px;padding:7px 16px;font-size:13px;font-weight:600;color:rgba(255,255,255,.75);backdrop-filter:blur(8px);}

.portal-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:680px;width:100%;}
.portal-card{background:var(--glass);border:1px solid var(--gb);border-radius:24px;padding:34px 26px;text-align:center;backdrop-filter:blur(16px);transition:all .3s;position:relative;overflow:hidden;}
.portal-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.portal-card.farmer::before{background:linear-gradient(90deg,#006a4e,#4ade80);}
.portal-card.admin::before{background:linear-gradient(90deg,#f42a41,#ff8080);}
.portal-card:hover{transform:translateY(-6px);box-shadow:0 32px 64px rgba(0,0,0,.5);}
.portal-card.farmer:hover{border-color:rgba(74,222,128,.35);}
.portal-card.admin:hover{border-color:rgba(244,42,65,.35);}
.p-icon{font-size:46px;margin-bottom:14px;}
.p-title{font-size:19px;font-weight:800;color:#fff;margin-bottom:8px;}
.p-desc{font-size:13px;color:rgba(255,255,255,.5);line-height:1.6;margin-bottom:22px;}

.stats-strip{display:flex;gap:24px;justify-content:center;margin-top:52px;flex-wrap:wrap;}
.stat-pill{text-align:center;padding:16px 22px;background:var(--glass);border:1px solid var(--gb);border-radius:16px;backdrop-filter:blur(8px);}
.stat-num{font-size:26px;font-weight:800;color:#4ade80;line-height:1;}
.stat-lbl{font-size:10px;color:rgba(255,255,255,.35);margin-top:4px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

.auth-wrap{min-height:100vh;background:radial-gradient(ellipse at 40% 30%,rgba(0,106,78,.2) 0%,transparent 60%),linear-gradient(160deg,#040c06 0%,#070e08 100%);display:flex;align-items:center;justify-content:center;padding:90px 20px 40px;}
.auth-card{background:rgba(255,255,255,.04);border:1px solid var(--gb);border-radius:28px;width:100%;max-width:430px;backdrop-filter:blur(20px);overflow:hidden;box-shadow:0 32px 80px rgba(0,0,0,.5);}
.auth-head{padding:34px 34px 26px;text-align:center;border-bottom:1px solid var(--gb);}
.auth-head.farmer{background:linear-gradient(135deg,rgba(0,106,78,.4),rgba(0,133,63,.2));}
.auth-head.admin{background:linear-gradient(135deg,rgba(200,16,46,.4),rgba(154,0,32,.2));}
.auth-icon{width:70px;height:70px;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:34px;margin:0 auto 14px;}
.auth-icon.farmer{background:linear-gradient(135deg,#006a4e,#00853f);box-shadow:0 8px 32px rgba(0,106,78,.4);}
.auth-icon.admin{background:linear-gradient(135deg,#c8102e,#9a0020);box-shadow:0 8px 32px rgba(200,16,46,.4);}
.auth-title{font-size:21px;font-weight:800;color:#fff;margin-bottom:4px;}
.auth-sub{font-size:13px;color:rgba(255,255,255,.5);}
.auth-body{padding:30px 34px 34px;}

.app-wrap{padding-top:62px;min-height:100vh;background:#070d08;}
.user-strip{background:linear-gradient(135deg,rgba(0,40,20,.95),rgba(0,20,10,.98));border-bottom:1px solid rgba(74,222,128,.12);padding:18px 32px;display:flex;align-items:center;justify-content:space-between;}
.u-greet{color:#fff;font-size:21px;font-weight:800;}
.u-loc{display:inline-flex;align-items:center;gap:6px;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.2);border-radius:20px;padding:4px 12px;color:#4ade80;font-size:12px;font-weight:700;}

.tab-bar{background:rgba(4,10,5,.97);border-bottom:1px solid rgba(74,222,128,.1);padding:0 28px;display:flex;gap:0;position:sticky;top:62px;z-index:500;backdrop-filter:blur(12px);overflow-x:auto;scrollbar-width:none;}
.tab-bar::-webkit-scrollbar{display:none;}
.tab-btn{padding:15px 20px;font-size:13px;font-weight:700;color:rgba(255,255,255,.4);border-bottom:2px solid transparent;cursor:pointer;transition:all .2s;white-space:nowrap;display:flex;align-items:center;gap:6px;background:transparent;border-top:none;border-left:none;border-right:none;font-family:inherit;}
.tab-btn:hover{color:rgba(255,255,255,.75);}
.tab-btn.active{color:#4ade80;border-bottom-color:#4ade80;}

.content{padding:28px 32px;max-width:1280px;margin:0 auto;}

.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px;}
.kpi-card{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:22px 20px;position:relative;overflow:hidden;transition:all .2s;}
.kpi-card:hover{border-color:rgba(255,255,255,.14);transform:translateY(-2px);}
.kpi-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;}
.kpi-card.green::after{background:linear-gradient(90deg,#006a4e,#4ade80);}
.kpi-card.red::after{background:linear-gradient(90deg,#f42a41,#ff8080);}
.kpi-card.gold::after{background:linear-gradient(90deg,#b45309,#d4a017);}
.kpi-card.blue::after{background:linear-gradient(90deg,#1e40af,#60a5fa);}
.kpi-icon{font-size:26px;margin-bottom:10px;}
.kpi-val{font-size:30px;font-weight:800;color:#fff;line-height:1;margin-bottom:4px;}
.kpi-lbl{font-size:11px;color:rgba(255,255,255,.38);font-weight:700;text-transform:uppercase;letter-spacing:.5px;}
.kpi-trend{font-size:11px;margin-top:8px;font-weight:700;}
.kpi-trend.up{color:#4ade80;}.kpi-trend.stable{color:rgba(255,255,255,.25);}

.sec-title{font-size:17px;font-weight:800;color:#fff;margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.sec-sub{font-size:12px;color:rgba(255,255,255,.35);margin-left:8px;font-weight:500;}

.weather-card{background:linear-gradient(135deg,rgba(21,101,192,.25),rgba(30,64,175,.15));border:1px solid rgba(96,165,250,.2);border-radius:20px;padding:22px;display:flex;align-items:center;gap:20px;}
.w-temp{font-size:46px;font-weight:800;color:#fff;line-height:1;}
.w-icon{font-size:52px;}
.w-cond{color:#fff;font-size:15px;font-weight:700;margin-bottom:4px;}
.w-detail{display:flex;gap:16px;margin-top:10px;}
.w-stat{font-size:12px;color:rgba(255,255,255,.45);}
.w-stat strong{color:rgba(96,165,250,.9);font-size:13px;display:block;}

.feat-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:22px;cursor:pointer;transition:all .25s;position:relative;overflow:hidden;}
.feat-card:hover{border-color:rgba(74,222,128,.3);background:rgba(74,222,128,.04);transform:translateY(-3px);box-shadow:0 16px 48px rgba(0,0,0,.3);}
.fc-icon{font-size:38px;margin-bottom:12px;}
.fc-title{font-size:15px;font-weight:800;color:#fff;margin-bottom:5px;}
.fc-desc{font-size:12px;color:rgba(255,255,255,.4);line-height:1.6;}
.fc-arrow{position:absolute;right:18px;top:50%;transform:translateY(-50%);font-size:18px;color:rgba(255,255,255,.18);transition:all .2s;}
.feat-card:hover .fc-arrow{color:#4ade80;transform:translateY(-50%) translateX(4px);}

.tip-card{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-left:3px solid #006a4e;border-radius:14px;padding:16px 18px;margin-bottom:10px;}
.tip-title{font-size:13px;font-weight:700;color:#fff;margin-bottom:4px;}
.tip-body{font-size:12px;color:rgba(255,255,255,.45);line-height:1.65;}

.market-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:12px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:14px 18px;margin-bottom:8px;align-items:center;}
.m-crop{font-size:14px;font-weight:700;color:#fff;}
.m-unit{font-size:11px;color:rgba(255,255,255,.35);}
.m-price{font-size:17px;font-weight:800;color:#4ade80;}
.m-chg{font-size:12px;font-weight:700;}
.m-up{color:#4ade80;}.m-dn{color:#f87171;}.m-flat{color:rgba(255,255,255,.3);}

.cal-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;}
.cal-m{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:12px 8px;text-align:center;}
.cal-m.now{background:rgba(74,222,128,.08);border-color:rgba(74,222,128,.3);}
.cal-m.boro{border-top:3px solid #f59e0b;}
.cal-m.aman{border-top:3px solid #4ade80;}
.cal-m.aus{border-top:3px solid #22d3ee;}
.cal-mn{font-size:12px;font-weight:700;color:rgba(255,255,255,.55);}
.cal-sn{font-size:10px;margin-top:4px;font-weight:700;}

.chat-shell{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);border-radius:20px;overflow:hidden;}
.chat-head{background:rgba(0,106,78,.18);border-bottom:1px solid rgba(74,222,128,.1);padding:14px 18px;display:flex;align-items:center;gap:12px;}
.bot-av{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#006a4e,#00853f);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;box-shadow:0 4px 16px rgba(0,106,78,.4);}
.bot-name{font-size:14px;font-weight:800;color:#fff;}
.bot-status{font-size:11px;color:#4ade80;}
.chat-msgs{padding:18px;height:430px;overflow-y:auto;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth;}
.chat-msgs::-webkit-scrollbar{width:4px;}
.chat-msgs::-webkit-scrollbar-thumb{background:rgba(74,222,128,.18);border-radius:2px;}
.msg-row{display:flex;align-items:flex-end;gap:8px;}
.msg-row.user{flex-direction:row-reverse;}
.msg-av{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.msg-av.bot{background:linear-gradient(135deg,#006a4e,#00853f);}
.msg-av.usr{background:linear-gradient(135deg,#1e40af,#3b82f6);}
.msg-bub{max-width:74%;padding:12px 16px;border-radius:18px;font-size:13px;line-height:1.75;}
.msg-bub.bot{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.09);color:rgba(255,255,255,.85);border-radius:4px 18px 18px 18px;}
.msg-bub.usr{background:linear-gradient(135deg,#006a4e,#00853f);color:#fff;border-radius:18px 18px 4px 18px;box-shadow:0 4px 16px rgba(0,106,78,.3);}
.src-tag{display:inline-flex;align-items:center;gap:4px;background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.2);border-radius:8px;padding:3px 9px;font-size:10px;color:#4ade80;font-weight:700;margin-top:7px;}

.result-card{border-radius:20px;padding:26px;position:relative;overflow:hidden;}
.result-card.healthy{background:linear-gradient(135deg,rgba(22,163,74,.14),rgba(74,222,128,.06));border:1px solid rgba(74,222,128,.22);}
.result-card.warn{background:linear-gradient(135deg,rgba(234,179,8,.14),rgba(251,191,36,.06));border:1px solid rgba(251,191,36,.22);}
.result-card.danger{background:linear-gradient(135deg,rgba(244,42,65,.14),rgba(239,68,68,.06));border:1px solid rgba(239,68,68,.22);}
.r-head{font-size:19px;font-weight:800;color:#fff;margin-bottom:6px;}
.r-sub{font-size:13px;color:rgba(255,255,255,.45);margin-bottom:16px;}
.badge-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px;}
.badge{display:inline-flex;align-items:center;gap:4px;border-radius:20px;padding:5px 13px;font-size:11px;font-weight:700;}
.b-green{background:rgba(74,222,128,.13);color:#4ade80;}
.b-yellow{background:rgba(251,191,36,.13);color:#fbbf24;}
.b-red{background:rgba(239,68,68,.13);color:#f87171;}
.b-blue{background:rgba(96,165,250,.13);color:#60a5fa;}

.upload-zone{border:2px dashed rgba(74,222,128,.22);border-radius:20px;padding:44px 28px;text-align:center;background:rgba(74,222,128,.025);transition:all .2s;min-height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.upload-zone:hover{border-color:rgba(74,222,128,.45);background:rgba(74,222,128,.05);}

.helpline{background:linear-gradient(135deg,rgba(0,106,78,.14),rgba(0,133,63,.07));border:1px solid rgba(74,222,128,.14);border-radius:16px;padding:18px 22px;display:flex;align-items:center;gap:16px;margin-top:20px;}
.hl-num{font-size:28px;font-weight:900;color:#4ade80;letter-spacing:-1px;}

.tri{height:3px;background:linear-gradient(90deg,#006a4e 0%,#006a4e 30%,#f42a41 30%,#f42a41 45%,#de2910 55%,#de2910 70%,#ffde00 70%,#ffde00 85%,#1565c0 85%,#1565c0 100%);border-radius:2px;margin:18px 0;}

.admin-banner{background:linear-gradient(135deg,#0a0a0a,#140005,#0a0505);border-bottom:1px solid rgba(244,42,65,.18);padding:22px 32px;display:flex;align-items:center;justify-content:space-between;}
.admin-kpi{background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:18px;text-align:center;}
.admin-kpi-val{font-size:28px;font-weight:800;line-height:1;}
.admin-kpi-lbl{font-size:10px;color:rgba(255,255,255,.3);margin-top:5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}

.stTextInput>div>div>input{background:rgba(255,255,255,.055)!important;border:1px solid rgba(255,255,255,.11)!important;border-radius:12px!important;color:#fff!important;font-size:14px!important;padding:11px 15px!important;}
.stTextInput>div>div>input:focus{border-color:rgba(74,222,128,.4)!important;box-shadow:0 0 0 3px rgba(74,222,128,.07)!important;outline:none!important;}
.stTextInput>div>div>input::placeholder{color:rgba(255,255,255,.22)!important;}
.stButton>button{border-radius:12px!important;font-weight:700!important;font-size:13px!important;transition:all .2s!important;font-family:inherit!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#006a4e,#00853f)!important;border:none!important;color:#fff!important;box-shadow:0 4px 20px rgba(0,106,78,.28)!important;}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;box-shadow:0 8px 28px rgba(0,106,78,.4)!important;}
.stButton>button:not([kind="primary"]){background:rgba(255,255,255,.055)!important;border:1px solid rgba(255,255,255,.11)!important;color:rgba(255,255,255,.65)!important;}
.stButton>button:not([kind="primary"]):hover{background:rgba(255,255,255,.09)!important;color:#fff!important;}
.stSelectbox>div>div{background:rgba(255,255,255,.055)!important;border:1px solid rgba(255,255,255,.11)!important;border-radius:12px!important;color:#fff!important;}
.stRadio>div>label{color:rgba(255,255,255,.65)!important;font-size:13px!important;}
div[data-testid="stForm"]{border:none!important;padding:0!important;}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,255,255,.035)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;}
.stTabs [data-baseweb="tab"]{color:rgba(255,255,255,.45)!important;border-radius:8px!important;font-weight:700!important;}
.stTabs [aria-selected="true"]{background:rgba(74,222,128,.13)!important;color:#4ade80!important;}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.09);border-radius:4px;}
@keyframes fade-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.animate-in{animation:fade-in .45s ease forwards;}
</style>""", unsafe_allow_html=True)

# ─── helpers ───
LANG_LABELS = {"bn": "🇧🇩 বাংলা", "zh": "🇨🇳 中文", "en": "🇬🇧 English"}
def switch_lang(l): st.session_state.lang = l; st.rerun()
def go(page): st.session_state.page = page; st.rerun()

def topbar_html(user_name="", is_admin=False):
    badge = ""
    if user_name:
        role = "🔐 Admin" if is_admin else f"👨‍🌾 {user_name}"
        badge = f'<div class="ubadge"><div class="udot"></div><span>{role}</span></div>'
    return f"""<div class="topbar">
        <div class="t-brand">
            <div class="t-logo">🌾</div>
            <div><div class="t-name">Edge-Agri</div><div class="t-sub">Agricultural AI v4</div></div>
        </div>
        <div class="t-right">{badge}</div>
    </div>"""

def get_weather(district):
    D = {
        "চট্টগ্রাম":{"t":31,"f":36,"h":78,"w":14,"c":"Partly Cloudy","i":"⛅"},
        "Chittagong":{"t":31,"f":36,"h":78,"w":14,"c":"Partly Cloudy","i":"⛅"},
        "ঢাকা":{"t":33,"f":39,"h":72,"w":10,"c":"Sunny","i":"☀️"},
        "Dhaka":{"t":33,"f":39,"h":72,"w":10,"c":"Sunny","i":"☀️"},
        "সিলেট":{"t":28,"f":32,"h":85,"w":8,"c":"Rainy","i":"🌧️"},
        "Sylhet":{"t":28,"f":32,"h":85,"w":8,"c":"Rainy","i":"🌧️"},
        "রাজশাহী":{"t":35,"f":41,"h":60,"w":12,"c":"Hot & Sunny","i":"🌞"},
        "Rajshahi":{"t":35,"f":41,"h":60,"w":12,"c":"Hot & Sunny","i":"🌞"},
        "বরিশাল":{"t":30,"f":35,"h":80,"w":11,"c":"Cloudy","i":"☁️"},
        "Barishal":{"t":30,"f":35,"h":80,"w":11,"c":"Cloudy","i":"☁️"},
        "রংপুর":{"t":29,"f":33,"h":75,"w":13,"c":"Partly Cloudy","i":"⛅"},
        "Rangpur":{"t":29,"f":33,"h":75,"w":13,"c":"Partly Cloudy","i":"⛅"},
    }
    return D.get(district, {"t":30,"f":35,"h":75,"w":12,"c":"Partly Cloudy","i":"⛅"})

def get_market_prices(lc):
    D = {
        "bn":[
            ("🌾 ধান (সাধারণ)","প্রতি মণ","৳৯২০","+২.৫%",True),
            ("🌾 ধান (BRRI 28)","প্রতি মণ","৳১০৮০","+১.২%",True),
            ("🥔 আলু","প্রতি কেজি","৳৩৫","-০.৮%",False),
            ("🌶️ মরিচ","প্রতি কেজি","৳১৮০","+৫.৩%",True),
            ("🧅 পেঁয়াজ","প্রতি কেজি","৳৬৫","+১.৮%",True),
            ("🌽 ভুট্টা","প্রতি মণ","৳৭৪০","+৩.১%",True),
            ("🍅 টমেটো","প্রতি কেজি","৳৪৫","-২.৩%",False),
            ("🥬 বাঁধাকপি","প্রতি কেজি","৳২৮","০.০%",None),
        ],
        "en":[
            ("🌾 Rice (Common)","per maund","৳920","+2.5%",True),
            ("🌾 Rice (BRRI 28)","per maund","৳1080","+1.2%",True),
            ("🥔 Potato","per kg","৳35","-0.8%",False),
            ("🌶️ Chili","per kg","৳180","+5.3%",True),
            ("🧅 Onion","per kg","৳65","+1.8%",True),
            ("🌽 Corn","per maund","৳740","+3.1%",True),
            ("🍅 Tomato","per kg","৳45","-2.3%",False),
            ("🥬 Cabbage","per kg","৳28","0.0%",None),
        ],
        "zh":[
            ("🌾 大米 (普通)","每马温","৳920","+2.5%",True),
            ("🌾 大米 (BRRI 28)","每马温","৳1080","+1.2%",True),
            ("🥔 土豆","每公斤","৳35","-0.8%",False),
            ("🌶️ 辣椒","每公斤","৳180","+5.3%",True),
            ("🧅 洋葱","每公斤","৳65","+1.8%",True),
            ("🌽 玉米","每马温","৳740","+3.1%",True),
            ("🍅 西红柿","每公斤","৳45","-2.3%",False),
            ("🥬 卷心菜","每公斤","৳28","0.0%",None),
        ],
    }
    return D.get(lc, D["en"])

CAL = {
    "bn":{"Jan":("শীত","boro"),"Feb":("শীত","boro"),"Mar":("বোরো","boro"),"Apr":("বোরো","boro"),
          "May":("আউশ","aus"),"Jun":("আউশ","aus"),"Jul":("আউশ","aus"),"Aug":("আমন","aman"),
          "Sep":("আমন","aman"),"Oct":("আমন","aman"),"Nov":("আমন","aman"),"Dec":("শীত","boro")},
    "en":{"Jan":("Winter","boro"),"Feb":("Winter","boro"),"Mar":("Boro","boro"),"Apr":("Boro","boro"),
          "May":("Aus","aus"),"Jun":("Aus","aus"),"Jul":("Aus","aus"),"Aug":("Aman","aman"),
          "Sep":("Aman","aman"),"Oct":("Aman","aman"),"Nov":("Aman","aman"),"Dec":("Winter","boro")},
    "zh":{"Jan":("冬季","boro"),"Feb":("冬季","boro"),"Mar":("博罗","boro"),"Apr":("博罗","boro"),
          "May":("阿乌什","aus"),"Jun":("阿乌什","aus"),"Jul":("阿乌什","aus"),"Aug":("阿曼","aman"),
          "Sep":("阿曼","aman"),"Oct":("阿曼","aman"),"Nov":("阿曼","aman"),"Dec":("冬季","boro")},
}

TIPS = {
    "bn":{
        "aman":[("আমন ধানের যত্ন","কুশি পর্যায়ে সঠিক সার ও সেচ নিশ্চিত করুন। মাজরা পোকার জন্য ফেরোমন ট্র্যাপ ব্যবহার করুন।"),
                ("আগাছা দমন","রোপণের ২০-২৫ দিনের মধ্যে আগাছা পরিষ্কার করুন।"),
                ("AWD সেচ পদ্ধতি","জমিতে ৫ সেমি পানি থাকলে সেচ দেবেন না। শুকালে ২-৩ সেমি দিন।")],
        "boro":[("বোরো বীজতলা","নভেম্বর-ডিসেম্বরে বীজতলা তৈরি করুন। BRRI dhan28 বা dhan29 জাত নিন।"),
                ("শৈত্য প্রবাহ","রাতে পলিথিন দিয়ে বীজতলা ঢেকে দিন। দিনে খুলে দিন।"),
                ("ইউরিয়া প্রয়োগ","তিন ভাগে দিন: রোপণের ১০ দিন পর, কুশি ও থোড় অবস্থায়।")],
        "aus":[("আউশ ধান বপন","এপ্রিল-মে মাসে বীজ বপন করুন। সরাসরি বপন পদ্ধতি অনুসরণ করুন।"),
               ("খরা মোকাবেলা","AWD পদ্ধতিতে সেচ দিন। মাটিতে ফাটল দেখা দিলে সেচ দিন।"),
               ("ব্লাস্ট প্রতিরোধ","শীষ বের হওয়ার ৫-১০ দিন আগে ট্রাইসাইক্লাজোল স্প্রে করুন।")],
    },
    "en":{
        "aman":[("Aman Rice Care","Ensure proper fertilization at tillering. Use pheromone traps for stem borer."),
                ("Weed Management","Clear weeds within 20-25 days of transplanting."),
                ("AWD Irrigation","Don't irrigate if 5cm water remains. Add 2-3cm when dry.")],
        "boro":[("Boro Seedbed","Prepare seedbed in Nov-Dec. Use BRRI dhan28 or dhan29."),
                ("Cold Wave","Cover seedbed with polythene at night. Remove during sunny days."),
                ("Urea Application","Apply in 3 splits: 10 days after transplant, at tillering, at panicle.")],
        "aus":[("Aus Sowing","Sow seeds in April-May. Follow direct seeding method."),
               ("Drought Management","Use AWD irrigation. Apply water when soil cracks appear."),
               ("Blast Prevention","Spray Tricyclazole 5-10 days before heading.")],
    },
    "zh":{
        "aman":[("阿曼水稻管理","分蘖期确保适当施肥。使用信息素诱捕器防治螟虫。"),
                ("除草管理","移栽后20-25天内清除杂草。"),
                ("AWD灌溉","田间有5厘米水时不要灌溉。干旱时加2-3厘米水。")],
        "boro":[("博罗苗床","11-12月准备苗床。使用BRRI dhan28或dhan29品种。"),
                ("防寒管理","夜间用聚乙烯薄膜覆盖苗床。晴天时掀开。"),
                ("尿素施用","分3次施用：移栽后10天、分蘖期和穗分化期。")],
        "aus":[("阿乌什播种","4-5月播种。遵循直播方法。"),
               ("抗旱管理","使用AWD灌溉。出现裂缝时补水。"),
               ("稻瘟病预防","抽穗前5-10天喷施三环唑。")],
    },
}

def voice_component(lang_code="bn-BD"):
    import streamlit.components.v1 as components
    start_txt = "মাইক চালু করুন" if lang_code=="bn-BD" else ("开始录音" if lang_code=="zh-CN" else "Start Recording")
    speak_txt = "কথা বলুন..." if lang_code=="bn-BD" else ("请说话..." if lang_code=="zh-CN" else "Speak now...")
    use_txt   = "এই টেক্সট ব্যবহার করুন" if lang_code=="bn-BD" else ("使用此文本" if lang_code=="zh-CN" else "Use This Text")
    html = f"""
    <div style="display:flex;flex-direction:column;gap:10px;">
      <button id="mb" onclick="tM()" style="background:linear-gradient(135deg,#006a4e,#00853f);color:#fff;border:none;border-radius:12px;padding:12px 22px;font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:8px;font-family:inherit;width:fit-content;">🎤 <span id="bt">{start_txt}</span></button>
      <div id="wav" style="display:none;height:38px;background:rgba(74,222,128,.09);border-radius:10px;border:1px solid rgba(74,222,128,.22);overflow:hidden;"><div id="wb" style="display:flex;align-items:center;gap:2px;padding:4px 10px;height:100%;"></div></div>
      <div id="tr" style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:13px;font-size:13px;color:rgba(255,255,255,.65);min-height:48px;font-family:inherit;line-height:1.6;">{speak_txt}</div>
      <button id="ub" onclick="uT()" disabled style="background:rgba(255,255,255,.06);color:rgba(255,255,255,.28);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:10px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;">✓ {use_txt}</button>
    </div>
    <script>
    let r=null,rec=false,ft='',wi=null;
    function sW(){{document.getElementById('wav').style.display='block';wi=setInterval(()=>{{document.getElementById('wb').innerHTML=Array.from({{length:18}},()=>`<div style="width:4px;height:${{Math.random()*28+6}}px;background:rgba(74,222,128,.7);border-radius:2px;transition:height .15s;"></div>`).join('');}},150);}}
    function eW(){{clearInterval(wi);document.getElementById('wav').style.display='none';}}
    function tM(){{
      if(rec){{r&&r.stop();return;}}
      const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
      if(!SR){{document.getElementById('tr').innerText='Browser not supported. Use Chrome.';return;}}
      r=new SR();r.lang='{lang_code}';r.continuous=true;r.interimResults=true;
      r.onstart=()=>{{rec=true;document.getElementById('bt').innerText='⏹ Stop';document.getElementById('mb').style.background='linear-gradient(135deg,#f42a41,#c8102e)';sW();}};
      r.onresult=(e)=>{{let it='';for(let i=e.resultIndex;i<e.results.length;i++){{if(e.results[i].isFinal)ft+=e.results[i][0].transcript;else it+=e.results[i][0].transcript;}}document.getElementById('tr').innerText=(ft+it)||'...';if(ft){{document.getElementById('ub').disabled=false;document.getElementById('ub').style.background='linear-gradient(135deg,#006a4e,#00853f)';document.getElementById('ub').style.color='#fff';}}}};
      r.onend=()=>{{rec=false;document.getElementById('bt').innerText='🎤 {start_txt}';document.getElementById('mb').style.background='linear-gradient(135deg,#006a4e,#00853f)';eW();}};
      r.start();
    }}
    function uT(){{
      const txt=document.getElementById('tr').innerText;
      window.parent.postMessage({{type:'voice_result',text:txt}},'*');
      const u=new URL(window.parent.location);u.searchParams.set('voice',encodeURIComponent(txt));window.parent.history.replaceState(null,'',u);
      setTimeout(()=>{{const b=window.parent.document.querySelectorAll('[data-testid="stButton"] button');b.forEach(x=>{{if(x.innerText.includes('__voice__'))x.click();}});}},100);
    }}
    </script>"""
    components.html(html, height=220)

# ════════════════════════════════════════════════════════════════
# LANDING
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown(topbar_html(), unsafe_allow_html=True)
    lc1,lc2,lc3,_ = st.columns([1,1,1,6])
    with lc1:
        if st.button("🇧🇩 বাংলা",key="lb"): switch_lang("bn")
    with lc2:
        if st.button("🇨🇳 中文",key="lz"): switch_lang("zh")
    with lc3:
        if st.button("🇬🇧 EN",key="le"): switch_lang("en")

    H = {
        "bn":("কৃষি AI বিপ্লব","আপনার মাঠে, আপনার ভাষায়","বাংলাদেশের কৃষকদের জন্য প্রথম অফলাইন AI পরামর্শ সিস্টেম। ভয়েস, টেক্সট বা ছবি দিয়ে BRRI-অনুমোদিত পরামর্শ পান — ইন্টারনেট ছাড়াই।"),
        "zh":("农业AI革命","在您的田间，用您的语言","孟加拉国首个离线AI农业咨询系统。通过语音、文字或图片获取BRRI认证建议——无需互联网。"),
        "en":("Agricultural AI Revolution","In Your Field, In Your Language","Bangladesh's first offline AI advisory for smallholder farmers. Get BRRI-validated advice via voice, text or image — no internet needed."),
    }
    EY = {"bn":"🏆 বাংলাদেশের #১ কৃষি AI","zh":"🏆 孟加拉国 #1 农业AI","en":"🏆 Bangladesh's #1 Agricultural AI"}
    BG = {
        "bn":["📶 সম্পূর্ণ অফলাইন","🤖 RAG AI পরামর্শ","🎤 আঞ্চলিক ভাষা","🌾 BRRI অনুমোদিত","🔬 রোগ শনাক্তকরণ","📊 বাজার মূল্য","🗓️ ফসল ক্যালেন্ডার"],
        "zh":["📶 完全离线","🤖 RAG AI建议","🎤 方言识别","🌾 BRRI认证","🔬 病害检测","📊 市场价格","🗓️ 作物日历"],
        "en":["📶 Fully Offline","🤖 RAG AI Advice","🎤 Dialect Voice","🌾 BRRI Validated","🔬 Disease Detection","📊 Market Prices","🗓️ Crop Calendar"],
    }
    PD = {
        "bn":("কৃষক পোর্টাল","AI চ্যাটবট, রোগ শনাক্তকরণ, বাজার মূল্য ও মৌসুম ক্যালেন্ডার","👨‍🌾 প্রবেশ করুন",
              "অ্যাডমিন পোর্টাল","সিস্টেম ব্যবস্থাপনা ও জ্ঞানভাণ্ডার পরিচালনা","🔐 অ্যাডমিন লগইন"),
        "zh":("农民门户","AI聊天机器人、病害检测、市场价格和季节日历","👨‍🌾 进入",
              "管理员门户","系统管理和知识库管理","🔐 管理员登录"),
        "en":("Farmer Portal","AI chatbot, disease detection, market prices & seasonal calendar","👨‍🌾 Enter",
              "Admin Portal","System management & knowledge base administration","🔐 Admin Login"),
    }
    h1,h2,h3 = H.get(lang,H["en"])
    badges = "".join(f'<span class="flag-pill">{b}</span>' for b in BG.get(lang,BG["en"]))
    ft,fd,fb,at,ad,ab = PD.get(lang,PD["en"])
    stats = get_stats()
    SL = {"bn":["মোট প্রশ্ন","জ্ঞানভাণ্ডার","রোগ শনাক্ত","ভাষা"],
          "zh":["总查询","知识库","检测次数","语言"],
          "en":["Queries","KB Entries","Detections","Languages"]}
    sl = SL.get(lang,SL["en"])

    st.markdown(f"""
    <style>.stApp>[data-testid="stAppViewContainer"]>[data-testid="stMain"]{{background:radial-gradient(ellipse at 15% 25%,rgba(0,106,78,.28) 0%,transparent 50%),radial-gradient(ellipse at 85% 75%,rgba(0,106,78,.16) 0%,transparent 50%),linear-gradient(160deg,#040c06 0%,#070f08 100%)!important;}}</style>
    <div class="hero-wrap"><div class="hero-grid-bg"></div>
    <div style="text-align:center;position:relative;z-index:1;max-width:820px;width:100%;">
        <div class="eyebrow">{EY.get(lang)}</div>
        <h1 class="hero-h1"><span class="hero-accent">{h1}</span></h1>
        <h2 style="font-size:clamp(15px,2.5vw,24px);font-weight:400;color:rgba(255,255,255,.4);margin:0 0 14px;">{h2}</h2>
        <p class="hero-sub">{h3}</p>
        <div class="flags-row">{badges}</div>
        <div style="display:flex;gap:14px;justify-content:center;margin-bottom:8px;">
            <span style="font-size:28px;">🇧🇩</span><span style="font-size:28px;">🇨🇳</span><span style="font-size:28px;">🇬🇧</span>
        </div>
    </div></div>""", unsafe_allow_html=True)

    _,col,_ = st.columns([1,2.2,1])
    with col:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="portal-card farmer"><div class="p-icon">👨‍🌾</div><div class="p-title">{ft}</div><div class="p-desc">{fd}</div></div>', unsafe_allow_html=True)
            if st.button(fb,key="go_farmer",use_container_width=True,type="primary"): go("user_login")
        with c2:
            st.markdown(f'<div class="portal-card admin"><div class="p-icon">🔐</div><div class="p-title">{at}</div><div class="p-desc">{ad}</div></div>', unsafe_allow_html=True)
            if st.button(ab,key="go_admin",use_container_width=True): go("admin_login")

    st.markdown(f"""
    <div class="stats-strip animate-in">
        <div class="stat-pill"><div class="stat-num">{stats['total_queries']}</div><div class="stat-lbl">{sl[0]}</div></div>
        <div class="stat-pill"><div class="stat-num">{stats['kb_count']}</div><div class="stat-lbl">{sl[1]}</div></div>
        <div class="stat-pill"><div class="stat-num">{stats['detections']}</div><div class="stat-lbl">{sl[2]}</div></div>
        <div class="stat-pill"><div class="stat-num">3</div><div class="stat-lbl">{sl[3]}</div></div>
    </div>
    <div style="text-align:center;color:rgba(255,255,255,.15);font-size:10px;padding:20px;letter-spacing:1px;">
        EDGE-AGRI v4 &nbsp;·&nbsp; BRRI KNOWLEDGE BASE &nbsp;·&nbsp; RAG ENGINE &nbsp;·&nbsp; PLANTVISION AI &nbsp;·&nbsp; DIALECT ASR &nbsp;·&nbsp; OFFLINE READY
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# USER LOGIN
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "user_login":
    st.markdown(topbar_html(), unsafe_allow_html=True)
    if st.button("← "+{"bn":"পেছনে","zh":"返回","en":"Back"}.get(lang,"Back"),key="back_ul"): go("landing")
    st.markdown(f"""<style>.stApp>[data-testid="stAppViewContainer"]>[data-testid="stMain"]{{background:radial-gradient(ellipse at 30% 35%,rgba(0,106,78,.2) 0%,transparent 60%),linear-gradient(160deg,#040c06 0%,#070e08 100%)!important;}}</style>""",unsafe_allow_html=True)
    L = {
        "bn":("👨‍🌾 কৃষক পোর্টাল","আপনার তথ্য দিন — কোনো পাসওয়ার্ড লাগবে না","আপনার নাম","আপনার জেলা","প্রবেশ করুন →"),
        "zh":("👨‍🌾 农民门户","输入您的信息——无需密码","您的姓名","您的地区","进入 →"),
        "en":("👨‍🌾 Farmer Portal","Enter your details — no password required","Your Name","Your District","Enter →"),
    }
    tl,ts,tn,td,tbtn = L.get(lang,L["en"])
    DO = {
        "bn":["চট্টগ্রাম","ঢাকা","সিলেট","রাজশাহী","বরিশাল","রংপুর","খুলনা","ময়মনসিংহ","কুমিল্লা","নোয়াখালী","ফেনী","লক্ষ্মীপুর","চাঁদপুর","ব্রাহ্মণবাড়িয়া","বান্দরবান","রাঙামাটি","খাগড়াছড়ি"],
        "zh":["吉大港","达卡","锡尔赫特","拉杰沙希","巴里萨尔","朗布尔","库尔纳","迈门辛","库米拉","诺阿卡利"],
        "en":["Chittagong","Dhaka","Sylhet","Rajshahi","Barishal","Rangpur","Khulna","Mymensingh","Cumilla","Noakhali","Feni","Lakshmipur","Chandpur","Brahmanbaria","Bandarban","Rangamati","Khagrachhari"],
    }
    st.markdown("<br><br>",unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.1,1])
    with col:
        st.markdown(f'<div class="auth-card animate-in"><div class="auth-head farmer"><div class="auth-icon farmer">🌾</div><div class="auth-title">{tl}</div><div class="auth-sub">{ts}</div></div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        with st.form("ulform"):
            name = st.text_input(f"👤 {tn}",placeholder={"bn":"যেমন: রহিম উদ্দিন","zh":"例如：张三","en":"e.g. John Rahman"}.get(lang))
            dist = st.selectbox(f"📍 {td}",DO.get(lang,DO["en"]))
            if st.form_submit_button(tbtn,use_container_width=True,type="primary"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.user_district = dist
                    st.session_state.chat_history = []
                    go("user_home")
                else:
                    st.error({"bn":"নাম লিখুন","zh":"请输入姓名","en":"Please enter your name"}.get(lang))

# ════════════════════════════════════════════════════════════════
# USER HOME
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "user_home":
    from utils.rag_engine import answer_query, QUICK_QUESTIONS
    uname = st.session_state.user_name
    udist = st.session_state.user_district
    active_tab = st.session_state.user_tab
    TL = {
        "bn":{"dashboard":"🏠 ড্যাশবোর্ড","chat":"💬 চ্যাটবট","detect":"🔬 রোগ শনাক্তকরণ","market":"📊 বাজার মূল্য","calendar":"🗓️ ফসল ক্যালেন্ডার"},
        "zh":{"dashboard":"🏠 仪表板","chat":"💬 聊天机器人","detect":"🔬 病害检测","market":"📊 市场价格","calendar":"🗓️ 作物日历"},
        "en":{"dashboard":"🏠 Dashboard","chat":"💬 Chatbot","detect":"🔬 Disease Detection","market":"📊 Market Prices","calendar":"🗓️ Crop Calendar"},
    }
    tabs = TL.get(lang,TL["en"])
    st.markdown(topbar_html(user_name=uname),unsafe_allow_html=True)

    nc = st.columns([1,1,1,1,1,1,1,1,2])
    tkeys = list(tabs.keys())
    for i,k in enumerate(tkeys):
        with nc[i]:
            if st.button(tabs[k],key=f"tab_{k}"): st.session_state.user_tab=k; st.rerun()
    with nc[5]:
        if st.button("🇧🇩",key="ub"): switch_lang("bn")
    with nc[6]:
        if st.button("🇨🇳",key="uz"): switch_lang("zh")
    with nc[7]:
        if st.button("🇬🇧",key="ue"): switch_lang("en")
    with nc[8]:
        lo_lbl = {"bn":"🚪 লগআউট","zh":"🚪 退出","en":"🚪 Logout"}.get(lang)
        if st.button(lo_lbl,key="ulogout"): st.session_state.user_name=""; go("landing")

    gw = {"bn":"স্বাগতম","zh":"欢迎","en":"Welcome"}.get(lang)
    sn = {"bn":"কৃষি পরামর্শ সিস্টেম","zh":"农业咨询系统","en":"Agricultural Advisory System"}.get(lang)
    today = datetime.datetime.now().strftime("%d %B %Y")
    tab_html_parts = []
    for i,(k,v) in enumerate(tabs.items()):
        active_cls = " active" if k==active_tab else ""
        tab_html_parts.append(f'<button class="tab-btn{active_cls}" onclick="document.querySelectorAll(\'[data-testid=stButton] button\')[{i}].click()">{v}</button>')
    tab_html = "".join(tab_html_parts)
    st.markdown(f"""
    <div style="margin-top:62px;">
        <div class="user-strip">
            <div>
                <div class="u-greet">{gw}, {uname} 👋</div>
                <div style="margin-top:7px;display:flex;gap:10px;align-items:center;">
                    <span class="u-loc">📍 {udist}</span>
                    <span style="color:rgba(255,255,255,.28);font-size:12px;">{today}</span>
                </div>
            </div>
            <div style="color:rgba(255,255,255,.25);font-size:11px;text-align:right;">Edge-Agri v4<br>{sn}</div>
        </div>
        <div class="tab-bar">{tab_html}</div>
    </div>""",unsafe_allow_html=True)

    st.markdown('<div class="content">',unsafe_allow_html=True)

    # ── DASHBOARD ──
    if active_tab == "dashboard":
        stats = get_stats()
        weather = get_weather(udist)
        nm = datetime.datetime.now().strftime("%b")
        cal_data = CAL.get(lang,CAL["en"])
        sname,skey = cal_data.get(nm,("","aman"))
        KL = {"bn":["মোট প্রশ্ন","BRRI জ্ঞানভাণ্ডার","রোগ শনাক্ত","ভাষা"],
              "zh":["总查询","知识库","检测","语言"],
              "en":["Total Queries","KB Entries","Detections","Languages"]}
        kl = KL.get(lang,KL["en"])
        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card green"><div class="kpi-icon">💬</div><div class="kpi-val">{stats['total_queries']}</div><div class="kpi-lbl">{kl[0]}</div><div class="kpi-trend up">↑ +{stats.get('today_queries',0)} today</div></div>
            <div class="kpi-card red"><div class="kpi-icon">📚</div><div class="kpi-val">{stats['kb_count']}</div><div class="kpi-lbl">{kl[1]}</div><div class="kpi-trend stable">BRRI 2024</div></div>
            <div class="kpi-card gold"><div class="kpi-icon">🔬</div><div class="kpi-val">{stats['detections']}</div><div class="kpi-lbl">{kl[2]}</div><div class="kpi-trend up">14 plants</div></div>
            <div class="kpi-card blue"><div class="kpi-icon">🌐</div><div class="kpi-val">3</div><div class="kpi-lbl">{kl[3]}</div><div class="kpi-trend stable">বাংলা · 中文 · EN</div></div>
        </div>""",unsafe_allow_html=True)

        cw,cs = st.columns(2)
        with cw:
            fl = {"bn":"আর্দ্রতা","zh":"湿度","en":"Humidity"}.get(lang)
            wl = {"bn":"বায়ু","zh":"风速","en":"Wind"}.get(lang)
            wt = {"bn":"আবহাওয়া","zh":"天气","en":"Weather"}.get(lang)
            fe = {"bn":"অনুভূত","zh":"体感","en":"Feels"}.get(lang)
            st.markdown(f"""
            <div class="sec-title">🌤️ {wt} — {udist}</div>
            <div class="weather-card">
                <div class="w-icon">{weather['i']}</div>
                <div>
                    <div class="w-temp">{weather['t']}°C</div>
                    <div style="color:rgba(255,255,255,.4);font-size:12px;">{fe} {weather['f']}°C</div>
                    <div class="w-detail">
                        <div class="w-stat"><strong>{weather['h']}%</strong>{fl}</div>
                        <div class="w-stat"><strong>{weather['w']} km/h</strong>{wl}</div>
                    </div>
                </div>
                <div style="margin-left:auto;text-align:right;">
                    <div style="color:#fff;font-size:13px;font-weight:700;">{weather['c']}</div>
                    <div style="color:rgba(255,255,255,.28);font-size:11px;margin-top:4px;">{today}</div>
                </div>
            </div>""",unsafe_allow_html=True)

        with cs:
            se_lbl = {"bn":"চলতি মৌসুম","zh":"当前季节","en":"Current Season"}.get(lang)
            si = "🌿" if skey=="aman" else ("☀️" if skey=="aus" else "❄️")
            cc = "healthy" if skey=="aman" else ("warn" if skey=="aus" else "danger")
            st.markdown(f"""
            <div class="sec-title">🌾 {se_lbl}</div>
            <div class="result-card {cc}" style="text-align:center;padding:28px;">
                <div style="font-size:48px;margin-bottom:10px;">{si}</div>
                <div class="r-head">{sname}</div>
                <div style="color:rgba(255,255,255,.4);font-size:13px;">{nm} Season</div>
            </div>""",unsafe_allow_html=True)

        tt = {"bn":"মৌসুমি পরামর্শ","zh":"季节性建议","en":"Seasonal Tips"}.get(lang)
        st.markdown(f"<br><div class='sec-title'>💡 {tt}</div>",unsafe_allow_html=True)
        lt = TIPS.get(lang,TIPS["en"])
        for title,body in lt.get(skey,lt.get("aman",[])):
            st.markdown(f'<div class="tip-card"><div class="tip-title">📌 {title}</div><div class="tip-body">{body}</div></div>',unsafe_allow_html=True)

        ft2 = {"bn":"দ্রুত অ্যাক্সেস","zh":"快速访问","en":"Quick Access"}.get(lang)
        st.markdown(f"<br><div class='sec-title'>⚡ {ft2}</div>",unsafe_allow_html=True)
        FD = {
            "bn":[("💬","AI চ্যাটবট","BRRI জ্ঞানভাণ্ডার থেকে তাৎক্ষণিক পরামর্শ","chat"),
                  ("🔬","রোগ শনাক্তকরণ","গাছের ছবি দিয়ে রোগ চিনুন","detect"),
                  ("📊","বাজার মূল্য","আজকের ধান ও সবজির দাম","market")],
            "zh":[("💬","AI聊天机器人","从BRRI知识库获取即时建议","chat"),
                  ("🔬","病害检测","通过植物图片识别病害","detect"),
                  ("📊","市场价格","今日农产品价格","market")],
            "en":[("💬","AI Chatbot","Instant advice from BRRI knowledge base","chat"),
                  ("🔬","Disease Detection","Identify diseases from plant photos","detect"),
                  ("📊","Market Prices","Today's crop prices","market")],
        }
        fc1,fc2,fc3 = st.columns(3)
        for col,(icon,title,desc,tk) in zip([fc1,fc2,fc3],FD.get(lang,FD["en"])):
            with col:
                st.markdown(f'<div class="feat-card"><div class="fc-icon">{icon}</div><div class="fc-title">{title}</div><div class="fc-desc">{desc}</div><div class="fc-arrow">→</div></div>',unsafe_allow_html=True)
                if st.button(f"→ {title}",key=f"feat_{tk}",use_container_width=True):
                    st.session_state.user_tab=tk; st.rerun()

        hl_t = {"bn":"কৃষি হেল্পলাইন","zh":"农业热线","en":"Agricultural Helpline"}.get(lang)
        hl_h = {"bn":"সোম–শুক্র | সকাল ৮টা–বিকাল ৫টা | বিনামূল্যে","zh":"周一至周五 8AM-5PM | 免费","en":"Mon–Fri | 8AM–5PM | Free"}.get(lang)
        st.markdown(f'<div class="helpline"><span style="font-size:34px;">📞</span><div><div style="font-size:11px;color:rgba(255,255,255,.45);font-weight:700;text-transform:uppercase;letter-spacing:.5px;">{hl_t}</div><div class="hl-num">16123</div><div style="font-size:11px;color:rgba(255,255,255,.3);">{hl_h}</div></div></div>',unsafe_allow_html=True)

    # ── CHATBOT ──
    elif active_tab == "chat":
        ct = {"bn":"💬 কৃষি AI চ্যাটবট","zh":"💬 农业AI聊天机器人","en":"💬 Agricultural AI Chatbot"}.get(lang)
        st.markdown(f'<div class="sec-title">{ct}<span class="sec-sub">BRRI Knowledge Base · RAG Engine</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="tri"></div>',unsafe_allow_html=True)

        cc,cs2 = st.columns([3,1])
        with cs2:
            qq_t = {"bn":"⚡ দ্রুত প্রশ্ন","zh":"⚡ 快速提问","en":"⚡ Quick Questions"}.get(lang)
            st.markdown(f'<div style="font-size:12px;font-weight:700;color:rgba(255,255,255,.4);margin-bottom:10px;">{qq_t}</div>',unsafe_allow_html=True)
            for q in QUICK_QUESTIONS.get(lang,QUICK_QUESTIONS["en"]):
                if st.button(f"↗ {q[:36]}{"…" if len(q)>36 else ""}",key=f"qq_{q[:14]}",use_container_width=True):
                    st.session_state.chat_history.append({"role":"user","text":q})
                    r = answer_query(q,lang,udist)
                    st.session_state.chat_history.append({"role":"bot","text":r["answer"],"source":r.get("source",""),"confidence":r.get("confidence",0),"related":r.get("related",[])})
                    st.rerun()
            st.markdown("---")
            if st.button({"bn":"🗑️ চ্যাট মুছুন","zh":"🗑️ 清除","en":"🗑️ Clear Chat"}.get(lang),use_container_width=True,key="clearchat"):
                st.session_state.chat_history=[]; st.rerun()

        with cc:
            greet = {
                "bn":f"আসসালামুয়ালাইকুম {uname}! 🌾 আমি Edge-Agri AI। BRRI-অনুমোদিত পরামর্শ দিতে পারি। আপনার সমস্যা বলুন।",
                "zh":f"您好 {uname}！🌾 我是Edge-Agri AI。请告诉我您的农业问题。",
                "en":f"Hello {uname}! 🌾 I'm Edge-Agri AI. Share your farming problem and I'll give BRRI-validated advice.",
            }
            st.markdown('<div class="chat-shell"><div class="chat-head"><div class="bot-av">🤖</div><div><div class="bot-name">Edge-Agri AI</div><div class="bot-status">● Online · BRRI Knowledge Base</div></div></div></div>',unsafe_allow_html=True)
            msgs = '<div class="chat-msgs" id="cb">'
            if not st.session_state.chat_history:
                msgs += f'<div class="msg-row"><div class="msg-av bot">🤖</div><div class="msg-bub bot">{greet.get(lang,greet["en"])}</div></div>'
            for m in st.session_state.chat_history:
                if m["role"]=="user":
                    msgs += f'<div class="msg-row user"><div class="msg-av usr">👤</div><div class="msg-bub usr">{m["text"]}</div></div>'
                else:
                    src = f'<div class="src-tag">📖 {m["source"]} · {int(m.get("confidence",0)*100)}%</div>' if m.get("source") else ""
                    msgs += f'<div class="msg-row"><div class="msg-av bot">🤖</div><div class="msg-bub bot">{m["text"]}{src}</div></div>'
            msgs += '<div id="ce"></div></div><script>document.getElementById("ce")?.scrollIntoView({behavior:"smooth"});</script>'
            st.markdown(msgs,unsafe_allow_html=True)

            if st.session_state.chat_history and st.session_state.chat_history[-1].get("related"):
                related = st.session_state.chat_history[-1]["related"]
                rc = st.columns(min(len(related),3))
                for ci,rq in enumerate(related[:3]):
                    with rc[ci]:
                        if st.button(rq[:30],key=f"rq_{rq[:10]}"):
                            st.session_state.chat_history.append({"role":"user","text":rq})
                            res = answer_query(rq,lang,udist)
                            st.session_state.chat_history.append({"role":"bot","text":res["answer"],"source":res.get("source",""),"confidence":res.get("confidence",0),"related":res.get("related",[])})
                            st.rerun()

            im = st.radio({"bn":"ইনপুট","zh":"输入","en":"Input"}.get(lang),
                [{"bn":"✍️ টেক্সট","zh":"✍️ 文字","en":"✍️ Text"}.get(lang),
                 {"bn":"🖼️ ছবি","zh":"🖼️ 图片","en":"🖼️ Image"}.get(lang),
                 {"bn":"🎤 ভয়েস","zh":"🎤 语音","en":"🎤 Voice"}.get(lang)],
                horizontal=True,key="imr",label_visibility="collapsed")

            if "টেক্সট" in im or "Text" in im or "文字" in im:
                with st.form("chatf",clear_on_submit=True):
                    ci2,cb2 = st.columns([5,1])
                    with ci2:
                        ui = st.text_input("q",placeholder={"bn":"প্রশ্ন লিখুন...","zh":"输入问题...","en":"Type your question..."}.get(lang),label_visibility="collapsed")
                    with cb2:
                        sent = st.form_submit_button({"bn":"পাঠান ➤","zh":"发送 ➤","en":"Send ➤"}.get(lang),use_container_width=True,type="primary")
                if sent and ui.strip():
                    st.session_state.chat_history.append({"role":"user","text":ui})
                    res = answer_query(ui,lang,udist)
                    st.session_state.chat_history.append({"role":"bot","text":res["answer"],"source":res.get("source",""),"confidence":res.get("confidence",0),"related":res.get("related",[])})
                    st.rerun()
            elif "ছবি" in im or "Image" in im or "图片" in im:
                iup = st.file_uploader({"bn":"ফসলের ছবি আপলোড","zh":"上传作物图片","en":"Upload crop image"}.get(lang),type=["jpg","jpeg","png","webp"],key="cimg")
                if iup:
                    cpv,cq = st.columns([1,2])
                    with cpv: st.image(iup,use_container_width=True)
                    with cq:
                        iq = st.text_input("iq",placeholder={"bn":"ছবি সম্পর্কে প্রশ্ন...","zh":"关于图片...","en":"Question about image..."}.get(lang),label_visibility="collapsed")
                        if st.button({"bn":"🔍 পরামর্শ নিন","zh":"🔍 获取建议","en":"🔍 Get Advice"}.get(lang),key="isend",type="primary"):
                            q2 = iq if iq.strip() else {"bn":"এই ফসলের সমস্যা কী?","zh":"这种作物有什么问题？","en":"What's the problem with this crop?"}.get(lang)
                            st.session_state.chat_history.append({"role":"user","text":f"[🖼️] {q2}"})
                            res = answer_query(q2,lang,udist)
                            st.session_state.chat_history.append({"role":"bot","text":res["answer"],"source":res.get("source",""),"confidence":res.get("confidence",0),"related":res.get("related",[])})
                            st.rerun()
            else:
                voice_component({"bn":"bn-BD","zh":"zh-CN","en":"en-US"}.get(lang,"bn-BD"))
                st.caption({"bn":"💡 Chrome browser এ ভয়েস সবচেয়ে ভালো কাজ করে","zh":"💡 Chrome浏览器语音效果最佳","en":"💡 Voice works best in Chrome browser"}.get(lang))

    # ── DISEASE DETECTION ──
    elif active_tab == "detect":
        from utils.disease_detector import predict_disease
        dt = {"bn":"🔬 উদ্ভিদ রোগ শনাক্তকরণ","zh":"🔬 植物病害检测","en":"🔬 Plant Disease Detection"}.get(lang)
        ds = {"bn":"PlantVision AI · ১৪ ধরনের উদ্ভিদ · ৩৮টি রোগ","zh":"PlantVision AI · 14种植物 · 38种病害","en":"PlantVision AI · 14 Plant Types · 38 Diseases"}.get(lang)
        st.markdown(f'<div class="sec-title">{dt}<span class="sec-sub">{ds}</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="tri"></div>',unsafe_allow_html=True)

        d1,d2 = st.columns([1,1.1])
        with d1:
            up = st.file_uploader({"bn":"📷 উদ্ভিদের পাতার ছবি আপলোড করুন","zh":"📷 上传植物叶片图片","en":"📷 Upload Plant Leaf Image"}.get(lang),type=["jpg","jpeg","png","webp"],key="dimg")
            if not up:
                st.markdown(f'<div class="upload-zone"><div style="font-size:60px;opacity:.5;margin-bottom:14px;">🌿</div><div style="font-size:15px;font-weight:700;color:rgba(255,255,255,.6);margin-bottom:6px;">{"ছবি ড্র্যাগ করুন বা ক্লিক করুন" if lang=="bn" else ("拖放或点击上传" if lang=="zh" else "Drag & drop or click to upload")}</div><div style="font-size:12px;color:rgba(255,255,255,.28);">JPG · PNG · WEBP · max 10MB</div></div>',unsafe_allow_html=True)
            else:
                img = Image.open(up)
                st.image(img,use_container_width=True,caption=up.name)
                db = {"bn":"🔬 রোগ শনাক্ত করুন","zh":"🔬 检测病害","en":"🔬 Analyze Disease"}.get(lang)
                if st.button(db,type="primary",use_container_width=True,key="dbtn"):
                    with st.spinner({"bn":"AI বিশ্লেষণ করছে...","zh":"AI分析中...","en":"AI analyzing..."}.get(lang)):
                        result = predict_disease(img,lang)
                    st.session_state.last_detection = result
                    from utils.database import log_detection
                    log_detection(up.name,result["plant_type"],result["disease"],result["confidence"],result["severity"],result["recommendation"])
                    st.rerun()
            with st.expander({"bn":"🌱 সমর্থিত উদ্ভিদ (১৪ ধরন)","zh":"🌱 支持植物（14种）","en":"🌱 Supported Plants (14 types)"}.get(lang)):
                plants = ["🍎 Apple","🫐 Blueberry","🍒 Cherry","🌽 Corn","🍇 Grape","🍊 Orange","🍑 Peach","🌶️ Pepper","🥔 Potato","🍓 Strawberry","🍅 Tomato","🌱 Soybean","🫑 Squash","🌿 Raspberry"]
                pc = st.columns(2)
                for i,p in enumerate(plants): pc[i%2].markdown(f"<small style='color:rgba(255,255,255,.45);'>{p}</small>",unsafe_allow_html=True)

        with d2:
            res = st.session_state.last_detection
            rl = {"bn":"📋 শনাক্তকরণ ফলাফল","zh":"📋 检测结果","en":"📋 Detection Result"}.get(lang)
            if res:
                st.markdown(f'<div class="sec-title">{rl}</div>',unsafe_allow_html=True)
                if res["is_healthy"]:
                    hl = {"bn":"সুস্থ উদ্ভিদ","zh":"健康植物","en":"Healthy Plant"}.get(lang)
                    cl = {"bn":"নিশ্চিততা","zh":"置信度","en":"Confidence"}.get(lang)
                    st.markdown(f'<div class="result-card healthy" style="text-align:center;padding:34px;"><div style="font-size:68px;margin-bottom:10px;">✅</div><div class="r-head" style="color:#4ade80;">{hl}</div><div class="r-sub">🌿 {res["plant_type"]}</div><div class="badge-row" style="justify-content:center;"><span class="badge b-green">{cl}: {res["confidence_pct"]}</span></div></div>',unsafe_allow_html=True)
                else:
                    sv = res["severity"]
                    cc2 = "danger" if sv=="High" else "warn"
                    bc = "b-red" if sv=="High" else "b-yellow"
                    pl = {"bn":"উদ্ভিদ","zh":"植物","en":"Plant"}.get(lang)
                    sl2 = {"bn":"তীব্রতা","zh":"严重程度","en":"Severity"}.get(lang)
                    cl2 = {"bn":"নিশ্চিততা","zh":"置信度","en":"Confidence"}.get(lang)
                    st.markdown(f'<div class="result-card {cc2}"><div style="font-size:10px;color:rgba(255,255,255,.35);margin-bottom:5px;font-weight:700;text-transform:uppercase;">{pl}: {res["plant_type"]}</div><div class="r-head">⚠️ {res["disease_display"]}</div><div class="r-sub">{res["disease"]}</div><div class="badge-row"><span class="badge {bc}">{sl2}: {res["severity_display"]}</span><span class="badge b-blue">{cl2}: {res["confidence_pct"]}</span></div></div>',unsafe_allow_html=True)
                if res.get("symptoms"):
                    symL = {"bn":"🔍 লক্ষণ","zh":"🔍 症状","en":"🔍 Symptoms"}.get(lang)
                    st.markdown(f"<br>**{symL}:**",unsafe_allow_html=True)
                    st.info(res["symptoms"])
                rL = {"bn":"💊 প্রতিকার ও পরামর্শ","zh":"💊 防治建议","en":"💊 Treatment & Recommendation"}.get(lang)
                st.markdown(f"**{rL}:**")
                st.success(res["recommendation"])
            else:
                st.markdown('<div style="text-align:center;padding:80px 20px;color:rgba(255,255,255,.12);"><div style="font-size:90px;margin-bottom:14px;">🌿</div><div style="font-size:15px;font-weight:600;">Upload an image to start</div><div style="font-size:12px;margin-top:6px;opacity:.6;">PlantVision AI identifies 38 disease classes</div></div>',unsafe_allow_html=True)

    # ── MARKET PRICES ──
    elif active_tab == "market":
        mt = {"bn":"📊 আজকের কৃষি বাজার মূল্য","zh":"📊 今日农业市场价格","en":"📊 Today's Agricultural Market Prices"}.get(lang)
        ms = {"bn":"সূত্র: কৃষি বিপণন অধিদপ্তর | আজ আপডেট","zh":"来源：农业营销局 | 今日更新","en":"Source: Dept. of Agricultural Marketing | Updated today"}.get(lang)
        st.markdown(f'<div class="sec-title">{mt}<span class="sec-sub">{ms}</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="tri"></div>',unsafe_allow_html=True)
        ch = {"bn":"ফসল","zh":"作物","en":"Crop"}.get(lang)
        uh = {"bn":"একক","zh":"单位","en":"Unit"}.get(lang)
        ph = {"bn":"মূল্য","zh":"价格","en":"Price"}.get(lang)
        xh = {"bn":"পরিবর্তন","zh":"变化","en":"Change"}.get(lang)
        st.markdown(f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:12px;padding:0 18px;margin-bottom:10px;"><div style="font-size:10px;font-weight:800;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:.5px;">{ch}</div><div style="font-size:10px;font-weight:800;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:.5px;">{uh}</div><div style="font-size:10px;font-weight:800;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:.5px;">{ph}</div><div style="font-size:10px;font-weight:800;color:rgba(255,255,255,.28);text-transform:uppercase;letter-spacing:.5px;">{xh}</div></div>',unsafe_allow_html=True)
        for crop,unit,price,change,is_up in get_market_prices(lang):
            cc3 = "m-up" if is_up else ("m-dn" if is_up is False else "m-flat")
            ci3 = "↑" if is_up else ("↓" if is_up is False else "→")
            st.markdown(f'<div class="market-row"><div class="m-crop">{crop}</div><div class="m-unit">{unit}</div><div class="m-price">{price}</div><div class="m-chg {cc3}">{ci3} {change}</div></div>',unsafe_allow_html=True)
        note = {"bn":"⚠️ দাম পরিবর্তনশীল। সঠিক দামের জন্য স্থানীয় বাজারে যোগাযোগ করুন।","zh":"⚠️ 价格可能变动。请联系当地市场。","en":"⚠️ Prices may vary. Contact your local market for accuracy."}.get(lang)
        st.markdown(f"<br><div style='font-size:11px;color:rgba(255,255,255,.22);'>{note}</div>",unsafe_allow_html=True)

    # ── CROP CALENDAR ──
    elif active_tab == "calendar":
        calt = {"bn":"🗓️ বাংলাদেশ ফসল মৌসুম ক্যালেন্ডার","zh":"🗓️ 孟加拉国作物季节日历","en":"🗓️ Bangladesh Crop Season Calendar"}.get(lang)
        cals = {"bn":"বোরো · আমন · আউশ ধানের মৌসুম","zh":"博罗·阿曼·阿乌什水稻季节","en":"Boro · Aman · Aus Rice Seasons"}.get(lang)
        st.markdown(f'<div class="sec-title">{calt}<span class="sec-sub">{cals}</span></div>',unsafe_allow_html=True)
        st.markdown('<div class="tri"></div>',unsafe_allow_html=True)
        cd = CAL.get(lang,CAL["en"])
        nm2 = datetime.datetime.now().strftime("%b")
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        sc = {"boro":"#f59e0b","aman":"#4ade80","aus":"#22d3ee"}
        cal_html = '<div class="cal-grid">'
        for m in months:
            sn2,sk2 = cd.get(m,("",""))
            clr = sc.get(sk2,"#fff")
            is_now = m==nm2
            cal_html += f'<div class="cal-m {sk2} {"now" if is_now else ""}"><div class="cal-mn" style="color:{"#fff" if is_now else "rgba(255,255,255,.5)"};">{m}</div><div class="cal-sn" style="color:{clr};">{sn2}</div>{"<div style='font-size:9px;color:#4ade80;margin-top:2px;'>◀ Now</div>" if is_now else ""}</div>'
        cal_html += '</div>'
        st.markdown(cal_html,unsafe_allow_html=True)

        leg_t = {"bn":"মৌসুম সূচক","zh":"季节图例","en":"Season Legend"}.get(lang)
        st.markdown(f"<br><div class='sec-title'>{leg_t}</div>",unsafe_allow_html=True)
        LEG = {
            "bn":[("🟡 বোরো","নভেম্বর–এপ্রিল","শীত মৌসুম। উচ্চ ফলনশীল। সেচ নির্ভর।"),
                  ("🟢 আমন","আগস্ট–নভেম্বর","বর্ষা মৌসুম। বৃষ্টিনির্ভর। প্রধান ফসল।"),
                  ("🔵 আউশ","মে–আগস্ট","গ্রীষ্ম মৌসুম। খরা সহনশীল জাত।")],
            "en":[("🟡 Boro","November–April","Winter season. High yield. Irrigation-dependent."),
                  ("🟢 Aman","August–November","Monsoon season. Rain-fed. Main crop."),
                  ("🔵 Aus","May–August","Summer season. Drought-tolerant varieties.")],
            "zh":[("🟡 博罗","11月–4月","冬季。高产。依赖灌溉。"),
                  ("🟢 阿曼","8月–11月","雨季。雨养。主要作物。"),
                  ("🔵 阿乌什","5月–8月","夏季。耐旱品种。")],
        }
        for inm,period,desc in LEG.get(lang,LEG["en"]):
            st.markdown(f'<div class="tip-card"><div class="tip-title">{inm} &nbsp;<span style="font-weight:400;color:rgba(255,255,255,.32);">{period}</span></div><div class="tip-body">{desc}</div></div>',unsafe_allow_html=True)

        vt = {"bn":"🌾 প্রস্তাবিত BRRI জাত","zh":"🌾 推荐BRRI品种","en":"🌾 Recommended BRRI Varieties"}.get(lang)
        st.markdown(f"<br><div class='sec-title'>{vt}</div>",unsafe_allow_html=True)
        VD = {
            "bn":[("বোরো","BRRI dhan28<br>BRRI dhan29<br>BRRI dhan81<br>BRRI dhan92"),
                  ("আমন","BRRI dhan49<br>BRRI dhan52<br>BRRI dhan87<br>BRRI dhan95"),
                  ("আউশ","BRRI dhan48<br>BR14 · BR16<br>BRRI dhan65")],
            "en":[("Boro","BRRI dhan28<br>BRRI dhan29<br>BRRI dhan81<br>BRRI dhan92"),
                  ("Aman","BRRI dhan49<br>BRRI dhan52<br>BRRI dhan87<br>BRRI dhan95"),
                  ("Aus","BRRI dhan48<br>BR14 · BR16<br>BRRI dhan65")],
            "zh":[("博罗","BRRI dhan28<br>BRRI dhan29<br>BRRI dhan81<br>BRRI dhan92"),
                  ("阿曼","BRRI dhan49<br>BRRI dhan52<br>BRRI dhan87<br>BRRI dhan95"),
                  ("阿乌什","BRRI dhan48<br>BR14 · BR16<br>BRRI dhan65")],
        }
        vc1,vc2,vc3 = st.columns(3)
        for col,(sn3,var) in zip([vc1,vc2,vc3],VD.get(lang,VD["en"])):
            with col:
                st.markdown(f'<div class="kpi-card green" style="text-align:center;padding:18px;"><div style="font-size:13px;font-weight:800;color:#fff;margin-bottom:10px;">🌾 {sn3}</div><div style="font-size:11px;color:rgba(255,255,255,.4);line-height:1.8;">{var}</div></div>',unsafe_allow_html=True)

    st.markdown('</div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# ADMIN LOGIN
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin_login":
    # সঠিক Indentation (৪টি স্পেস ডানে)
    from utils.database import verify_admin
    
    st.markdown(topbar_html(), unsafe_allow_html=True)
    
    if st.button("← Back", key="back_al"): 
        st.session_state.page = "landing"
        st.rerun()
        
    st.markdown('<style>.stApp>[data-testid="stAppViewContainer"]>[data-testid="stMain"]{background:radial-gradient(ellipse at 50% 30%,rgba(200,16,46,.14) 0%,transparent 60%),linear-gradient(160deg,#090406 0%,#0c0507 100%)!important;}</style>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown('<div class="auth-card animate-in"><div class="auth-head admin"><div class="auth-icon admin">🔐</div><div class="auth-title">Admin Portal</div><div class="auth-sub">Restricted — Administrators Only</div></div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("alf"):
            username = st.text_input("👤 Username", placeholder="admin")
            password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
            
            if st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary"):
                if verify_admin(username, password):
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_user = username
                    st.session_state.page = "admin_home" # go() এর বদলে সরাসরি স্টেট সেট করা নিরাপদ
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
                    
        st.caption("Default: admin / admin123")
# ════════════════════════════════════════════════════════════════
# ADMIN HOME
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin_home":
    # app.py এর ইমপোর্ট লাইনটি এভাবে আপডেট করুন:
from utils.database import get_stats, get_recent_queries, get_detections, get_kb_entries, add_kb_entry, delete_kb_entry
    import pandas as pd
    if not st.session_state.admin_logged_in: go("admin_login")
    st.markdown(topbar_html(user_name=st.session_state.get("admin_user","admin"),is_admin=True),unsafe_allow_html=True)
    _,lc2 = st.columns([9,1])
    with lc2:
        if st.button("🚪 Logout",key="alo"): st.session_state.admin_logged_in=False; go("landing")
    stats = get_stats()
    st.markdown(f"""
    <div style="margin-top:62px;">
        <div class="admin-banner">
            <div>
                <div style="font-size:21px;font-weight:800;color:#fff;">📊 Admin Dashboard</div>
                <div style="font-size:12px;color:rgba(255,255,255,.35);margin-top:3px;">Welcome, {st.session_state.get('admin_user','admin')} · Edge-Agri v4 System</div>
            </div>
            <div style="color:rgba(255,255,255,.2);font-size:10px;text-align:right;">Edge-Agri v4<br>{datetime.datetime.now().strftime('%d %b %Y %H:%M')}</div>
        </div>
    </div>""",unsafe_allow_html=True)
    st.markdown('<div style="padding:24px 32px;">',unsafe_allow_html=True)
    a1,a2,a3,a4 = st.columns(4)
    for col,val,lbl,clr in [(a1,stats["total_queries"],"Total Queries","#4ade80"),(a2,stats["today_queries"],"Today","#f42a41"),(a3,stats["kb_count"],"KB Entries","#f59e0b"),(a4,f'{stats["avg_confidence"]}%',"Avg Accuracy","#60a5fa")]:
        col.markdown(f'<div class="admin-kpi" style="border-top:3px solid {clr};"><div class="admin-kpi-val" style="color:{clr};">{val}</div><div class="admin-kpi-lbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    t1,t2,t3,t4 = st.tabs(["💬 Query Logs","🔬 Detection Logs","📚 Knowledge Base","➕ Add Entry"])
    with t1:
        qs = get_all_queries(500)
        if qs:
            df = pd.DataFrame(qs)[["id","query_text","query_lang","confidence_score","district","created_at"]]
            df.columns = ["#","Query","Lang","Confidence","District","Time"]
            df["Confidence"] = df["Confidence"].apply(lambda x: f"{round((x or 0)*100,1)}%")
            st.dataframe(df,use_container_width=True,hide_index=True)
        else: st.info("No queries yet.")
    with t2:
        ds2 = get_all_detections(500)
        if ds2:
            df2 = pd.DataFrame(ds2)[["id","image_name","plant_type","detected_disease","confidence","severity","created_at"]]
            df2.columns = ["#","Image","Plant","Disease","Confidence","Severity","Time"]
            df2["Confidence"] = df2["Confidence"].apply(lambda x: f"{round((x or 0)*100,1)}%")
            st.dataframe(df2,use_container_width=True,hide_index=True)
        else: st.info("No detections yet.")
    with t3:
        srch = st.text_input("🔍 Search",placeholder="Search knowledge base...")
        kb = get_all_kb()
        if srch: kb = [k for k in kb if srch.lower() in (k["question_bn"] or "").lower() or srch.lower() in (k.get("keywords") or "").lower()]
        st.caption(f"**{len(kb)}** entries")
        for item in kb:
            with st.expander(f"[{item['category']}] {item['question_bn'][:60]}…"):
                c1,c2 = st.columns([4,1])
                with c1:
                    st.write(f"**BN:** {item['answer_bn'][:250]}…")
                    if item.get('answer_en'): st.caption(f"EN: {item['answer_en'][:200]}…")
                    st.caption(f"Source: {item['source']} · KW: {item.get('keywords','')}")
                with c2:
                    if st.button("🗑️",key=f"del_{item['id']}"): delete_kb_entry(item["id"]); st.rerun()
    with t4:
        with st.form("addkb"):
            cats = ["ধানের রোগ","সার ব্যবস্থাপনা","পোকামাকড়","সেচ ব্যবস্থাপনা","আবহাওয়া ও মৌসুম","ফসল কাটা","মাটি পরীক্ষা","বীজ ব্যবস্থাপনা","জৈব চাষ","বাজার ও বিক্রয়","অন্যান্য"]
            e1,e2 = st.columns(2)
            with e1: cat = st.selectbox("Category *",cats); src = st.text_input("Source",value="BRRI Manual 2024")
            with e2: kw = st.text_input("Keywords",placeholder="blast,disease"); qen = st.text_input("Q (English)",placeholder="Optional")
            qbn = st.text_input("Question (বাংলা) *",placeholder="বাংলায় প্রশ্ন লিখুন...")
            abn = st.text_area("Answer (বাংলা) *",height=90,placeholder="বিস্তারিত উত্তর...")
            aen = st.text_area("Answer (English)",height=70,placeholder="Optional...")
            if st.form_submit_button("💾 Save Entry",type="primary",use_container_width=True):
                if qbn and abn: add_kb_entry(cat,qbn,abn,src,kw,qen,aen); st.success("✅ Saved!"); st.rerun()
                else: st.error("Bengali Q&A required!")
    st.markdown('</div>',unsafe_allow_html=True)
