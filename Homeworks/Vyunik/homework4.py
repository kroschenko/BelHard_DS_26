import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, roc_auc_score
)

# ── 1. Загрузка данных ────────────────────────────────────────────────────────
df = pd.read_csv('heart.csv')
print('Размер датасета:', df.shape)
print('\nРаспределение целевой переменной:')
print(df['target'].value_counts())

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f'\nОбучающая выборка: {X_train.shape[0]} записей')
print(f'Тестовая выборка:  {X_test.shape[0]} записей')

# ── 2. Обучение моделей ───────────────────────────────────────────────────────

# Наивный Байес
nb = GaussianNB()
nb.fit(X_train, y_train)
y_pred_nb = nb.predict(X_test)

# Логистическая регрессия
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_sc, y_train)
y_pred_lr = lr.predict(X_test_sc)

# KNN — подбор лучшего k
k_range = range(1, 31)
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_sc, y_train)
    k_scores.append(accuracy_score(y_test, knn.predict(X_test_sc)))

best_k = list(k_range)[np.argmax(k_scores)]
print(f'\nЛучшее k для KNN = {best_k}, accuracy = {max(k_scores):.4f}')

plt.figure(figsize=(10, 4))
plt.plot(k_range, k_scores, marker='o', color='steelblue')
plt.axvline(best_k, color='red', linestyle='--', label=f'Лучшее k={best_k}')
plt.xlabel('k')
plt.ylabel('Accuracy')
plt.title('Accuracy KNN при различных k')
plt.legend()
plt.tight_layout()
plt.savefig('knn_k_search.png', dpi=150)
plt.show()

knn_best = KNeighborsClassifier(n_neighbors=best_k)
knn_best.fit(X_train_sc, y_train)
y_pred_knn = knn_best.predict(X_test_sc)

# ── 3. Матрицы ошибок ─────────────────────────────────────────────────────────
models = {
    'Naive Bayes':           y_pred_nb,
    'Logistic Regression':   y_pred_lr,
    f'KNN (k={best_k})':     y_pred_knn,
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, y_pred) in zip(axes, models.items()):
    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=['No Disease', 'Disease']).plot(
        ax=ax, colorbar=False, cmap='Blues'
    )
    ax.set_title(name)
plt.suptitle('Матрицы ошибок', fontsize=14)
plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150)
plt.show()

# ── 4. Метрики качества ───────────────────────────────────────────────────────
print('\n' + '='*60)
print(f'{"Модель":<25} {"Accuracy":>9} {"Precision":>10} {"Recall":>8} {"F1":>8}')
print('='*60)
for name, y_pred in models.items():
    print(
        f'{name:<25}'
        f'{accuracy_score(y_test, y_pred):>9.4f}'
        f'{precision_score(y_test, y_pred):>10.4f}'
        f'{recall_score(y_test, y_pred):>8.4f}'
        f'{f1_score(y_test, y_pred):>8.4f}'
    )
print('='*60)

# ── 5. ROC-анализ ─────────────────────────────────────────────────────────────
proba = {
    'Naive Bayes':           nb.predict_proba(X_test)[:, 1],
    'Logistic Regression':   lr.predict_proba(X_test_sc)[:, 1],
    f'KNN (k={best_k})':     knn_best.predict_proba(X_test_sc)[:, 1],
}

plt.figure(figsize=(8, 6))
colors = ['steelblue', 'darkorange', 'green']
for (name, prob), color in zip(proba.items(), colors):
    fpr, tpr, _ = roc_curve(y_test, prob)
    auc = roc_auc_score(y_test, prob)
    plt.plot(fpr, tpr, color=color, lw=2, label=f'{name} (AUC = {auc:.3f})')

plt.plot([0, 1], [0, 1], 'k--', lw=1, label='Случайный классификатор')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-кривые')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('roc_curves.png', dpi=150)
plt.show()

print('\nAUC-ROC:')
for name, prob in proba.items():
    print(f'  {name}: {roc_auc_score(y_test, prob):.4f}')
