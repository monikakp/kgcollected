# app.py
import streamlit as st
import pandas as pd
import psycopg
from psycopg.rows import dict_row

st.title("Моите таблици от Supabase")

# ---------------------------
# Връзка с базата (от secrets)
# ---------------------------
db = st.secrets["connections"]["supabase"]

conn = psycopg.connect(
    host=db["host"],
    dbname=db["dbname"],
    user=db["user"],
    password=db["password"],
    port=int(db.get("port", 5432)),
    sslmode=db.get("sslmode", "require"),
    row_factory=dict_row
)

# ---------------------------
# Списък с твоите таблици
# ---------------------------
tables = ["children", "expenses", "collected_money"]  # смени с истинските имена

# Sidebar за избор на таблица
table_choice = st.sidebar.selectbox("Избери таблица", tables)

# ---------------------------
# Покажи данните от избраната таблица
# ---------------------------
query = f'SELECT * FROM kg."{table_choice}" LIMIT 100;'  # взема първите 100 реда
df = pd.read_sql(query, conn)

st.subheader(f"Съдържание на {table_choice}")
st.dataframe(df)
