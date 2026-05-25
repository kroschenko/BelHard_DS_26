import pandas as pd

from minisom import MiniSom

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score


print('Загрузка данных...\n')

columns = [
    'Area',
    'Perimeter',
    'Compactness',
    'Kernel_Length',
    'Kernel_Width',
    'Asymmetry_Coefficient',
    'Kernel_Groove_Length',
    'Class'
]

df = pd.read_csv(r'datasets/seeds_dataset.txt', sep=r'\s+', header=None, names=columns)

print(df.head())

# Признаки
X = df.drop('Class', axis=1)

# Настоящие классы
y = df['Class']

# Масштабирование
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ------------------------------------------------
# Нейронная сеть Кохонена
# ------------------------------------------------

print('\nОбучение сети Кохонена...\n')

som = MiniSom(x=3, y=1, input_len=X_scaled.shape[1], sigma=1.0, learning_rate=0.5, random_seed=42)

som.random_weights_init(X_scaled)

som.train_random(X_scaled,1000)

som_clusters = []

for row in X_scaled:
    winner = som.winner(row)
    som_clusters.append(winner[0])

# ------------------------------------------------
# K-Means
# ------------------------------------------------

print('Обучение K-Means...\n')

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

kmeans_clusters = kmeans.fit_predict(X_scaled)

# ------------------------------------------------
# Сравнение результатов
# ------------------------------------------------

som_score = adjusted_rand_score(y, som_clusters)

kmeans_score = adjusted_rand_score(y, kmeans_clusters)

print('Результаты:\n')

print(f'Сеть Кохонена: {som_score:.4f}')
print(f'K-Means: {kmeans_score:.4f}')