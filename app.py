import streamlit as st
from supabase import create_client
import pandas as pd

st.title("Тест за връзка с Supabase")

# Вземаме URL и anon_key от Secrets
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase = create_client(url, st.secrets["supabase"]["service_role_key"])

# Името на таблицата за тест
TEST_TABLE = "children"

st.subheader(f"Таблица: {TEST_TABLE}")

try:
    # Изпълняваме прост SELECT
    response = supabase.table(TEST_TABLE).select("*").limit(5).execute()
    data = response.data
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
        st.success("Успешно се чете таблицата!")
    else:
        st.info("Таблицата е празна или няма редове.")
except Exception as e:
    st.error(f"Проблем при зареждане на {TEST_TABLE}: {e}")
