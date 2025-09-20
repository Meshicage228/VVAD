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

# === Очистка возраста ===
df[COL_AGE] = pd.to_numeric(df[COL_AGE], errors="coerce")
df = df[(df[COL_AGE] >= MIN_AGE) & (df[COL_AGE] <= MAX_AGE)]

# === Очистка семейного положения ===
df[COL_STATUS] = df[COL_STATUS].str.lower()
df = df[df[COL_STATUS].isin(VALID_MARITAL_STATUS)]

# === Очистка доходов ===
df[COL_INCOME] = pd.to_numeric(df[COL_INCOME], errors="coerce")
df = df[df[COL_INCOME] >= MIN_INCOME_THRESHOLD]

# === Очистка наличия обеспечения ===
df[COL_GUARANTEE] = df[COL_GUARANTEE].str.lower()
df = df[df[COL_GUARANTEE].isin(["yes", "no"])]
df[COL_GUARANTEE] = df[COL_GUARANTEE].map({"yes": 1, "no": 0})

# === Нормализация числовых значений ===
scaler = MinMaxScaler()
df[NUMERIC_COLUMNS] = scaler.fit_transform(df[NUMERIC_COLUMNS])

# === One-Hot Encoding категориальных данных ===
df = pd.get_dummies(df, columns=[COL_STATUS])

# === Сохранение результата ===
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False, sep=SEP, encoding=ENCODING)

print(f"Очистка, отбор, нормализация и кодирование завершены. Результат сохранен в файл: {OUTPUT_FILE}")