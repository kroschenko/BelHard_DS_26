

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import adjusted_rand_score, r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from minisom import MiniSom

# ==========================================================
# ЧАСТЬ 1: КЛАСТЕРИЗАЦИЯ (Seeds Data Set)
# ==========================================================
print("=== ЧАСТЬ 1: КЛАСТЕРИЗАЦИЯ (SEEDS) ===")

# 1. Загрузка данных
try:
    df_seeds = pd.read_csv('seeds.csv') 
    X_seeds = df_seeds.iloc[:, :-1].values 
    y_seeds = df_seeds.iloc[:, -1].values  

    # Нормализация для кластеризации
    scaler_seeds = MinMaxScaler()
    X_seeds_scaled = scaler_seeds.fit_transform(X_seeds)

    # --- Нейронная сеть Кохонена (SOM) ---
    som = MiniSom(x=1, y=3, input_len=X_seeds.shape[1], sigma=1.0, learning_rate=0.5)
    som.random_weights_init(X_seeds_scaled)
    som.train_random(X_seeds_scaled, 100)
    som_clusters = [som.winner(x)[1] for x in X_seeds_scaled]

    # --- Алгоритм K-means ---
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans_clusters = kmeans.fit_predict(X_seeds_scaled)

    print(f"Сходство SOM с реальными метками: {adjusted_rand_score(y_seeds, som_clusters):.4f}")
    print(f"Сходство K-means с реальными метками: {adjusted_rand_score(y_seeds, kmeans_clusters):.4f}")
 
except FileNotFoundError:
    print("Ошибка: Файл seeds.csv не найден!")
 
# ==========================================================
# ЧАСТЬ 2: ПРОГНОЗ ВЕСА (Fish Market)
# ==========================================================
    print("\n=== ЧАСТЬ 2: ПРОГНОЗ ВЕСА (FISH MARKET) ===")

try:
    df_fish = pd.read_csv('Fish.csv')
    features = ['Length1', 'Length2', 'Length3', 'Height', 'Width']
    X_fish = df_fish[features]
    y_fish = df_fish['Weight']

# Разделение и масштабирование
    X_train, X_test, y_train, y_test = train_test_split(X_fish, y_fish, test_size=0.2, random_state=42)
    scaler_fish = StandardScaler()
    X_train_scaled = scaler_fish.fit_transform(X_train)
    X_test_scaled = scaler_fish.transform(X_test)

# --- Многослойный перцептрон (MLP) ---
# Поставил 100 000 итераций. На 5000 и 10000 итераций выдает предупреждение
 

    mlp = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=100000, random_state=42)
    mlp.fit(X_train_scaled, y_train)
    y_pred_mlp = mlp.predict(X_test_scaled)

# --- Линейная регрессия ---
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

# Вывод метрик
    def print_fish_metrics(name, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        print(f"\nМодель: {name}")
        print(f"  R2: {r2:.4f}")
        print(f"  RMSE: {rmse:.2f} гр.")
        print(f"  MAE: {mae:.2f} гр.")

    print_fish_metrics("Многослойный перцептрон", y_test, y_pred_mlp)
    print_fish_metrics("Линейная регрессия", y_test, y_pred_lr)

# --- ВИЗУАЛИЗАЦИЯ ДЛЯ ВТОРОЙ ЧАСТИ ---
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(y_test, y_pred_mlp, color='blue', alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('MLP: Прогноз vs Реальность')
    plt.xlabel('Реальный вес')
    plt.ylabel('Предсказанный вес')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.scatter(y_test, y_pred_lr, color='green', alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('Линейная регрессия: Прогноз vs Реальность')
    plt.xlabel('Реальный вес')
    plt.ylabel('Предсказанный вес')
    plt.grid(True)

    plt.tight_layout()
    print("\nГрафики построены. Закройте окно графика, чтобы завершить программу.")
    plt.show()

except FileNotFoundError:
    print("Ошибка: Файл Fish.csv не найден!")
