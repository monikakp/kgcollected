# app.py
import streamlit as st
import pandas as pd
import psycopg
from psycopg.rows import dict_row

st.set_page_config(page_title="Supabase ↔ Streamlit", layout="wide")

st.title("🔗 Supabase ↔ Streamlit (без парола в кода)")

# ---------------------------
# Четене на данни за връзка
# ---------------------------
# Очакваме структурата в secrets.toml или Streamlit Cloud Secrets:
# [connections.supabase]
# host = "grtbkhkxaemkxjuotvjy.supabase.co"
# dbname = "kgcollected"        # или "postgres"
# user = "postgres"
# password = "ТВОЯТА_ПАРОЛА"
# port = "5432"

db = st.secrets["connections"]["supabase"]

# ---------------------------
# Инициализация на връзката (cached)
# ---------------------------
@st.cache_resource
def get_conn():
    try:
        conn = psycopg.connect(
            host=db["host"],
            dbname=db["dbname"],
            user=db["user"],
            password=db["password"],
            port=int(db.get("port", 5432)),
            row_factory=dict_row,  # връща редовете като речници
            autocommit=False
        )
        return conn
    except Exception as e:
        st.error(f"Неуспешна връзка към базата: {e}")
        raise

conn = get_conn()

# ---------------------------
# Помощни функции
# ---------------------------
def list_tables(conn):
    q = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type='BASE TABLE'
        ORDER BY table_name;
    """
    with conn.cursor() as cur:
        cur.execute(q)
        return [r["table_name"] for r in cur.fetchall()]

def get_table_df(conn, table_name, limit=200):
    q = f"SELECT * FROM public.{psycopg.sql.Identifier(table_name).string} LIMIT %s"
    # psycopg.sql.Identifier.string used only to safely assemble; simpler path below
    q = f"SELECT * FROM public.{table_name} LIMIT %s"
    with conn.cursor() as cur:
        cur.execute(q, (limit,))
        rows = cur.fetchall()
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows)

def get_table_columns(conn, table_name):
    q = """
    SELECT column_name, is_identity, column_default, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = %s
    ORDER BY ordinal_position;
    """
    with conn.cursor() as cur:
        cur.execute(q, (table_name,))
        return cur.fetchall()

def insert_row(conn, table_name, col_names, values):
    placeholders = ", ".join(["%s"] * len(values))
    cols = ", ".join([f'"{c}"' for c in col_names])
    q = f'INSERT INTO public."{table_name}" ({cols}) VALUES ({placeholders}) RETURNING *;'
    with conn.cursor() as cur:
        cur.execute(q, tuple(values))
        conn.commit()
        return cur.fetchone()

# ---------------------------
# UI
# ---------------------------
with st.sidebar:
    st.header("Настройки")
    try:
        tables = list_tables(conn)
    except Exception as e:
        st.error("Не мога да прочета таблиците: " + str(e))
        st.stop()

    if not tables:
        st.info("Няма таблици в схемата public.")
        st.stop()

    table = st.selectbox("Избери таблица", tables)

st.markdown(f"## Таблица: `{table}`")

# Покажи съдържание
st.subheader("Преглед на данни")
try:
    df = get_table_df(conn, table, limit=200)
    st.dataframe(df)
except Exception as e:
    st.error(f"Грешка при четене на таблицата: {e}")

# Формуляр за добавяне на нов ред
st.subheader("Добави нов ред")

cols_meta = get_table_columns(conn, table)

# Филтрираме кои колони да попълним (пропускаме identity / serial / default nextval)
insertable_cols = []
for c in cols_meta:
    if c["is_identity"] == "YES":
        continue
    col_default = c["column_default"] or ""
    if "nextval" in (col_default or ""):  # serial/sequence
        continue
    insertable_cols.append(c)

if not insertable_cols:
    st.info("Няма колони, в които да добавяш стойности (всички са идентичности или се попълват автоматично).")
else:
    with st.form("insert_form"):
        inputs = {}
        for meta in insertable_cols:
            cname = meta["column_name"]
            dtype = meta["data_type"]
            # опростено: използваме текстов input за всичко. Може да се подобри по тип.
            inputs[cname] = st.text_input(f"{cname} ({dtype})")
        submitted = st.form_submit_button("Добави")

        if submitted:
            # Превръщаме празни стрингове в None (NULL)
            values = [None if v == "" else v for v in inputs.values()]
            try:
                new_row = insert_row(conn, table, list(inputs.keys()), values)
                st.success("Успешно добавен ред.")
                if new_row:
                    st.json(new_row)
                # Обнови визуализацията
                df = get_table_df(conn, table, limit=200)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Грешка при добавяне: {e}")
