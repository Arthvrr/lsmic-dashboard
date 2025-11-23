import pandas as pd
import re

# Lire le CSV
df = pd.read_csv("./databases/Members.csv")

# Renommer les colonnes
df = df.rename(columns={
    "Name": "first_name",
    "Surname": "last_name",
    "Active": "active",
    "Email_address": "email",
    "City": "city",
    "Birthdate": "birthdate",
    "Sex": "sex",
    "Entry_Date": "entry_date",
    "Exit_Date": "exit_date",
    "Studies": "studies",
    "Holdings (%)": "holdings_pct",
    "PL_Absolute": "pl_absolute",
    "PL_Return": "pl_return",
    "Investment": "investment"
})

columns_to_keep = [
    "first_name", "last_name", "active", "email",
    "holdings_pct", "pl_absolute", "pl_return", "investment"
]

df_clean = df[columns_to_keep].copy()

# Normaliser les floats
for col in ["holdings_pct", "pl_absolute", "pl_return", "investment"]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0.0)

# Convertir active en bool
df_clean['active'] = df_clean['active'].astype(bool)

# Export CSV
df_clean.to_csv("./databases/Members_clean.csv", index=False)

print("CSV nettoyé créé avec succès !")