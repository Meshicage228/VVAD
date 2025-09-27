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
df_clean = df.copy()

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

print(f"Количество строк после очистки: {len(df_clean)}")

scaler = MinMaxScaler()
df_clean[NUMERIC_COLUMNS] = scaler.fit_transform(df_clean[NUMERIC_COLUMNS])

df_clean = pd.get_dummies(df_clean, columns=[COL_STATUS], dtype=int)

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df_clean.to_csv(OUTPUT_FILE, index=False, sep=SEP, encoding=ENCODING)

print(f"Очистка завершена. Удалено {len(df) - len(df_clean)} строк.")
print(f"Результат сохранен в файл: {OUTPUT_FILE}")
print(f"Итоговый размер данных: {df_clean.shape}")