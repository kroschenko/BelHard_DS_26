import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#  1. file reading and validation on empty values
file_path = '../../../datasets/heart.csv'
df: pd.DataFrame = pd.read_csv(file_path)
missing_data_in_rows = df.isna().sum()
total_missing_data = df.isna().sum().sum()
#   uncomment line below to print all rows in DF
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print('Initial DataFrame\n', df, '\n')
print(f'missing data in rows: \n{missing_data_in_rows}', '\n')
print(f'total missing data: {total_missing_data}', '\n')


sick_patients = df[df['target'] == 1]
healthy_patients = df[df['target'] == 0]


#  2. bar chart comparing the numbers of healthy and sick patients
fig, ax = plt.subplots()
category = ['sick', 'healthy']
total_sick = len(sick_patients)
total_healthy = len(healthy_patients)
colors = ['tab:red', 'tab:green']

bar_1 = ax.bar(category, [total_sick, total_healthy], color=colors)
ax.set_ylabel('Number of patients')
ax.set_title('Comparison of sick and healthy patients')

for bar in bar_1.patches:
    width = bar.get_width()
    height = bar.get_height()
    ax.text(bar.get_x() + 0.5 * width, 0.5 * height, str(height), ha='center', va='center', color='white')

plt.show()


#   3. scatterplot showing thalach-age relationship
plt.scatter(sick_patients['age'], sick_patients['thalach'], color='red', label='Sick')
plt.scatter(healthy_patients['age'], healthy_patients['thalach'], color='green', label='Healthy')

plt.xlabel('Age')
plt.ylabel('Max Heart Rate (thalach)')
plt.title('Relationship between Age and Max Heart Rate')

plt.legend()
plt.grid(True)

plt.show()


#  4. sex attribute converting and one-hot encoding applying
df_converted = df.copy()
df_converted['sex'] = df_converted['sex'].map({0: 'female', 1: 'male'})
print('DataFrame with sex attribute converted \n', df_converted, '\n')

df_converted = pd.get_dummies(df_converted, columns=['sex'], dtype='int')
print('DataFrame with one-hot encoding for sex attribute \n', df_converted, '\n')


#   5. average cholesterol (chol) level calculation
chol_sick = sick_patients['chol'].sum() / len(sick_patients)
chol_healthy = healthy_patients['chol'].sum() / len(healthy_patients)

print(f'chol for sick patients: {chol_sick}')
print(f'chol for healthy patients: {chol_healthy} \n')


#  6. normalization of the age, trestbps, chol, thalach features
min_max_normalized_df = df.copy()
mean_normalized_df = df.copy()
features = ['age', 'trestbps', 'chol', 'thalach']

for col in features:
    min_max_normalized_df[col] = (min_max_normalized_df[col] - min_max_normalized_df[col].min()) / (
        min_max_normalized_df[col].max() - min_max_normalized_df[col].min())

    mean_normalized_df[col] = (mean_normalized_df[col] - mean_normalized_df[col].mean()) / mean_normalized_df[col].std()

print('DataFrame with min-max normalization \n', min_max_normalized_df, '\n')
print('DataFrame with mean normalization \n', mean_normalized_df)
