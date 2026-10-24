from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ML Experiment Studio",
    page_icon="✳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.ui import apply_global_styles, render_sidebar_brand, render_hero, render_section_heading, render_mini_stats, render_footer

BASE_DIR = Path(__file__).resolve().parent

apply_global_styles()
render_sidebar_brand()

render_hero(
    "MACHINE LEARNING WORKSPACE  ·  2026",
    "Turn your data into <span style='color:#FFB37D'>clear insights.</span>",
    "Ruang eksperimen interaktif untuk menguji model, mengeksplorasi pola, dan memahami performa machine learning tanpa alur kerja yang berbelit.",
    "✳",
)

# Quick workspace overview
supervised_df = pd.read_csv(BASE_DIR / "data" / "dataset_supervised.csv")
unsupervised_df = pd.read_csv(BASE_DIR / "data" / "dataset_unsupervised.csv")
render_mini_stats([
    ("LEARNING MODES", "02", "◈", "Supervised & unsupervised"),
    ("ALGORITHMS", "04", "⌘", "RF · SVM · K-Means · DBSCAN"),
    ("SAMPLE DATASETS", "02", "▤", "Langsung bisa dieksplorasi"),
    ("VISUAL ANALYTICS", "LIVE", "↗", "Grafik dan metrik interaktif"),
])

st.write("")
render_section_heading("YOUR WORKSPACE", "Choose your experiment", "Pilih jalur analisis yang sesuai dengan pertanyaanmu. Setiap ruang menyediakan kontrol model dan hasil evaluasi yang bisa diunduh.")

left, right = st.columns(2, gap="large")
with left:
    st.markdown(
        """<div class="workspace-card">
          <div class="workspace-head"><div class="workspace-icon">🧠</div><span class="workspace-chip">Predictive</span></div>
          <h3>Supervised Learning</h3>
          <p>Latih model klasifikasi dengan data berlabel. Atur target, test split, dan parameter model, lalu evaluasi performa menggunakan metrik aktual.</p>
          <div class="pill-list"><span class="pill">Random Forest</span><span class="pill">Support Vector Machine</span><span class="pill">Confusion Matrix</span></div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Supervised.py", label="Open Supervised Lab", icon="🧠", use_container_width=True)
with right:
    st.markdown(
        """<div class="workspace-card">
          <div class="workspace-head"><div class="workspace-icon" style="background:#FFF0E5;color:#D76611">◌</div><span class="workspace-chip">Pattern discovery</span></div>
          <h3>Unsupervised Learning</h3>
          <p>Temukan pola tersembunyi tanpa label. Bandingkan hasil K-Means dan DBSCAN melalui sebaran klaster, ukuran klaster, dan skor evaluasi.</p>
          <div class="pill-list"><span class="pill">K-Means</span><span class="pill">DBSCAN</span><span class="pill">Cluster Scatter Plot</span></div>
        </div>""",
        unsafe_allow_html=True,
    )
   
    st.page_link(
        "pages/2_Unsupervised.py",
        label="Open Unsupervised Lab",
        icon="🧪",
        width="stretch",
    )

st.write("")
render_section_heading("HOW IT WORKS", "A clear path from data to decision", "Satu alur ringkas untuk menjaga eksperimen tetap mudah diulang dan hasilnya mudah dibaca.")
steps = st.columns(4, gap="medium")
step_content = [
    ("01", "Import data", "Gunakan dataset contoh atau unggah CSV milikmu."),
    ("02", "Configure", "Pilih target atau fitur dan tentukan parameter."),
    ("03", "Run experiment", "Model dilatih dan dihitung dari data yang dipilih."),
    ("04", "Review & export", "Pahami metrik, grafik, lalu unduh hasil analisis."),
]
for col, (num, title, copy) in zip(steps, step_content):
    col.markdown(
        f'<div class="workflow-step"><div class="workflow-num">STEP {num}</div><h4>{title}</h4><p>{copy}</p></div>',
        unsafe_allow_html=True,
    )

st.write("")
render_section_heading("SAMPLE DATA", "Ready-to-use datasets", "Dataset bawaan membantu kamu mulai bereksperimen tanpa perlu menyiapkan file terlebih dahulu.")
d1, d2 = st.columns(2, gap="large")
with d1:
    st.markdown("**🌿 Iris species · Supervised**")
    st.caption(f"{len(supervised_df):,} baris · {len(supervised_df.columns)-1} fitur · target `species`")
    with st.expander("Preview Iris dataset"):
        st.dataframe(supervised_df.head(6), use_container_width=True, hide_index=True)
with d2:
    st.markdown("**👥 Customer behavior · Unsupervised**")
    st.caption(f"{len(unsupervised_df):,} baris · {len(unsupervised_df.columns)} kolom numerik")
    with st.expander("Preview customer dataset"):
        st.dataframe(unsupervised_df.head(6), use_container_width=True, hide_index=True)

st.markdown(
    '<div class="soft-note"><strong>Pro tip:</strong> Untuk hasil yang lebih bermakna, periksa kolom kosong, jangan gunakan ID sebagai fitur klaster kecuali memang relevan, dan bandingkan beberapa pengaturan sebelum menarik kesimpulan.</div>',
    unsafe_allow_html=True,
)
render_footer()
