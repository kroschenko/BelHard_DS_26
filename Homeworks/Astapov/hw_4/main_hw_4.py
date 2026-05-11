#main_hw_4.py

import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

print('----------------------------------------------------------------------')
print('1. Взять за основу датасет Heart Disease UCI из ДЗ 2 (heart.csv)\n')

# Загрузка датасета
data = pd.read_csv('datasets/heart.csv')

# Просмотр первых строк
print(data.head())

# Признаки (X) и целевая переменная (y)
X = data.drop('target', axis=1)
y = data['target']

# Разделение данных:
# 80% - обучение
# 20% - тест
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Размеры выборок
print('\nРазмер обучающей выборки:', X_train.shape)
print('Размер тестовой выборки:', X_test.shape)

print('----------------------------------------------------------------------')
print('\n')
print('----------------------------------------------------------------------')

print('2. Загрузить данные, разделить их на обучающую и тестовую выборки\n')

# Масштабирование данных
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Создание модели
log_model = LogisticRegression(max_iter=1000)

# Обучение модели
log_model.fit(X_train_scaled, y_train)

# Предсказания
y_pred_log = log_model.predict(X_test_scaled)

# Accuracy
accuracy_log = accuracy_score(y_test, y_pred_log)

print('Точность логистической регрессии:', accuracy_log)

print('----------------------------------------------------------------------')
print('\n')
print('----------------------------------------------------------------------')

print('''3. Обучить модели наивного байесовского классификатора, логистической регрессии и k-ближайших соседей
(выявить k с наилучшим результатом, например, путем перебора результатов, получаемых для классификаторов с разными значениями k)\n''')

# Naive Bayes
nb_model = GaussianNB()

# Обучение
nb_model.fit(X_train_scaled, y_train)

# Предсказания
y_pred_nb = nb_model.predict(X_test_scaled)

# Accuracy
accuracy_nb = accuracy_score(y_test, y_pred_nb)

print('Точность Naive Bayes:', accuracy_nb)


# KNN
best_k = 1
best_accuracy = 0

print('\nРезультаты KNN:')

for k in range(1, 21):

    knn_model = KNeighborsClassifier(n_neighbors=k)

    # Обучение
    knn_model.fit(X_train_scaled, y_train)

    # Предсказания
    y_pred_knn = knn_model.predict(X_test_scaled)

    # Accuracy
    accuracy_knn = accuracy_score(y_test, y_pred_knn)

    print(f'k = {k}, accuracy = {accuracy_knn:.4f}')

    # Лучший результат
    if accuracy_knn > best_accuracy:
        best_accuracy = accuracy_knn
        best_k = k

print(f'\nЛучший k: {best_k}')
print(f'Лучшая accuracy: {best_accuracy:.4f}')

print('----------------------------------------------------------------------')
print('\n')
print('----------------------------------------------------------------------')

print('4. Построить матрицу ошибок, оценить модель с помощью accuracy, precision, recall и F1-score\n')

# Финальная модель KNN с лучшим k
final_knn = KNeighborsClassifier(n_neighbors=best_k)

# Обучение
final_knn.fit(X_train_scaled, y_train)

# Предсказания
y_pred_final_knn = final_knn.predict(X_test_scaled)

final_knn_accuracy = accuracy_score(y_test, y_pred_final_knn)

print('Точность финальной модели KNN:', final_knn_accuracy)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_final_knn)

print('\nМатрица ошибок:')
print(cm)

# Метрики качества
precision = precision_score(y_test, y_pred_final_knn)
recall = recall_score(y_test, y_pred_final_knn)
f1 = f1_score(y_test, y_pred_final_knn)

print('\nPrecision:', precision)
print('Recall:', recall)
print('F1-score:', f1)

print('----------------------------------------------------------------------')
print('\n')
print('----------------------------------------------------------------------')

print('5. Провести ROC-анализ обученных классификаторов\n')

# ROC-анализ

# Вероятности классов
y_prob_log = log_model.predict_proba(X_test_scaled)[:, 1]
y_prob_nb = nb_model.predict_proba(X_test_scaled)[:, 1]
y_prob_knn = final_knn.predict_proba(X_test_scaled)[:, 1]

# ROC-кривые
fpr_log, tpr_log, _ = roc_curve(y_test, y_prob_log)
fpr_nb, tpr_nb, _ = roc_curve(y_test, y_prob_nb)
fpr_knn, tpr_knn, _ = roc_curve(y_test, y_prob_knn)

# ROC-AUC
auc_log = roc_auc_score(y_test, y_prob_log)
auc_nb = roc_auc_score(y_test, y_prob_nb)
auc_knn = roc_auc_score(y_test, y_prob_knn)

print('ROC-AUC Logistic Regression:', auc_log)
print('ROC-AUC Naive Bayes:', auc_nb)
print('ROC-AUC KNN:', auc_knn)

# График
plt.figure(figsize=(8, 6))

plt.plot(fpr_log, tpr_log, label=f'Logistic Regression (AUC = {auc_log:.3f})')
plt.plot(fpr_nb, tpr_nb, label=f'Naive Bayes (AUC = {auc_nb:.3f})')
plt.plot(fpr_knn, tpr_knn, label=f'KNN (AUC = {auc_knn:.3f})')

# Линия случайного классификатора
plt.plot([0, 1], [0, 1], linestyle='--')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

plt.title('ROC-кривые классификаторов')

plt.legend()

plt.grid()

plt.show()

print('----------------------------------------------------------------------')
