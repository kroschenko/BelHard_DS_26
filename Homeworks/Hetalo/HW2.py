import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('heart.csv')
print(df.isnull().sum())
fig, ax = plt.subplots()
patients = ['Здоровые', 'Больные']
counts = df['target'].value_counts()
bar_labels = ['Здоровые', 'Больные']
bar_colors = ['tab:blue', 'tab:red']
ax.bar(patients, counts, label=bar_labels, color=bar_colors)
ax.set_ylabel('Количество')
ax.set_title('Количество здоровых и больных пациентов')
ax.legend(title='Типы пациентов')
plt.show()

health = df[df['target'] == 0]
sick = df[df['target'] == 1]

plt.figure()
plt.scatter(health['age'], health['thalach'], c="blue")
plt.scatter(sick['age'], sick['thalach'], c="red")

m, b = np.polyfit(sick['age'], sick['thalach'], 1)
plt.plot(sick['age'], m*sick['age'] + b, color="red")

z, o = np.polyfit(health['age'], health['thalach'], 1)
plt.plot(health['age'], z*health['age'] + o, color="blue")

plt.xlabel("Возраст")
plt.ylabel("Пульс")

plt.title("Диаграмма рассеяния")

plt.show()

sex_mapping = {0: "female",   1: "male"}
df["sex"] = df["sex"].map(sex_mapping)
print(df)
df = pd.get_dummies(df, columns=['sex'],dtype="int")
print(df)

average_chol_health = health['chol'].mean()
average_chol_sick = sick['chol'].mean()

print(average_chol_health)
print(average_chol_sick)

print(df[['age', 'trestbps', 'chol', 'thalach']].describe())

scaler = MinMaxScaler()
df[['age', 'trestbps', 'chol', 'thalach']] = scaler.fit_transform(df[['age', 'trestbps', 'chol', 'thalach']])

print(df[['age', 'trestbps', 'chol', 'thalach']].describe())