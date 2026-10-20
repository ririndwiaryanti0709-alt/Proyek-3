"""Fungsi preprocessing data — dipakai ulang di halaman Supervised/Unsupervised."""
import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(df, target, test_size=0.2, random_state=42):
    """Pisahkan fitur (X) dan target (y), lalu split train-test."""
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size,
                            random_state=random_state, stratify=y)


def encode_categorical(X, y):
    """Encode otomatis kolom kategorik pada X (one-hot) dan y (label encoding)."""
    cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=False)
    if y.dtype == "object":
        y = y.astype("category").cat.codes
    return X, y
