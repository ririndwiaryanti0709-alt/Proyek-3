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
    --cobalt: #153EBD;
    --dark-cobalt: #102F91;
    --royal: #4169E1;
    --orange: #FF7A1A;
    --canvas: #F4F7FF;
    --white: #FFFFFF;
    --ink: #172344;
    --muted: #536487;
    --line: #D8E1F5;
}

/* ---------- Page foundation ---------- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: var(--canvas);
    color: var(--ink);
    font-size: 15px;
}
[data-testid="stHeader"] {
    background: rgba(244, 247, 255, 0.96);
}
[data-testid="stToolbar"] { right: 1.25rem; }
.main .block-container {
    max-width: 1420px;
    padding: 2rem 2.4rem 3rem;
}
h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.03em;
    color: var(--ink);
}
.main [data-testid="stMarkdownContainer"] p,
.main [data-testid="stCaptionContainer"] {
    color: #435273;
    line-height: 1.7;
    font-size: 14px;
}
a { color: var(--cobalt); }

/* Keep Streamlit columns aligned without forcing unrelated widgets to fixed sizes. */
[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}
[data-testid="stColumn"] {
    min-width: 0;
}

/* ---------- Sidebar base and readable copy ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102F91 0%, #153EBD 58%, #2349C3 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.18);
    color: #FFFFFF !important;
    font-size: 14px;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stCaption {
    color: #FFFFFF !important;
    opacity: 1 !important;
    font-size: 14px;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}

/* ---------- Sidebar brand and tip card ---------- */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 7px 5px 17px;
    margin: 0 0 9px;
    border-bottom: 1px solid rgba(255,255,255,0.25);
}
.brand-mark {
    display: grid;
    place-items: center;
    flex: 0 0 42px;
    width: 42px;
    height: 42px;
    border-radius: 13px;
    color: #FFFFFF;
    font-size: 21px;
    background: linear-gradient(135deg, #4169E1, #78A2FF);
    box-shadow: 0 5px 14px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.32);
}
.brand-name {
    font-family: 'Manrope', sans-serif;
    color: #FFFFFF !important;
    font-weight: 800;
    font-size: 15px;
    line-height: 1.22;
    letter-spacing: -0.02em;
}
.brand-sub {
    color: #E4ECFF !important;
    font-size: 10px !important;
    font-weight: 600;
    margin-top: 4px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.sidebar-tip {
    margin-top: 0.8rem;
    padding: 13px 14px;
    border-radius: 13px;
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}
.sidebar-tip strong {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 800;
}
.sidebar-tip p {
    color: #FFFFFF !important;
    font-size: 13px !important;
    line-height: 1.6;
    margin: 5px 0 0;
}

/* ---------- Sidebar navigation: blue active row + orange accent ---------- */
[data-testid="stSidebarNav"] { padding-top: 0.45rem; }
[data-testid="stSidebarNav"] a {
    border-radius: 9px;
    margin: 2px 8px;
    padding-top: 7px;
    padding-bottom: 7px;
    border-left: 3px solid transparent;
    transition: background 0.18s ease, border-color 0.18s ease;
}
[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a p {
    color: #FFFFFF !important;
    font-size: 14px !important;
    font-weight: 600;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.13) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(65,105,225,0.72) !important;
    border-left: 3px solid #FF7A1A !important;
    box-shadow: none !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] p {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* ---------- Sidebar uploader: white button with dark readable text ---------- */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    color: #FFFFFF !important;
    font-size: 13px;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.12) !important;
    border: 1px dashed rgba(255,255,255,0.82) !important;
    border-radius: 12px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stSidebar"] [data-testid="stFileUploader"] small {
    color: #FFFFFF !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #FFFFFF !important;
    color: #172344 !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
    min-height: 38px;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button,
[data-testid="stSidebar"] [data-testid="stFileUploader"] button span,
[data-testid="stSidebar"] [data-testid="stFileUploader"] button p,
[data-testid="stSidebar"] [data-testid="stFileUploader"] button svg,
[data-testid="stSidebar"] [data-testid="stFileUploader"] button * {
    color: #172344 !important;
    fill: #172344 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {
    background: #EAF0FF !important;
    border-color: #FF7A1A !important;
}

/* ---------- Sidebar select boxes and inputs ---------- */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div,
[data-testid="stSidebar"] [data-baseweb="textarea"] > div {
    background: #FFFFFF !important;
    border: 1px solid #8AB4FF !important;
    border-radius: 9px !important;
    min-height: 39px;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="input"] input,
[data-testid="stSidebar"] [data-baseweb="textarea"] textarea {
    color: #172344 !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #153EBD !important;
    color: #153EBD !important;
}
[data-baseweb="popover"] [role="option"] {
    background: #FFFFFF;
    color: #172344 !important;
    font-size: 14px !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background: #EAF0FF !important;
}
[data-testid="stSidebar"] input[type="number"],
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] textarea {
    background: #FFFFFF !important;
    color: #172344 !important;
    border-color: #8AB4FF !important;
    font-size: 13px !important;
}

/* ---------- Sidebar sliders: visible rail, thumb, and value ---------- */
[data-testid="stSidebar"] [data-testid="stSlider"] label,
[data-testid="stSidebar"] [data-testid="stSlider"] label *,
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}
/* Base rail / unselected section */
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    background-color: #A9C5FF !important;
    border-radius: 99px !important;
    min-height: 6px;
}
/* Selected range section */
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] > div:first-child > div,
[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[style*="left:"][style*="right:"] {
    background-color: #FF7A1A !important;
    border-radius: 99px !important;
}
/* Draggable circle */
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #FFFFFF !important;
    border: 3px solid #FF7A1A !important;
    box-shadow: 0 0 0 3px rgba(255,255,255,0.2) !important;
    width: 18px !important;
    height: 18px !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"]:focus {
    box-shadow: 0 0 0 4px rgba(138,180,255,0.65) !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
    background: #4169E1 !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 7px;
    padding: 2px 6px;
}

/* ---------- Sidebar checkbox / radio ---------- */
[data-testid="stSidebar"] [data-testid="stCheckbox"] label,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label *,
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label * {
    color: #FFFFFF !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] input[type="checkbox"],
[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #FF7A1A;
}

/* ---------- Buttons; make Run Experiment clearly visible ---------- */
.stButton > button,
.stDownloadButton > button,
[data-testid="stPageLink"] a {
    border: 1px solid transparent;
    border-radius: 11px;
    font-size: 14px !important;
    font-weight: 700 !important;
    min-height: 42px;
    padding: 0.58rem 1rem;
    background: var(--cobalt) !important;
    color: #FFFFFF !important;
    box-shadow: 0 5px 13px rgba(21,62,189,0.15);
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}
.stButton > button *,
.stDownloadButton > button *,
[data-testid="stPageLink"] a * { color: inherit !important; }
.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stPageLink"] a:hover {
    background: var(--orange) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 17px rgba(255,122,26,0.22);
}
.stButton > button:focus,
.stDownloadButton > button:focus {
    outline: 2px solid #8AB4FF !important;
    outline-offset: 2px;
}
[data-testid="stPageLink"] a {
    display: flex;
    justify-content: center;
    align-items: center;
    text-decoration: none;
}
/* Sidebar buttons: a brighter blue separates them from the sidebar */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stDownloadButton > button {
    background: #4169E1 !important;
    color: #FFFFFF !important;
    border: 1px solid #A9C5FF !important;
    min-height: 44px;
    box-shadow: 0 5px 14px rgba(0,0,0,0.16);
}
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] .stDownloadButton > button * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: #4169E1 !important;
    color: #FFFFFF !important;
    border: 2px solid #FFFFFF !important;
    box-shadow: 0 0 0 2px rgba(138,180,255,0.35), 0 6px 15px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stDownloadButton > button:hover {
    background: #FF7A1A !important;
    border-color: #FFFFFF !important;
}

/* ---------- Streamlit metrics and tables ---------- */
[data-testid="stMetric"] {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #FFFFFF;
    padding: 1rem 1.1rem;
    border: 1px solid var(--line);
    border-radius: 15px;
    box-shadow: 0 5px 16px rgba(32,61,125,0.045);
    min-height: 116px;
    height: 100%;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #536487 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricValue"] {
    color: var(--cobalt) !important;
    font-family: 'Manrope', sans-serif;
    font-size: 27px !important;
    font-weight: 800 !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 13px;
    overflow: hidden;
    background: #FFFFFF;
}
[data-testid="stDataFrame"] * { font-size: 13px; }

/* ---------- Alerts, expanders, tabs ---------- */
[data-testid="stAlert"] { border-radius: 13px; }
[data-testid="stAlert"] p { font-size: 14px; line-height: 1.65; }
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 13px;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #172344 !important;
    font-size: 14px !important;
    font-weight: 700;
}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
    color: #3E4D6D;
    font-size: 14px;
}
[data-testid="stTabs"] button { font-size: 14px !important; font-weight: 700 !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--cobalt) !important;
    border-bottom-color: var(--orange) !important;
}
[data-testid="stTabs"] button[aria-selected="false"] { color: #536487 !important; }
hr { border-color: var(--line); }

/* ---------- Hero section ---------- */
.hero-shell {
    position: relative;
    overflow: hidden;
    isolation: isolate;
    box-sizing: border-box;
    padding: 29px 31px;
    margin: 0 0 25px;
    min-height: 218px;
    border-radius: 23px;
    color: #FFFFFF;
    background: linear-gradient(118deg, #102F91 0%, #153EBD 59%, #4169E1 100%);
    box-shadow: 0 16px 36px rgba(16,47,145,0.16);
}
.hero-shell:before {
    content: '';
    z-index: -1;
    position: absolute;
    right: -57px;
    top: -135px;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.17);
    box-shadow: 0 0 0 28px rgba(255,255,255,0.04), 0 0 0 58px rgba(255,255,255,0.035);
}
.hero-shell:after {
    content: '';
    position: absolute;
    width: 120px;
    height: 120px;
    right: 17%;
    bottom: -82px;
    border-radius: 50%;
    background: rgba(255,122,26,0.92);
    z-index: -1;
}
.hero-topline {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #FFFFFF;
    font-size: 11px;
    letter-spacing: 0.13em;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-dot {
    width: 8px;
    height: 8px;
    flex: 0 0 8px;
    border-radius: 50%;
    background: #FF7A1A;
    box-shadow: 0 0 0 5px rgba(255,122,26,0.17);
}
.hero-shell h1 {
    color: #FFFFFF !important;
    font-size: clamp(29px,3.1vw,43px) !important;
    line-height: 1.15;
    font-weight: 800;
    margin: 0 0 12px;
    max-width: 760px;
}
.hero-shell p {
    color: #FFFFFF !important;
    margin: 0;
    line-height: 1.7;
    max-width: 720px;
    font-size: 15px;
}
.hero-icon {
    position: absolute;
    right: 32px;
    top: 32px;
    width: 68px;
    height: 68px;
    border-radius: 20px;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.24);
    font-size: 32px;
    backdrop-filter: blur(8px);
}

/* ---------- Section headings ---------- */
.section-kicker {
    color: var(--cobalt);
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 5px 0 7px;
}
.section-title {
    font-family: 'Manrope', sans-serif;
    color: var(--ink);
    font-size: 25px;
    line-height: 1.28;
    letter-spacing: -0.035em;
    font-weight: 800;
    margin: 0 0 8px;
}
.section-copy {
    color: #536487;
    font-size: 14px;
    line-height: 1.75;
    margin: 0 0 18px;
}

/* ---------- Summary cards: same baseline and height ---------- */
.mini-stat {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 138px;
    min-height: 138px;
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 15px;
    padding: 15px 16px 13px;
    box-shadow: 0 5px 16px rgba(32,61,125,0.04);
}
.mini-stat .stat-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    min-height: 29px;
    color: #536487;
    font-size: 11px;
    line-height: 1.35;
    font-weight: 800;
}
.mini-stat .stat-icon {
    display: grid;
    place-items: center;
    flex: 0 0 30px;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: #EAF0FF;
    color: #153EBD;
    font-size: 16px;
}
.mini-stat .stat-value {
    font-family: 'Manrope', sans-serif;
    color: #153EBD;
    font-size: 27px;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin-top: auto;
    padding-top: 5px;
}
.mini-stat .stat-note {
    color: #536487;
    font-size: 11px;
    line-height: 1.35;
    min-height: 27px;
    margin-top: 4px;
}

/* ---------- Workspace cards on the app home page ---------- */
.workspace-card {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    height: 326px;
    min-height: 326px;
    background: #FFFFFF;
    border: 1px solid #D8E1F5;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 23px rgba(27,55,112,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.workspace-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 27px rgba(27,55,112,0.09);
}
.workspace-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    min-height: 53px;
    margin-bottom: 13px;
}
.workspace-icon {
    display: grid;
    place-items: center;
    flex: 0 0 51px;
    width: 51px;
    height: 51px;
    border-radius: 16px;
    background: #EAF0FF;
    font-size: 25px;
}
.workspace-chip {
    display: inline-flex;
    align-items: center;
    max-width: 65%;
    padding: 5px 9px;
    border-radius: 99px;
    background: #FFF0E5;
    color: #A94300;
    font-size: 10px;
    line-height: 1.35;
    font-weight: 800;
    text-align: right;
    text-transform: uppercase;
}
.workspace-card h3 {
    min-height: 27px;
    font-size: 19px;
    line-height: 1.3;
    margin: 0 0 8px;
    font-weight: 800;
}
.workspace-card > p {
    color: #536487;
    font-size: 13px;
    line-height: 1.65;
    min-height: 82px;
    margin: 0 0 12px;
}
.pill-list {
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    gap: 6px;
    min-height: 48px;
    margin-top: auto;
    padding-top: 5px;
}
.pill {
    display: inline-flex;
    align-items: center;
    padding: 5px 8px;
    border-radius: 8px;
    background: #EAF0FF;
    color: #24469B;
    font-size: 10px;
    line-height: 1.35;
    font-weight: 800;
}
[data-testid="stPageLink"] a {
    width: 100%;
    min-height: 42px;
    margin-top: 10px;
}

/* ---------- Workflow cards: consistent height ---------- */
.workflow-step {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    height: 184px;
    min-height: 184px;
    background: rgba(255,255,255,0.92);
    border: 1px solid #D8E1F5;
    border-radius: 14px;
    padding: 15px 16px;
    box-shadow: 0 5px 13px rgba(27,55,112,0.035);
}
.workflow-num {
    color: #C85200;
    font-family: 'Manrope', sans-serif;
    font-size: 11px;
    line-height: 1.4;
    font-weight: 800;
    letter-spacing: 0.1em;
}
.workflow-step h4 {
    font-size: 15px;
    line-height: 1.35;
    min-height: 21px;
    margin: 7px 0 5px;
    font-weight: 800;
}
.workflow-step p {
    color: #536487;
    font-size: 12px;
    line-height: 1.55;
    margin: 0;
}

/* ---------- Feature / run / note cards ---------- */
.feature-card {
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 180px;
    background: #FFFFFF;
    border: 1px solid #D8E1F5;
    border-radius: 17px;
    padding: 20px;
    box-shadow: 0 7px 20px rgba(27,55,112,0.045);
}
.feature-icon {
    display: grid;
    place-items: center;
    width: 43px;
    height: 43px;
    border-radius: 13px;
    color: #153EBD;
    background: #EAF0FF;
    font-size: 21px;
    margin-bottom: 13px;
}
.feature-card h3 { font-size: 17px; margin: 0 0 7px; }
.feature-card p { color: #536487; font-size: 13px; line-height: 1.65; margin: 0; }
.soft-note {
    background: #EAF0FF;
    border: 1px solid #CAD8FF;
    border-radius: 13px;
    padding: 13px 15px;
    color: #293E70;
    font-size: 13px;
    line-height: 1.7;
}
.soft-note strong { color: #153EBD; }
.run-panel {
    box-sizing: border-box;
    height: 100%;
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 19px 20px;
    box-shadow: 0 7px 20px rgba(27,55,112,0.04);
}
.run-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    border-radius: 99px;
    padding: 7px 10px;
    background: #E2F7EB;
    color: #12663D;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.run-status span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #168B53;
}
.footer-note {
    color: #657493;
    font-size: 11px;
    text-align: center;
    padding: 22px 0 3px;
    letter-spacing: 0.03em;
}

/* ---------- Responsive sizing ---------- */
@media (max-width: 1100px) {
    .main .block-container { padding: 1.6rem 1.3rem 2.5rem; }
    .workspace-card { height: 350px; min-height: 350px; }
    .workspace-card > p { min-height: 105px; }
    .workflow-step { height: 200px; min-height: 200px; }
}
@media (max-width: 700px) {
    .main .block-container { padding: 1.15rem 0.85rem 2rem; }
    .hero-shell { padding: 22px 19px; min-height: 0; }
    .hero-icon { position: static; margin: 0 0 15px; width: 52px; height: 52px; font-size: 26px; }
    .hero-shell h1 { font-size: 29px !important; }
    .hero-shell p { font-size: 14px; }
    .section-title { font-size: 22px; }
    .workspace-card { height: auto; min-height: 0; padding: 19px; }
    .workspace-card > p { min-height: 0; }
    .pill-list { min-height: 0; margin-top: 10px; }
    .workflow-step { height: auto; min-height: 0; }
    .mini-stat { height: auto; min-height: 125px; }
}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
          <div class="brand-mark">✳</div>
          <div>
            <div class="brand-name">ML Experiment<br>Studio</div>
            <div class="brand-sub">Data science workspace</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-tip">
          <strong>✦ &nbsp; Explore with purpose</strong>
          <p>Unggah data, atur eksperimen, lalu baca hasilnya dalam satu workspace.</p>
        </div>
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
            f"""<div class="mini-stat">
                <div class="stat-top"><span>{escape(str(label))}</span><span class="stat-icon">{escape(str(icon))}</span></div>
                <div class="stat-value">{escape(str(value))}</div>
                <div class="stat-note">{escape(str(note))}</div>
            </div>""",
            unsafe_allow_html=True,
        )


def render_footer():
    st.markdown(
        '<div class="footer-note">ML EXPERIMENT STUDIO &nbsp;·&nbsp; BUILD INSIGHTFULLY &nbsp;·&nbsp; 2026</div>',
        unsafe_allow_html=True,
    )
