"""Fungsi evaluasi & visualisasi — dipakai di halaman Supervised."""
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true, y_pred):
    """Buat figure heatmap confusion matrix. Return objek Figure Streamlit."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Prediksi")
    ax.set_ylabel("Aktual")
    return fig
