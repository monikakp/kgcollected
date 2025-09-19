import streamlit as st
from supabase import create_client

# Взимаме данните от Secrets (Streamlit Cloud → Settings → Secrets)
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase = create_client(url, anon_key)

st.title("Информация за събрани пари и разходи")

# Списък с таблиците (схема + име)
TABLES = [
    "children",
    "collected_money",
    "curr_year_start_with",
    "expense_types",
    "expenses",
]

# Визуализация
for table in TABLES:
    st.subheader(f"Таблица: {table}")
    try:
        response = supabase.table(table).select("*").execute()
        data = response.data
        if data:
            st.dataframe(data)
        else:
            st.info("Няма редове в тази таблица.")
    except Exception as e:
        st.error(f"Проблем при зареждане на {table}: {e}")
