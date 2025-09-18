import streamlit as st
import pandas as pd
import psycopg
from psycopg.rows import dict_row

st.title("Всички таблици от схема kg")

# --- Връзка към Supabase ---
db = st.secrets["connections"]["supabase"]

try:
    conn = psycopg.connect(
        host=db["host"],
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        port=int(db.get("port", 5432)),
        sslmode=db.get("sslmode", "require"),
        row_factory=dict_row
    )
    st.success("Успешна връзка с базата")
except Exception as e:
    st.error(f"Грешка при връзка със Supabase: {e}")
    st.stop()

# --- Вземи всички таблици от kg ---
try:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'kg'
            ORDER BY table_name;
        """)
        tables = [r["table_name"] for r in cur.fetchall()]
except Exception as e:
    st.error(f"Грешка при четене на таблици: {e}")
    st.stop()

if not tables:
    st.warning("Няма намерени таблици в schema 'kg'.")
else:
    for table in tables:
        st.subheader(f"Таблица: {table}")
        try:
            df = pd.read_sql(f'SELECT * FROM kg."{table}" LIMIT 100;', conn)
            if df.empty:
                st.info("Таблицата е празна")
            else:
                st.dataframe(df)
        except Exception as e:
            st.error(f"Грешка при зареждане на {table}: {e}")
