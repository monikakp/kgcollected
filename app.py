import streamlit as st
from supabase import create_client, Client
import pandas as pd

st.title("Тест за Supabase с service_role_key (public schema)")

# Вземаме URL и service_role_key от Streamlit Secrets
url: str = st.secrets["supabase"]["url"]
service_key: str = st.secrets["supabase"]["service_role_key"]

# Създаваме Supabase клиент
supabase: Client = create_client(url, service_key)

# Таблиците за тест
TABLES = [
    "children",
    "collected_money",
    "curr_year_start_with",
    "expense_types",
    "expenses",
]

# Функция за визуализация на таблица
def show_table(table_name: str):
    st.subheader(f"Таблица: {table_name}")
    try:
        response = supabase.table(table_name).select("*").limit(100).execute()
        data = response.data
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.success(f"Данните от {table_name} са заредени успешно!")
        else:
            st.info(f"Таблицата {table_name} е празна.")
    except Exception as e:
        st.error(f"Проблем при зареждане на {table_name}: {e}")

# Визуализираме всички таблици
for table in TABLES:
    show_table(table)
