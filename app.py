import streamlit as st
from supabase import create_client
import pandas as pd

# Взимаме данните от Secrets
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase = create_client(url, anon_key)

st.title("Моите таблици от Supabase (public schema)")

TABLES = [
    "children",
    "collected_money",
    "curr_year_start_with",
    "expense_types",
    "expenses",
]

for table in TABLES:
    st.subheader(f"Таблица: {table}")
    try:
        response = supabase.table(table).select("*").limit(100).execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("Няма редове в тази таблица.")
    except Exception as e:
        st.error(f"Проблем при зареждане на {table}: {e}")
