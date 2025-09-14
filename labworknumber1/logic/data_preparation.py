import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# === Пути к файлам ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # папка, где лежит скрипт
INPUT_FILE = os.path.join(BASE_DIR, "..", "source", "source_data_var_6.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "result", "cleaned_table.csv")

# === Константы ===
SEP = ";"
ENCODING = "utf-8-sig"

COL_AGE = "Возраст"
COL_STATUS = "Семейное положение"
COL_INCOME = "Доходы"
COL_GUARANTEE = "Наличие обеспечения"

MAX_AGE = 100
MIN_AGE = 10
VALID_MARITAL_STATUS = ["married", "single", "divorced"]
MIN_INCOME_THRESHOLD = 10
NUMERIC_COLUMNS = [COL_AGE, COL_INCOME]

# === Загрузка данных ===
df = pd.read_csv(INPUT_FILE, sep=SEP, encoding=ENCODING)
df_clean = df.copy()

# === Очистка возраста ===
df_clean[COL_AGE] = pd.to_numeric(df_clean[COL_AGE], errors="coerce")
df_clean.loc[df_clean[COL_AGE] > MAX_AGE, COL_AGE] = np.nan
df_clean.loc[df_clean[COL_AGE] < MIN_AGE, COL_AGE] = np.nan
median_age = df_clean[COL_AGE].median()
df_clean[COL_AGE].fillna(median_age, inplace=True)
df_clean[COL_AGE] = df_clean[COL_AGE].astype(int)

# === Очистка семейного положения ===
df_clean[COL_STATUS] = df_clean[COL_STATUS].str.lower()
df_clean.loc[~df_clean[COL_STATUS].isin(VALID_MARITAL_STATUS), COL_STATUS] = np.nan
most_frequent_status = df_clean[COL_STATUS].mode()[0]
df_clean[COL_STATUS].fillna(most_frequent_status, inplace=True)

# === Очистка доходов ===
df_clean[COL_INCOME] = pd.to_numeric(df_clean[COL_INCOME], errors="coerce")
df_clean.loc[df_clean[COL_INCOME] < MIN_INCOME_THRESHOLD, COL_INCOME] = np.nan
median_income = df_clean[COL_INCOME].median()
df_clean[COL_INCOME].fillna(median_income, inplace=True)

# === Обработка наличия обеспечения ===
df_clean[COL_GUARANTEE] = df_clean[COL_GUARANTEE].str.lower().map({"yes": 1, "no": 0})

# === Нормализация числовых значений ===
scaler = MinMaxScaler()
df_clean[NUMERIC_COLUMNS] = scaler.fit_transform(df_clean[NUMERIC_COLUMNS])

# === One-Hot Encoding категориальных данных ===
df_clean = pd.get_dummies(df_clean, columns=[COL_STATUS])

# === Сохранение результата ===
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_clean.to_csv(OUTPUT_FILE, index=False, sep=SEP, encoding=ENCODING)

print(f"Очистка и нормализация завершены. Результат сохранен в файл: {OUTPUT_FILE}")