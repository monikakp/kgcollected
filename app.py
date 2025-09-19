import streamlit as st
from supabase import create_client
import pandas as pd

st.title("Тест за Supabase с service_role_key")

# Вземаме URL и service_role_key от Secrets
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_role_key"]

# Създаваме клиент с service_role_key
supabase = create_client(url, service_key)

# Таблиците за тест
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
        response = supabase.table(table).select("*").limit(5).execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.success("Успешно се четат данните!")
        else:
            st.info("Таблицата е празна.")
    except Exception as e:
        st.error(f"Проблем при зареждане на {table}: {e}")
