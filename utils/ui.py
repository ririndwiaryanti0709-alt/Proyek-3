"""Shared visual system for ML Experiment Studio."""
from html import escape
import streamlit as st


PALETTE = {
    "cobalt": "#153EBD",
    "dark": "#102F91",
    "royal": "#4169E1",
    "orange": "#FF7A1A",
    "background": "#F4F7FF",
    "white": "#FFFFFF",
}


def apply_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root {
          --cobalt: #153EBD; --dark-cobalt: #102F91; --royal: #4169E1;
          --orange: #FF7A1A; --canvas: #F4F7FF; --white: #FFFFFF;
          --ink: #172344; --muted: #7180A3; --line: #E4EAF8;
        }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp { background: var(--canvas); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(244,247,255,.82); }
        [data-testid="stToolbar"] { right: 1.25rem; }
        .main .block-container { max-width: 1420px; padding: 2.1rem 2.8rem 3rem; }
        @media (max-width: 900px) { .main .block-container { padding: 1.4rem 1rem 2.4rem; } }
        h1, h2, h3, h4 { font-family: 'Manrope', sans-serif !important; letter-spacing: -0.035em; color: var(--ink); }
        p, li, label { color: #4D5A79; }
        a { color: var(--cobalt); }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #102F91 0%, #153EBD 57%, #2349C3 100%); border-right: 0; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] small { color: rgba(255,255,255,.84) !important; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: white !important; }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section { background: rgba(255,255,255,.08); border: 1px dashed rgba(255,255,255,.35); }
        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div,
        [data-testid="stSidebar"] [data-baseweb="textarea"] > div { border-radius: 10px; }
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color: rgba(255,255,255,.9) !important; font-weight: 600; }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .8rem; }
        [data-testid="stSidebarNav"] { padding-top: .5rem; }
        [data-testid="stSidebarNav"] a { border-radius: 10px; margin: 2px 9px; }
        [data-testid="stSidebarNav"] a:hover { background: rgba(255,255,255,.12); }
        [data-testid="stSidebarNav"] span { color: white !important; }
        [data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(255,255,255,.17); border-left: 3px solid #FF7A1A; }
        .stButton > button, .stDownloadButton > button, [data-testid="stPageLink"] a {
          border: 0; border-radius: 12px; font-weight: 700; min-height: 2.75rem;
          background: var(--cobalt); color: white; box-shadow: 0 7px 16px rgba(21,62,189,.16);
          transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stPageLink"] a:hover {
          color: white; background: var(--orange); transform: translateY(-1px); box-shadow: 0 9px 20px rgba(255,122,26,.2);
        }
        .stButton > button:focus, .stDownloadButton > button:focus { box-shadow: 0 0 0 .2rem rgba(65,105,225,.22); }
        [data-testid="stPageLink"] a { display: flex; justify-content: center; align-items: center; padding: .55rem 1rem; text-decoration: none; }
        [data-testid="stMetric"] { background: white; padding: 1rem 1.15rem; border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 5px 18px rgba(32,61,125,.035); }
        [data-testid="stMetricLabel"] p { color: var(--muted); font-size: .82rem; font-weight: 700; }
        [data-testid="stMetricValue"] { color: var(--cobalt); font-family: 'Manrope',sans-serif; }
        [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }
        [data-testid="stAlert"] { border-radius: 14px; }
        [data-testid="stExpander"] { background: rgba(255,255,255,.78); border: 1px solid var(--line); border-radius: 14px; }
        [data-testid="stTabs"] button { font-weight: 700; }
        [data-testid="stTabs"] button[aria-selected="true"] { color: var(--cobalt); }
        hr { border-color: var(--line); }
        .sidebar-brand { display:flex; align-items:center; gap:11px; padding: 7px 5px 18px; margin: 0 0 9px; border-bottom: 1px solid rgba(255,255,255,.18); }
        .brand-mark { display:grid; place-items:center; width:42px; height:42px; border-radius:14px; color:#fff; font-size:21px; background:linear-gradient(135deg,#4169E1,#153EBD); box-shadow:0 7px 18px rgba(0,0,0,.12); border:1px solid rgba(255,255,255,.24); }
        .brand-name { font-family:'Manrope',sans-serif; color:white; font-weight:800; font-size:14px; line-height:1.18; letter-spacing:-.025em; }
        .brand-sub { color:rgba(255,255,255,.66); font-size:10px; margin-top:4px; letter-spacing:.12em; text-transform:uppercase; }
        .sidebar-tip { margin-top: 1.1rem; padding: 13px 14px; border-radius: 13px; background: rgba(255,255,255,.09); border: 1px solid rgba(255,255,255,.13); }
        .sidebar-tip strong { color:white; font-size:12px; }
        .sidebar-tip p { color:rgba(255,255,255,.73) !important; font-size:11px; line-height:1.55; margin:5px 0 0; }
        .hero-shell { position:relative; overflow:hidden; isolation:isolate; padding:28px 30px; margin:0 0 25px; min-height:218px; border-radius:24px; color:white; background:linear-gradient(118deg,#102F91 0%,#153EBD 59%,#4169E1 100%); box-shadow:0 17px 40px rgba(16,47,145,.17); }
        .hero-shell:before { content:''; z-index:-1; position:absolute; right:-57px; top:-135px; width:340px; height:340px; border-radius:50%; border:1px solid rgba(255,255,255,.17); box-shadow:0 0 0 28px rgba(255,255,255,.04),0 0 0 58px rgba(255,255,255,.035); }
        .hero-shell:after { content:''; position:absolute; width:120px;height:120px;right:17%;bottom:-82px;border-radius:50%;background:rgba(255,122,26,.9);filter:blur(1px);opacity:.9;z-index:-1; }
        .hero-topline { display:flex; align-items:center; gap:9px; color:rgba(255,255,255,.78); font-size:11px; letter-spacing:.15em; font-weight:800; text-transform:uppercase; margin-bottom:14px; }
        .hero-dot { width:7px;height:7px;border-radius:50%;background:#FF7A1A;box-shadow:0 0 0 5px rgba(255,122,26,.15); }
        .hero-shell h1 { color:white !important; font-size:clamp(29px,3.2vw,43px) !important; line-height:1.12; font-weight:800; margin:0 0 11px; max-width:760px; }
        .hero-shell p { color:rgba(255,255,255,.78) !important; margin:0; line-height:1.65; max-width:720px; font-size:14px; }
        .hero-icon { position:absolute; right:34px; top:34px; width:72px;height:72px;border-radius:22px; display:grid;place-items:center;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.2);font-size:34px;backdrop-filter:blur(8px); }
        .section-kicker { color:var(--cobalt); font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:.15em; margin:5px 0 6px; }
        .section-title { font-family:'Manrope',sans-serif; color:var(--ink); font-size:23px; line-height:1.2; letter-spacing:-.04em; font-weight:800; margin:0 0 7px; }
        .section-copy { color:var(--muted); font-size:13px; line-height:1.65; margin:0 0 17px; }
        .feature-card { position:relative; overflow:hidden; background:white; border:1px solid #E4EAF8; border-radius:19px; padding:21px 21px 19px; min-height:176px; box-shadow:0 8px 24px rgba(27,55,112,.045); }
        .feature-card:after { content:''; position:absolute; right:-30px; bottom:-50px; width:115px;height:115px;border-radius:50%; background:#F0F4FF; }
        .feature-icon { display:grid;place-items:center;width:43px;height:43px;border-radius:14px;color:#153EBD;background:#EDF2FF;font-size:22px;margin-bottom:17px; position:relative; z-index:1; }
        .feature-card h3 { font-size:16px; font-weight:800; margin:0 0 7px; position:relative;z-index:1; }
        .feature-card p { font-size:12px; line-height:1.65; color:#7180A3; margin:0; position:relative;z-index:1; }
        .mini-stat { background:#fff; border:1px solid var(--line); border-radius:16px; padding:15px 16px; box-shadow:0 5px 17px rgba(32,61,125,.035); min-height:94px; }
        .mini-stat .stat-top { display:flex;justify-content:space-between;align-items:center;gap:10px;color:#7180A3;font-size:11px;font-weight:700; }
        .mini-stat .stat-icon {display:grid;place-items:center;width:29px;height:29px;border-radius:9px;background:#EEF2FF;color:#153EBD;font-size:15px;}
        .mini-stat .stat-value { font-family:'Manrope',sans-serif; color:#153EBD; font-size:25px; font-weight:800; letter-spacing:-.04em; margin-top:7px; }
        .mini-stat .stat-note {font-size:10px;color:#8894B0;margin-top:1px;}
        .workspace-card { background:white;border:1px solid #E1E8F8;border-radius:22px;padding:23px; min-height:234px;box-shadow:0 9px 26px rgba(27,55,112,.05); }
        .workspace-head {display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:17px;}
        .workspace-icon {display:grid;place-items:center;width:53px;height:53px;border-radius:17px;background:#EDF2FF;font-size:26px;}
        .workspace-chip {display:inline-flex;padding:5px 9px;border-radius:99px;background:#FFF0E5;color:#C65B0B;font-size:10px;letter-spacing:.07em;font-weight:800;text-transform:uppercase;}
        .workspace-card h3 {font-size:19px;margin:0 0 7px;font-weight:800;}
        .workspace-card p {font-size:12px;line-height:1.7;color:#7180A3;margin:0 0 14px;}
        .pill-list {display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
        .pill {display:inline-flex;padding:5px 8px;border-radius:8px;background:#F3F6FF;color:#51628C;font-size:10px;font-weight:700;}
        .workflow-step { height:100%; background:rgba(255,255,255,.72);border:1px solid #E4EAF8;border-radius:15px;padding:15px 16px; }
        .workflow-num {color:#FF7A1A;font-family:'Manrope',sans-serif;font-size:11px;font-weight:800;letter-spacing:.12em;}
        .workflow-step h4 {font-size:14px;margin:7px 0 4px;font-weight:800;}
        .workflow-step p {font-size:11px;line-height:1.6;color:#7180A3;margin:0;}
        .soft-note { background:#EEF3FF;border:1px solid #DDE6FF;border-radius:14px;padding:13px 15px;color:#43557F;font-size:12px;line-height:1.65; }
        .soft-note strong {color:#153EBD;}
        .run-panel { background:white;border:1px solid var(--line);border-radius:18px;padding:20px 22px;box-shadow:0 8px 24px rgba(27,55,112,.035); }
        .run-status {display:inline-flex;align-items:center;gap:7px;border-radius:99px;padding:7px 10px;background:#E9F8EF;color:#187548;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.07em;}
        .run-status span {width:6px;height:6px;border-radius:50%;background:#22A566;}
        .footer-note { color:#91A0BC;font-size:10px;text-align:center;padding:22px 0 3px;letter-spacing:.04em; }
        @media(max-width:700px) { .hero-shell {padding:23px 20px;min-height:0;} .hero-icon {position:static;margin:0 0 17px;width:54px;height:54px;font-size:27px;} .hero-shell h1 {font-size:29px !important;} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
          <div class="brand-mark">✳</div>
          <div><div class="brand-name">ML Experiment<br>Studio</div><div class="brand-sub">Data science workspace</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-tip"><strong>✦ &nbsp; Explore with purpose</strong>
        <p>Unggah data, atur eksperimen, lalu baca hasilnya dalam satu workspace.</p></div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(eyebrow, title, description, icon="✳"):
    st.markdown(
        f"""<section class="hero-shell">
          <div class="hero-icon">{escape(str(icon))}</div>
          <div class="hero-topline"><span class="hero-dot"></span>{escape(str(eyebrow))}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </section>""",
        unsafe_allow_html=True,
    )


def render_section_heading(kicker, title, copy=None):
    safe_copy = f'<p class="section-copy">{escape(str(copy))}</p>' if copy else ""
    st.markdown(
        f'<div class="section-kicker">{escape(str(kicker))}</div><div class="section-title">{escape(str(title))}</div>{safe_copy}',
        unsafe_allow_html=True,
    )


def render_mini_stats(items):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        label, value, icon, note = item
        col.markdown(
            f"""<div class="mini-stat"><div class="stat-top"><span>{escape(str(label))}</span><span class="stat-icon">{escape(str(icon))}</span></div>
            <div class="stat-value">{escape(str(value))}</div><div class="stat-note">{escape(str(note))}</div></div>""",
            unsafe_allow_html=True,
        )


def render_footer():
    st.markdown('<div class="footer-note">ML EXPERIMENT STUDIO &nbsp;·&nbsp; BUILD INSIGHTFULLY &nbsp;·&nbsp; 2026</div>', unsafe_allow_html=True)
