import streamlit as st
import pandas as pd
import psycopg
from psycopg.rows import dict_row

st.title("📊 Моите таблици от Supabase (схема kg)")

# --- Връзка към Supabase (данните идват от Secrets) ---
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

# --- Вземи всички таблици от схема kg ---
with conn.cursor() as cur:
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'kg'
        ORDER BY table_name;
    """)
    tables = [r["table_name"] for r in cur.fetchall()]

if not tables:
    st.warning("❗ Няма намерени таблици в схема 'kg'")
else:
    # Sidebar за избор на таблица
    table_choice = st.sidebar.selectbox("Избери таблица", tables)

    # Зареждаме първите 100 реда от избраната таблица
    query = f'SELECT * FROM kg."{table_choice}" LIMIT 100;'
    df = pd.read_sql(query, conn)

    st.subheader(f"Таблица: {table_choice}")
    st.dataframe(df)
