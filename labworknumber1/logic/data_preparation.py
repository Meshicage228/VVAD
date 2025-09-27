import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "..", "source", "source_data_var_6.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "result", "cleaned_table.csv")

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

df = pd.read_csv(INPUT_FILE, sep=SEP, encoding=ENCODING)

<<<<<<< HEAD
print(f"Исходное количество строк: {len(df_clean)}")

df_clean[COL_AGE] = pd.to_numeric(df_clean[COL_AGE], errors="coerce")
age_mask = (df_clean[COL_AGE] >= MIN_AGE) & (df_clean[COL_AGE] <= MAX_AGE) & (df_clean[COL_AGE].notna())
df_clean = df_clean[age_mask]
df_clean[COL_AGE] = df_clean[COL_AGE].astype(int)

df_clean[COL_STATUS] = df_clean[COL_STATUS].str.lower()
status_mask = df_clean[COL_STATUS].isin(VALID_MARITAL_STATUS) & (df_clean[COL_STATUS].notna())
df_clean = df_clean[status_mask]

df_clean[COL_INCOME] = pd.to_numeric(df_clean[COL_INCOME], errors="coerce")
income_mask = (df_clean[COL_INCOME] >= MIN_INCOME_THRESHOLD) & (df_clean[COL_INCOME].notna())
df_clean = df_clean[income_mask]

guarantee_mask = df_clean[COL_GUARANTEE].str.lower().isin(["yes", "no"]) & (df_clean[COL_GUARANTEE].notna())
df_clean = df_clean[guarantee_mask]
df_clean[COL_GUARANTEE] = df_clean[COL_GUARANTEE].str.lower().map({"yes": 1, "no": 0})
=======
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
>>>>>>> 37bad32d3ff30f1832e77b616f55ed9a0fa15f18

print(f"Количество строк после очистки: {len(df_clean)}")

scaler = MinMaxScaler()
df[NUMERIC_COLUMNS] = scaler.fit_transform(df[NUMERIC_COLUMNS])

<<<<<<< HEAD
df_clean = pd.get_dummies(df_clean, columns=[COL_STATUS], dtype=int)
=======
# === One-Hot Encoding категориальных данных ===
df = pd.get_dummies(df, columns=[COL_STATUS])
>>>>>>> 37bad32d3ff30f1832e77b616f55ed9a0fa15f18

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False, sep=SEP, encoding=ENCODING)

<<<<<<< HEAD
print(f"Очистка завершена. Удалено {len(df) - len(df_clean)} строк.")
print(f"Результат сохранен в файл: {OUTPUT_FILE}")
print(f"Итоговый размер данных: {df_clean.shape}")
=======
print(f"Очистка, отбор, нормализация и кодирование завершены. Результат сохранен в файл: {OUTPUT_FILE}")
>>>>>>> 37bad32d3ff30f1832e77b616f55ed9a0fa15f18
