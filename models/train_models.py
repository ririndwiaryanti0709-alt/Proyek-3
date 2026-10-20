"""Jalankan sekali untuk menghasilkan file .pkl di folder models/:
    python models/train_models.py
"""
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Model supervised
iris = load_iris()
clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
clf.fit(iris.data, iris.target)
joblib.dump(clf, "models/supervised_model.pkl")

# Model unsupervised (scaler + K-Means)
X = iris.data
scaler = StandardScaler().fit(X)
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(scaler.transform(X))
joblib.dump({"scaler": scaler, "model": km}, "models/unsupervised_model.pkl")

print("OK: supervised_model.pkl & unsupervised_model.pkl tersimpan")
