import streamlit as st
from supabase import create_client
import pandas as pd

# Взимаме данните от Secrets
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase = create_client(url, anon_key)

st.title("Моите таблици от Supabase (public schema)")

# Списък с таблиците
TABLES = [
    "children",
    "collected_money",
    "curr_year_start_with",
    "expense_types",
    "expenses",
]

# Функция за изпълнение на SQL query
def fetch_table(table_name):
    sql = f"SELECT * FROM {table_name} LIMIT 100;"
    try:
        result = supabase.rpc("sql", {"query": sql}).execute()
        return result.data
    except Exception as e:
        st.error(f"Проблем при зареждане на {table_name}: {e}")
        return None

# Визуализация на таблиците
for table in TABLES:
    st.subheader(f"Таблица: {table}")
    data = fetch_table(table)
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.info("Няма налични редове или достъпът е отказан.")
