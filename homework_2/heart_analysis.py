# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.preprocessing import MinMaxScaler

mpl.rcParams["font.family"] = "DejaVu Sans"

df = pd.read_csv("heart.csv")

print(df.info())
print("\nПропуски:\n", df.isnull().sum())

target_counts = df["target"].value_counts().sort_index()
plt.figure()
plt.bar(["Здоровые (0)", "Больные (1)"], target_counts.values, color=["steelblue", "tomato"])
plt.title("Количество здоровых и больных пациентов")
plt.ylabel("Количество")
plt.tight_layout()
plt.savefig("bar_chart.png")

plt.figure()
colors = df["target"].map({0: "steelblue", 1: "tomato"})
plt.scatter(df["age"], df["thalach"], c=colors, alpha=0.7)
plt.title("Максимальный пульс от возраста")
plt.xlabel("Возраст (age)")
plt.ylabel("Максимальный пульс (thalach)")
handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="steelblue", label="Здоровые"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="tomato", label="Больные"),
]
plt.legend(handles=handles)
plt.tight_layout()
plt.savefig("scatter_plot.png")

df["sex"] = df["sex"].map({0: "female", 1: "male"})
df = pd.get_dummies(df, columns=["sex"], dtype=int)
print("\nПосле One-Hot Encoding (столбец sex):\n", df[["sex_female", "sex_male"]].head())

mean_chol = df.groupby("target")["chol"].mean()
print("\nСредний уровень холестерина:")
print(f"  Здоровые (0): {mean_chol[0]:.2f}")
print(f"  Больные  (1): {mean_chol[1]:.2f}")

cols = ["age", "trestbps", "chol", "thalach"]

scaler = MinMaxScaler()
df_sklearn = df.copy()
df_sklearn[cols] = scaler.fit_transform(df_sklearn[cols])
print("\nНормализация через sklearn (все строки):")
print(df_sklearn[cols].to_string())

df_manual = df.copy()
for col in cols:
    col_min = df_manual[col].min()
    col_max = df_manual[col].max()
    df_manual[col] = (df_manual[col] - col_min) / (col_max - col_min)
print("\nНормализация вручную (все строки):")
print(df_manual[cols].to_string())

print("\nРезультаты совпадают:", df_sklearn[cols].round(8).equals(df_manual[cols].round(8)))
