import streamlit as st
import psycopg
from psycopg.rows import dict_row

st.title("📊 Тест връзка със Supabase")

# --- Връзка към Supabase ---
try:
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
    st.success("✅ Успешна връзка с базата")

    # Пробна заявка: покажи всички схеми
    with conn.cursor() as cur:
        cur.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;")
        schemas = [r["schema_name"] for r in cur.fetchall()]
    st.write("🔍 Намерени схеми:", schemas)

except Exception as e:
    st.error(f"❌ Грешка: {e}")
