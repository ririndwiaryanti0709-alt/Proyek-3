from pathlib import Path
from html import escape
import hashlib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import DBSCAN, KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Unsupervised Lab · ML Studio", page_icon="◌", layout="wide", initial_sidebar_state="expanded")

from utils.ui import apply_global_styles, render_sidebar_brand, render_hero, render_section_heading, render_mini_stats, render_footer

BASE_DIR = Path(__file__).resolve().parents[1]
PALETTE = ["#153EBD", "#4169E1", "#FF7A1A", "#102F91", "#83A0FF", "#F7B27C", "#8DA2D8", "#B8C7EF"]

apply_global_styles()
render_sidebar_brand()


def read_dataset(uploaded):
    if uploaded is not None:
        content = uploaded.getvalue()
        digest = hashlib.md5(content).hexdigest()
        uploaded.seek(0)
        return pd.read_csv(uploaded), f"upload:{digest}", uploaded.name
    path = BASE_DIR / "data" / "dataset_unsupervised.csv"
    return pd.read_csv(path), f"default:{path.stat().st_mtime_ns}", "dataset_unsupervised.csv"


def short_label(value):
    return "Noise" if int(value) == -1 else f"Cluster {int(value) + 1}"


render_hero(
    "LAB 02  ·  UNSUPERVISED LEARNING",
    "Discover patterns <span style='color:#FFB37D'>without labels.</span>",
    "Eksplorasi struktur tersembunyi dalam data menggunakan clustering. Bandingkan pendekatan berbasis centroid dan kepadatan, lalu lihat bagaimana parameter mengubah pembagian kelompok.",
    "◌",
)

with st.sidebar:
    st.markdown("### ⚙️ Clustering controls")
    st.caption("Pilih fitur numerik yang mewakili pola yang ingin ditemukan.")
    uploaded_file = st.file_uploader("Dataset CSV", type=["csv"], key="unsup_upload", help="Fitur clustering harus berupa nilai numerik.")
    df_unsup = None
    dataset_signature = ""
    dataset_name = ""
    try:
        df_unsup, dataset_signature, dataset_name = read_dataset(uploaded_file)
    except Exception as exc:
        st.error(f"CSV tidak dapat dibaca: {exc}")

    if df_unsup is not None:
        numeric_columns = [
            c for c in df_unsup.select_dtypes(include=np.number).columns
            if df_unsup[c].notna().any() and df_unsup[c].nunique(dropna=True) > 1
        ]
        default_features = [c for c in numeric_columns if str(c).lower() not in {"id", "customerid", "customer_id", "index"} and not str(c).lower().endswith("_id")]
        if len(default_features) < 2:
            default_features = numeric_columns[:2]
        default_features = default_features[:max(2, min(3, len(default_features)))] if len(default_features) >= 2 else default_features
        if len(numeric_columns) >= 2 and len(df_unsup) >= 3:
            features = st.multiselect(
                "Features for clustering", numeric_columns,
                default=default_features,
                help="Pilih minimal dua fitur. Kolom ID biasanya tidak membantu mengukur kemiripan antarobservasi.",
            )
            algorithm = st.selectbox("Clustering algorithm", ["K-Means", "DBSCAN"])
            if algorithm == "K-Means":
                cluster_max = max(2, min(10, len(df_unsup) - 1))
                n_clusters = st.slider("Number of clusters (K)", 2, cluster_max, min(3, cluster_max), step=1)
                eps_val = None
                min_samples = None
            else:
                eps_val = st.slider("Neighborhood radius (eps)", 0.1, 3.0, 0.65, step=0.05, help="Jarak dihitung pada fitur yang telah distandardisasi.")
                min_samples_max = max(2, min(20, len(df_unsup)))
                min_samples = st.slider("Minimum samples", 2, min_samples_max, min(5, min_samples_max), step=1)
                n_clusters = None
            run_clustering = st.button("◌  Run clustering", use_container_width=True, type="primary")
        else:
            features = []
            algorithm = "K-Means"
            n_clusters = 3
            eps_val = 0.65
            min_samples = 5
            run_clustering = False
            st.warning("Dataset membutuhkan sedikitnya 3 baris dan 2 kolom numerik yang bervariasi.")
    else:
        numeric_columns = []
        features = []
        algorithm = "K-Means"
        n_clusters = 3
        eps_val = 0.65
        min_samples = 5
        run_clustering = False

config_signature = None
if df_unsup is not None:
    config_signature = (
        dataset_signature, tuple(features), algorithm,
        n_clusters if algorithm == "K-Means" else None,
        eps_val if algorithm == "DBSCAN" else None,
        min_samples if algorithm == "DBSCAN" else None,
    )

if run_clustering and df_unsup is not None:
    try:
        if len(features) < 2:
            raise ValueError("Pilih minimal dua fitur numerik untuk menjalankan clustering.")
        raw_features = df_unsup[features].replace([np.inf, -np.inf], np.nan).copy()
        entirely_empty = [c for c in raw_features.columns if raw_features[c].notna().sum() == 0]
        if entirely_empty:
            raise ValueError(f"Kolom tanpa nilai valid: {', '.join(map(str, entirely_empty))}.")
        # Impute missing values, then scale to prevent features with larger units dominating distances.
        imputer = SimpleImputer(strategy="median")
        X_imputed = imputer.fit_transform(raw_features)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)
        if not np.isfinite(X_scaled).all():
            raise ValueError("Terdapat nilai non-finite setelah preprocessing. Periksa kembali fitur pilihanmu.")
        with st.spinner("Menemukan pola dan menghitung evaluasi cluster..."):
            if algorithm == "K-Means":
                model = KMeans(n_clusters=int(n_clusters), n_init=10, random_state=42)
                labels = model.fit_predict(X_scaled)
            else:
                model = DBSCAN(eps=float(eps_val), min_samples=int(min_samples))
                labels = model.fit_predict(X_scaled)

        distinct_labels = sorted(np.unique(labels).tolist())
        real_clusters = [v for v in distinct_labels if v != -1]
        noise_count = int(np.sum(labels == -1)) if algorithm == "DBSCAN" else 0
        cluster_count = len(real_clusters)
        silhouette = None
        silhouette_note = ""
        if algorithm == "K-Means":
            if 2 <= len(np.unique(labels)) < len(labels):
                try:
                    silhouette = float(silhouette_score(X_scaled, labels))
                except Exception:
                    silhouette_note = "Silhouette score tidak tersedia untuk struktur cluster ini."
            else:
                silhouette_note = "Silhouette score tidak dapat dihitung karena hasil hanya memiliki satu cluster efektif."
        else:
            assigned_mask = labels != -1
            assigned_labels = labels[assigned_mask]
            if len(np.unique(assigned_labels)) >= 2 and len(assigned_labels) > len(np.unique(assigned_labels)):
                try:
                    silhouette = float(silhouette_score(X_scaled[assigned_mask], assigned_labels))
                    silhouette_note = "Skor dihitung pada titik yang bukan noise."
                except Exception:
                    silhouette_note = "Silhouette score tidak tersedia untuk struktur cluster ini."
            else:
                silhouette_note = "Silhouette score belum tersedia: DBSCAN perlu menemukan minimal dua cluster non-noise."

        result_df = df_unsup.copy()
        result_df["Cluster"] = labels
        result_df["Cluster label"] = [short_label(v) for v in labels]
        counts = pd.Series([short_label(v) for v in labels]).value_counts().rename_axis("Cluster").reset_index(name="Points")
        points_for_plot = result_df.copy()
        points_for_plot["Cluster label"] = pd.Categorical(
            points_for_plot["Cluster label"], categories=[short_label(v) for v in distinct_labels], ordered=True
        )
        st.session_state["unsup_result"] = {
            "signature": config_signature,
            "algorithm": algorithm,
            "features": list(features),
            "labels": labels,
            "cluster_count": cluster_count,
            "noise_count": noise_count,
            "silhouette": silhouette,
            "silhouette_note": silhouette_note,
            "result_df": result_df,
            "counts": counts,
            "points_for_plot": points_for_plot,
            "rows": len(result_df),
        }
        st.session_state.pop("unsup_error", None)
    except Exception as exc:
        st.session_state["unsup_error"] = str(exc)

if st.session_state.get("unsup_error"):
    st.error(f"Clustering tidak berhasil dijalankan. Periksa fitur dan kualitas data. Detail: {st.session_state['unsup_error']}")

if df_unsup is None:
    st.warning("Dataset belum tersedia. Unggah CSV di panel kiri atau pastikan dataset bawaan ada di folder `data/`.")
else:
    missing_total = int(df_unsup.isna().sum().sum())
    numeric_count = len(df_unsup.select_dtypes(include=np.number).columns)
    duplicate_total = int(df_unsup.duplicated().sum())
    render_section_heading("DATA OVERVIEW", "Map the shape of your data", f"Sumber data: {dataset_name}. Pilih fitur yang sesuai konteks; untuk data customer, umur, pendapatan, dan spending score sering lebih informatif dibanding ID.")
    render_mini_stats([
        ("OBSERVATIONS", f"{len(df_unsup):,}", "▤", "Total titik data"),
        ("NUMERIC FIELDS", f"{numeric_count:,}", "▦", "Kolom yang bisa dianalisis"),
        ("MISSING VALUES", f"{missing_total:,}", "◌", "Diimputasi dengan median"),
        ("DUPLICATES", f"{duplicate_total:,}", "⧉", "Baris identik terdeteksi"),
    ])
    with st.expander("⌕  Preview dataset & column profile", expanded=True):
        preview_tab, profile_tab = st.tabs(["Data preview", "Column profile"])
        with preview_tab:
            st.dataframe(df_unsup.head(12), use_container_width=True, hide_index=True)
        with profile_tab:
            profile = pd.DataFrame({
                "Column": df_unsup.columns.astype(str),
                "Data type": [str(t) for t in df_unsup.dtypes],
                "Non-null": [int(df_unsup[c].notna().sum()) for c in df_unsup.columns],
                "Missing": [int(df_unsup[c].isna().sum()) for c in df_unsup.columns],
                "Unique values": [int(df_unsup[c].nunique(dropna=True)) for c in df_unsup.columns],
            })
            st.dataframe(profile, use_container_width=True, hide_index=True)

    st.write("")
    render_section_heading("CLUSTER RESULTS", "Patterns in the data", "Silhouette score lebih dekat ke 1 biasanya menunjukkan cluster yang lebih rapat dan terpisah; interpretasikan bersama visualisasi dan konteks datanya.")
    result = st.session_state.get("unsup_result")
    if result and result.get("signature") == config_signature:
        silhouette_value = f"{result['silhouette']:.3f}" if result["silhouette"] is not None else "N/A"
        render_mini_stats([
            ("CLUSTERS FOUND", f"{result['cluster_count']:,}", "◉", "Cluster non-noise"),
            ("SILHOUETTE", silhouette_value, "✦", "Validasi pemisahan cluster"),
            ("NOISE POINTS", f"{result['noise_count']:,}", "◌", "DBSCAN only"),
            ("DATA POINTS", f"{result['rows']:,}", "▤", "Titik yang dikelompokkan"),
        ])
        st.write("")
        safe_features = escape(", ".join(map(str, result["features"])))
        st.markdown(
            f'<div class="run-panel"><span class="run-status"><span></span> Clustering completed</span><h3 style="margin:13px 0 5px;font-size:19px">{result["algorithm"]}</h3><div style="font-size:12px;color:#7180A3">Features: <b>{safe_features}</b></div></div>',
            unsafe_allow_html=True,
        )
        if result["silhouette_note"]:
            st.info(result["silhouette_note"])
        scatter_tab, distribution_tab, assigned_tab = st.tabs(["Cluster map", "Cluster distribution", "Assigned data"])
        with scatter_tab:
            if len(result["features"]) >= 2:
                a1, a2 = st.columns(2)
                with a1:
                    x_axis = st.selectbox("Horizontal axis", result["features"], index=0, key="unsup_x_axis")
                with a2:
                    y_default = 1 if len(result["features"]) > 1 else 0
                    y_axis = st.selectbox("Vertical axis", result["features"], index=y_default, key="unsup_y_axis")
                if x_axis == y_axis:
                    st.info("Gunakan fitur yang berbeda untuk sumbu X dan Y agar pola lebih mudah dibaca.")
                plot_df = result["points_for_plot"]
                label_values = plot_df["Cluster label"].astype(str).unique().tolist()
                color_map = {lab: ("#9AA5BD" if lab == "Noise" else PALETTE[i % len(PALETTE)]) for i, lab in enumerate(label_values)}
                fig = px.scatter(
                    plot_df, x=x_axis, y=y_axis, color="Cluster label", color_discrete_map=color_map,
                    hover_data=[c for c in result["features"] if c not in {x_axis, y_axis}],
                    opacity=0.84, labels={x_axis: str(x_axis).replace("_", " "), y_axis: str(y_axis).replace("_", " ")},
                    category_orders={"Cluster label": label_values},
                )
                fig.update_traces(marker=dict(size=10, line=dict(width=0.7, color="white")))
                fig.update_layout(
                    height=500, margin=dict(l=10, r=15, t=20, b=10),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white",
                    font=dict(family="DM Sans", color="#344267"),
                    legend_title_text="Group", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                    xaxis=dict(showgrid=True, gridcolor="#EDF1F8", zeroline=False),
                    yaxis=dict(showgrid=True, gridcolor="#EDF1F8", zeroline=False),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Pilih sedikitnya dua fitur untuk menampilkan scatter plot.")
        with distribution_tab:
            c1, c2 = st.columns([1.15, 1])
            with c1:
                fig_dist = px.bar(
                    result["counts"], x="Cluster", y="Points", color="Cluster",
                    color_discrete_map={r["Cluster"]: ("#9AA5BD" if r["Cluster"] == "Noise" else PALETTE[i % len(PALETTE)]) for i, r in result["counts"].iterrows()},
                    text="Points",
                )
                fig_dist.update_traces(textposition="outside", cliponaxis=False)
                fig_dist.update_layout(showlegend=False, height=360, margin=dict(l=10, r=15, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="white", font=dict(family="DM Sans", color="#344267"), xaxis_title="", yaxis_title="Number of points", yaxis=dict(gridcolor="#EDF1F8", rangemode="tozero"))
                st.plotly_chart(fig_dist, use_container_width=True)
            with c2:
                st.markdown("**Cluster balance**")
                st.dataframe(result["counts"], use_container_width=True, hide_index=True)
                st.markdown("**Interpretation guide**")
                st.markdown("- **K-Means** membagi setiap observasi ke cluster terdekat berdasarkan centroid.\n- **DBSCAN** membangun cluster dari kepadatan dan dapat menandai titik yang tidak cocok sebagai *Noise*.\n- Bandingkan ukuran cluster dan plot sebelum memutuskan apakah hasilnya masuk akal.")
        with assigned_tab:
            output_df = result["result_df"]
            st.dataframe(output_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⇩  Download clustered dataset (CSV)",
                data=output_df.to_csv(index=False).encode("utf-8-sig"),
                file_name="unsupervised_cluster_results.csv", mime="text/csv", use_container_width=True,
            )
    else:
        st.markdown(
            """<div class="run-panel"><div style="font-size:12px;color:#153EBD;font-weight:800;letter-spacing:.1em;text-transform:uppercase">Ready to find structure</div><h3 style="font-size:21px;margin:10px 0 7px">Your cluster map will appear here.</h3><p style="font-size:13px;color:#7180A3;line-height:1.7;margin:0">Pilih minimal dua fitur numerik di panel kiri, pilih algoritma, lalu tekan <b>Run clustering</b>. Fitur akan diimputasi dan distandardisasi sebelum model dijalankan.</p></div>""",
            unsafe_allow_html=True,
        )
        if result:
            st.caption("Pengaturan berubah sejak proses terakhir. Jalankan ulang clustering agar hasil sesuai dengan pilihan baru.")

render_footer()
