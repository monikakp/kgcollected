import streamlit as st
import pandas as pd
import psycopg
from psycopg.rows import dict_row

st.title("📊 Моите таблици от Supabase")

# --- Връзка към Supabase ---
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

# --- Покажи всички схеми за проверка ---
with conn.cursor() as cur:
    cur.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;")
    schemas = [r["schema_name"] for r in cur.fetchall()]
st.write("🔍 Намерени схеми в базата:", schemas)

# --- Покажи всички таблици от schema = 'kg' ---
with conn.cursor() as cur:
    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """)
    all_tables = cur.fetchall()

st.write("📋 Всички таблици, които виждам:", all_tables)

# --- Ако има таблици в kg, покажи данни ---
kg_tables = [t["table_name"] for t in all_tables if t["table_schema"] == "kg"]

if not kg_tables:
    st.warning("❗ Не намерих таблици в schema 'kg'. Проверете името на схемата.")
else:
    table_choice = st.sidebar.selectbox("Избери таблица", kg_tables)
    query = f'SELECT * FROM kg."{table_choice}" LIMIT 100;'
    df = pd.read_sql(query, conn)
    st.subheader(f"Таблица: {table_choice}")
    st.dataframe(df)
