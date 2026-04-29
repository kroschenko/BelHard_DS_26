import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

path_file_csv = 'datasets/heart.csv'

df = pd.read_csv(path_file_csv)


print('1. Загрузите данные и выведите информацию о них. Проверьте на наличие пропусков.\n')

# Общая информация о датасете
print(df.info())

# Первые и последние строки
print(df.head())
print(df.tail())

# Описательная статистика
print(df.describe())

# Проверка пропусков
print(df.isnull().sum())

input('\nДалее? [Enter]\n')



print('2. Постройте столбчатую диаграмму, сравнивающую количество здоровых и больных пациентов.\n')

# Подсчёт классов
counts = df['target'].value_counts().rename(index={0: 'Healthy', 1: 'Disease'})

# Построение
plt.figure()
counts.plot(kind='bar')
plt.title('Количество здоровых и больных пациентов')
plt.xlabel('Состояние пациента')
plt.ylabel('Количество')
plt.grid()
plt.show()

input('\nДалее? [Enter]\n')



print('''
3. Создайте диаграмму рассеяния, показывающую зависимость
максимального пульса (thalach) от возраста (age).
Раскрасьте точки в зависимости от наличия болезни.
''')

plt.figure()

# Разделяем по классам
healthy = df[df['target'] == 0]
disease = df[df['target'] == 1]

plt.scatter(healthy['age'], healthy['thalach'], label='Healthy', alpha=0.7)
plt.scatter(disease['age'], disease['thalach'], label='Disease', alpha=0.7)

plt.xlabel('Возраст')
plt.ylabel('Макс. пульс (thalach)')
plt.title('Возраст vs Максимальный пульс')

plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

input('\nДалее? [Enter]\n')



print('''
4. Преобразуйте признак sex (0 = женщина, 1 = мужчина) в более
читаемый формат с категориями 'female' и 'male',
а затем примените к нему One-Hot Encoding.
''')

# Замена значений
df['sex'] = df['sex'].map({0: 'female', 1: 'male'})

# One-Hot Encoding (создаём новый DataFrame)
df_encoded = pd.get_dummies(df, columns=['sex'])

print(df_encoded.head())

input('\nДалее? [Enter]\n')



print('5. Рассчитайте средний уровень холестерина (chol) для больных и здоровых пациентов.')

mean_chol = df.groupby('target')['chol'].mean()

print("Средний холестерин:")
print("Здоровые:", mean_chol[0])
print("Больные:", mean_chol[1])

input('\nДалее? [Enter]\n')



print('6. Выполните нормализацию признаков age, trestbps, chol и thalach.')

scaler = MinMaxScaler()

columns_to_scale = ['age', 'trestbps', 'chol', 'thalach']

# Создаём копию, чтобы не портить исходные данные
df_scaled = df.copy()
df_scaled[columns_to_scale] = scaler.fit_transform(df_scaled[columns_to_scale])

print(df_scaled.head())
