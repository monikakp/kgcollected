import streamlit as st
import pandas as pd
from supabase import create_client

st.title("📊 Всички таблици от Supabase (схема kg)")

# --- Вземи URL и ключ от Secrets ---
url = st.secrets["connections"]["supabase"]["url"]
key = st.secrets["connections"]["supabase"]["anon_key"]

supabase = create_client(url, key)

# --- Пример: изброяване на таблиците в schema 'kg' ---
# Supabase не предлага директен SQL за всички таблици чрез client, така че може да въведеш имената ръчно
tables = ["table1", "table2", "table3", "table4", "table5"]  # сложи твоите реални таблици

for table in tables:
    st.subheader(f"Таблица: {table}")
    try:
        # Вземи до 100 реда от таблицата
        response = supabase.table(table).select("*").limit(100).execute()
        data = response.data
        if not data:
            st.info("Таблицата е празна")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df)
    except Exception as e:
        st.error(f"Грешка при зареждане на {table}: {e}")
