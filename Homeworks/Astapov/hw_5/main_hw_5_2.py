import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    r2_score,
    root_mean_squared_error
)

print('Загрузка данных...\n')

df = pd.read_csv(r'datasets/Fish.csv')

print(df.head())

# ------------------------------------------------
# Признаки и целевая переменная
# ------------------------------------------------

X = df[['Length1', 'Length2', 'Length3', 'Height', 'Width']]

y = df['Weight']

# ------------------------------------------------
# Разделение данных
# ------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------------------------------------
# Масштабирование
# ------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------------------------
# Многослойный персептрон
# ------------------------------------------------

print('\nОбучение многослойного персептрона...\n')

mlp = MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=5000, random_state=42)

mlp.fit(X_train_scaled, y_train)

y_pred_mlp = mlp.predict(X_test_scaled)

mlp_r2 = r2_score(y_test, y_pred_mlp)

mlp_rmse = root_mean_squared_error(y_test, y_pred_mlp)

print('Многослойный персептрон')

print(f'R2: {mlp_r2:.4f}')
print(f'RMSE: {mlp_rmse:.4f}')

# ------------------------------------------------
# Линейная регрессия
# ------------------------------------------------

print('\nОбучение линейной регрессии...\n')

lr = LinearRegression()

lr.fit(X_train_scaled, y_train)

y_pred_lr = lr.predict(X_test_scaled)

lr_r2 = r2_score(y_test, y_pred_lr)

lr_rmse = root_mean_squared_error(y_test, y_pred_lr)

print('Линейная регрессия')

print(f'R2: {lr_r2:.4f}')
print(f'RMSE: {lr_rmse:.4f}')

# ------------------------------------------------
# Сравнение моделей
# ------------------------------------------------

print('\nСравнение результатов:\n')

if mlp_r2 > lr_r2:
    print('Многослойный персептрон показал лучший R2')
else:
    print('Линейная регрессия показала лучший R2')

if mlp_rmse < lr_rmse:
    print('Многослойный персептрон показал меньшую ошибку RMSE')
else:
    print('Линейная регрессия показала меньшую ошибку RMSE')
