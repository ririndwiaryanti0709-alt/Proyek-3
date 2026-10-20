from pathlib import Path
import hashlib
import math
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC

st.set_page_config(page_title="Supervised Lab · ML Studio", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

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
    path = BASE_DIR / "data" / "dataset_supervised.csv"
    return pd.read_csv(path), f"default:{path.stat().st_mtime_ns}", "dataset_supervised.csv"


def make_preprocessor(X):
    numeric_columns = X.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = X.select_dtypes(exclude=np.number).columns.tolist()
    transformers = []
    if numeric_columns:
        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        transformers.append(("numeric", numeric_pipe, numeric_columns))
    if categorical_columns:
        categorical_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ])
        transformers.append(("categorical", categorical_pipe, categorical_columns))
    if not transformers:
        raise ValueError("Tidak ada kolom fitur yang bisa digunakan setelah target dipilih.")
    return ColumnTransformer(transformers=transformers, remainder="drop")


render_hero(
    "LAB 01  ·  SUPERVISED LEARNING",
    "Teach a model to <span style='color:#FFB37D'>make predictions.</span>",
    "Gunakan data berlabel untuk membangun model klasifikasi. Atur parameter, evaluasi prediksi pada data uji, lalu periksa kelas mana yang paling sering tertukar.",
    "🧠",
)

with st.sidebar:
    st.markdown("### ⚙️ Experiment controls")
    st.caption("Konfigurasikan data dan model untuk setiap eksperimen.")
    uploaded_file = st.file_uploader("Dataset CSV", type=["csv"], key="sup_upload", help="Unggah file CSV dengan satu kolom target/label.")
    df = None
    dataset_signature = ""
    dataset_name = ""
    load_error = None
    try:
        df, dataset_signature, dataset_name = read_dataset(uploaded_file)
    except Exception as exc:
        load_error = str(exc)
        st.error(f"CSV tidak dapat dibaca: {exc}")

    if df is not None and not df.empty and len(df.columns) >= 2:
        preferred_target = "species" if "species" in df.columns else str(df.columns[-1])
        target_index = list(df.columns).index(preferred_target) if preferred_target in df.columns else len(df.columns) - 1
        target_col = st.selectbox("Target / label", df.columns.tolist(), index=target_index)
        test_size = st.slider("Porsi data uji", min_value=0.10, max_value=0.40, value=0.20, step=0.05, help="Persentase data yang disimpan untuk evaluasi.")
        algorithm = st.selectbox("Algorithm", ["Random Forest", "Support Vector Machine (SVM)"])
        if algorithm == "Random Forest":
            max_depth = st.slider("Maximum tree depth", min_value=2, max_value=24, value=8, step=1)
            c_param = None
        else:
            c_param = st.slider("Regularization (C)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, help="Nilai C yang lebih tinggi memberi penalti lebih besar pada kesalahan klasifikasi saat training.")
            max_depth = None
        random_state = st.number_input("Random state", min_value=0, max_value=9999, value=42, step=1)
        run_training = st.button("▶  Run experiment", use_container_width=True, type="primary")
    else:
        target_col = None
        test_size = 0.2
        algorithm = "Random Forest"
        max_depth = 8
        c_param = None
        random_state = 42
        run_training = False
        if df is not None:
            st.warning("Dataset harus memiliki minimal 1 baris dan 2 kolom.")

config_signature = None
if df is not None and target_col is not None:
    config_signature = (dataset_signature, target_col, float(test_size), algorithm, max_depth, c_param, int(random_state))

if run_training and df is not None and target_col is not None:
    try:
        working = df.dropna(subset=[target_col]).copy()
        if len(working) < 6:
            raise ValueError("Dataset terlalu kecil. Gunakan setidaknya 6 baris dengan target yang terisi.")
        y = working[target_col]
        X = working.drop(columns=[target_col])
        if X.shape[1] == 0:
            raise ValueError("Pilih kolom target yang tidak menghapus seluruh fitur.")
        if y.nunique(dropna=True) < 2:
            raise ValueError("Target hanya memiliki satu kelas. Model klasifikasi memerlukan minimal dua kelas.")
        counts = y.value_counts(dropna=True)
        class_count = int(y.nunique())
        test_count = int(math.ceil(test_size * len(working)))
        train_count = len(working) - test_count
        can_stratify = counts.min() >= 2 and test_count >= class_count and train_count >= class_count
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=int(random_state),
            stratify=y if can_stratify else None,
        )
        preprocessor = make_preprocessor(X_train)
        if algorithm == "Random Forest":
            classifier = RandomForestClassifier(
                n_estimators=250, max_depth=int(max_depth), min_samples_leaf=1,
                class_weight="balanced_subsample", random_state=int(random_state), n_jobs=-1,
            )
        else:
            classifier = SVC(C=float(c_param), kernel="rbf", class_weight="balanced")
        model = Pipeline([("preprocessor", preprocessor), ("model", classifier)])
        with st.spinner("Training model dan menghitung metrik pada data uji..."):
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
        classes = list(model.named_steps["model"].classes_)
        cm = confusion_matrix(y_test, predictions, labels=classes)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average="weighted", zero_division=0),
            "recall": recall_score(y_test, predictions, average="weighted", zero_division=0),
            "f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
        }
        report = classification_report(y_test, predictions, labels=classes, output_dict=True, zero_division=0)
        report_df = pd.DataFrame(report).transpose().reset_index().rename(columns={"index": "Class / metric"})
        pred_df = X_test.reset_index(drop=True).copy()
        pred_df.insert(0, "Actual", y_test.reset_index(drop=True))
        pred_df.insert(1, "Predicted", pd.Series(predictions).reset_index(drop=True))
        pred_df["Correct"] = pred_df["Actual"].astype(str) == pred_df["Predicted"].astype(str)
        importance = None
        if algorithm == "Random Forest":
            names = model.named_steps["preprocessor"].get_feature_names_out()
            values = model.named_steps["model"].feature_importances_
            importance = pd.DataFrame({"Feature": names, "Importance": values}).sort_values("Importance", ascending=False).head(12)
        st.session_state["sup_result"] = {
            "signature": config_signature, "metrics": metrics, "classes": [str(v) for v in classes],
            "cm": cm, "report": report_df, "predictions": pred_df, "importance": importance,
            "model_name": algorithm, "train_rows": len(X_train), "test_rows": len(X_test),
            "class_count": class_count, "stratified": can_stratify,
        }
        st.session_state.pop("sup_error", None)
    except Exception as exc:
        st.session_state["sup_error"] = str(exc)

if st.session_state.get("sup_error"):
    st.error(f"Eksperimen belum berhasil dijalankan. Periksa target atau kualitas data. Detail: {st.session_state['sup_error']}")

if df is None:
    st.warning("Dataset belum tersedia. Unggah CSV di panel kiri atau pastikan dataset bawaan ada di folder `data/`.")
else:
    # Dataset overview
    missing_total = int(df.isna().sum().sum())
    duplicate_total = int(df.duplicated().sum())
    render_section_heading("DATA OVERVIEW", "Know what goes into the model", f"Sumber data: {dataset_name}. Periksa struktur dan kualitas dataset sebelum menjalankan training.")
    render_mini_stats([
        ("ROWS", f"{len(df):,}", "▤", "Total observasi"),
        ("COLUMNS", f"{len(df.columns):,}", "▦", "Termasuk target"),
        ("MISSING VALUES", f"{missing_total:,}", "◌", "Akan ditangani pipeline"),
        ("DUPLICATES", f"{duplicate_total:,}", "⧉", "Baris identik terdeteksi"),
    ])
    with st.expander("⌕  Preview dataset & column profile", expanded=True):
        preview_tab, profile_tab = st.tabs(["Data preview", "Column profile"])
        with preview_tab:
            st.dataframe(df.head(12), use_container_width=True, hide_index=True)
        with profile_tab:
            profile = pd.DataFrame({
                "Column": df.columns.astype(str),
                "Data type": [str(t) for t in df.dtypes],
                "Non-null": [int(df[c].notna().sum()) for c in df.columns],
                "Missing": [int(df[c].isna().sum()) for c in df.columns],
                "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns],
            })
            st.dataframe(profile, use_container_width=True, hide_index=True)

    st.write("")
    render_section_heading("MODEL RESULTS", "Performance & diagnostics", "Metrik berikut dihitung dari data uji pada eksperimen terakhir, bukan angka contoh.")
    result = st.session_state.get("sup_result")
    if result and result.get("signature") == config_signature:
        m = result["metrics"]
        render_mini_stats([
            ("ACCURACY", f"{m['accuracy']:.1%}", "◎", "Prediksi benar secara keseluruhan"),
            ("PRECISION", f"{m['precision']:.1%}", "◈", "Rata-rata tertimbang"),
            ("RECALL", f"{m['recall']:.1%}", "↗", "Rata-rata tertimbang"),
            ("F1 SCORE", f"{m['f1']:.1%}", "✦", "Keseimbangan precision & recall"),
        ])
        st.write("")
        st.markdown(
            f'<div class="run-panel"><span class="run-status"><span></span> Experiment completed</span><h3 style="margin:13px 0 5px;font-size:19px">{result["model_name"]}</h3><div style="font-size:12px;color:#7180A3">Training rows: <b>{result["train_rows"]}</b> &nbsp;·&nbsp; Test rows: <b>{result["test_rows"]}</b> &nbsp;·&nbsp; Classes: <b>{result["class_count"]}</b></div></div>',
            unsafe_allow_html=True,
        )
        if not result["stratified"]:
            st.info("Data dibagi tanpa stratifikasi karena jumlah sampel per kelas tidak memungkinkan stratifikasi yang aman.")
        cm_tab, report_tab, prediction_tab = st.tabs(["Confusion matrix", "Class report", "Test predictions"])
        with cm_tab:
            c1, c2 = st.columns([1.2, 1])
            with c1:
                fig_cm = px.imshow(
                    result["cm"], x=result["classes"], y=result["classes"], text_auto=True,
                    aspect="auto", color_continuous_scale=[[0, "#EDF2FF"], [0.5, "#83A0FF"], [1, "#153EBD"]],
                    labels={"x": "Predicted class", "y": "Actual class", "color": "Count"},
                )
                fig_cm.update_layout(margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#344267"), coloraxis_colorbar=dict(title="Count"))
                st.plotly_chart(fig_cm, use_container_width=True)
            with c2:
                st.markdown("**How to read it**")
                st.markdown("Diagonal cells are correct predictions. Values outside the diagonal show which classes the model confuses.")
                st.markdown("**Quick checks**")
                st.markdown(f"- Evaluated on **{result['test_rows']}** rows\n- **{sum(np.diag(result['cm']))}** correct predictions\n- **{result['cm'].sum() - sum(np.diag(result['cm']))}** misclassifications")
        with report_tab:
            st.dataframe(result["report"].round(4), use_container_width=True, hide_index=True)
        with prediction_tab:
            predictions_df = result["predictions"]
            correct_count = int(predictions_df["Correct"].sum())
            st.caption(f"{correct_count} benar dari {len(predictions_df)} prediksi pada data uji.")
            st.dataframe(predictions_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⇩  Download test predictions (CSV)",
                data=predictions_df.to_csv(index=False).encode("utf-8-sig"),
                file_name="supervised_test_predictions.csv", mime="text/csv", use_container_width=True,
            )
        if result["importance"] is not None and not result["importance"].empty:
            st.write("")
            render_section_heading("MODEL EXPLAINABILITY", "Which features influenced the model?", "Feature importance tersedia untuk Random Forest. Nilai lebih tinggi menunjukkan kontribusi relatif yang lebih besar pada model ini.")
            fi = result["importance"].sort_values("Importance", ascending=True)
            fig_fi = px.bar(fi, x="Importance", y="Feature", orientation="h", color="Importance", color_continuous_scale=[[0, "#B9C8F7"], [1, "#153EBD"]])
            fig_fi.update_layout(height=max(300, 26 * len(fi)), margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color="#344267"), coloraxis_showscale=False, xaxis_title="Relative importance", yaxis_title="")
            st.plotly_chart(fig_fi, use_container_width=True)
    else:
        st.markdown(
            """<div class="run-panel"><div style="font-size:12px;color:#153EBD;font-weight:800;letter-spacing:.1em;text-transform:uppercase">Ready when you are</div><h3 style="font-size:21px;margin:10px 0 7px">Your model results will appear here.</h3><p style="font-size:13px;color:#7180A3;line-height:1.7;margin:0">Pilih target dan algoritma di panel kiri, lalu tekan <b>Run experiment</b>. Pipeline akan mengisi nilai kosong, mengubah fitur kategorik, melatih model, dan menghitung evaluasi dari data uji.</p></div>""",
            unsafe_allow_html=True,
        )
        if result:
            st.caption("Konfigurasi berubah sejak eksperimen terakhir. Jalankan ulang model untuk memperbarui hasil.")

render_footer()
