import streamlit as st
from supabase import create_client
import pandas as pd

st.title("Тест за Supabase с service_role_key")

# Вземаме URL и service_role_key от Secrets
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_role_key"]

# Създаваме Supabase клиент с service_role_key
supabase = create_client(url, service_key)

# Списък с таблиците
TABLES = [
    "children",
    "collected_money",
    "curr_year_start_with",
    "expense_types",
    "expenses",
]

# Визуализация на таблиците
for table in TABLES:
    st.subheader(f"Таблица: {table}")
    try:
        response = supabase.table(table).select("*").limit(100).execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.success("Успешно се четат данните!")
        else:
            st.info("Таблицата е празна.")
    except Exception as e:
        st.error(f"Проблем при зареждане на {table}: {e}")
