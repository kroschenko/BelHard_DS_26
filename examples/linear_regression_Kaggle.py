import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# загрузка данных
train = pd.read_csv("../datasets/linear regression Kaggle dataset/train.csv")
test = pd.read_csv("../datasets/linear regression Kaggle dataset/test.csv")

date_col = "id"
target_col = "value"

original_test_date = test[date_col]

# предобработка данных
train[date_col] = pd.to_datetime(train[date_col], format="%m/%d/%y")
test[date_col] = pd.to_datetime(test[date_col], format="%m/%d/%y")

# находим самую раннюю дату, чтобы сделать ее "нулевым" днем
min_date = train[date_col].min()

# создаем новый числовой признак: количество дней с начальной даты
train["days_since_start"] = (train[date_col] - min_date).dt.days
test["days_since_start"] = (test[date_col] - min_date).dt.days

# формируем обучающую и тестовую выборки
X_train = train[["days_since_start"]]
y_train = train[target_col]
X_test = test[["days_since_start"]]

# обучение базовой модели
model = LinearRegression()
model.fit(X_train, y_train)

# ошибка на обучающей выборке
train_preds = model.predict(X_train)
mse_train = mean_squared_error(y_train, train_preds)
print(f"MSE на обучающей выборке: {mse_train:.4f}")

predictions = model.predict(X_test).round(4)

# Заполняем файл для отправки
test[date_col] = original_test_date
test[target_col] = predictions
test = test.drop(columns=["days_since_start"])
test.to_csv('submission.csv', index=False)

plt.figure(figsize=(12, 6))

plt.scatter(X_train['days_since_start'], y_train, color='blue', alpha=0.5, label='Фактические данные (Train)')

plt.title('Зависимость целевой переменной от времени', fontsize=14)
plt.xlabel('Количество дней со старта', fontsize=12)
plt.ylabel('Значение (Value)', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.show()
