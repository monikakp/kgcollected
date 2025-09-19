import streamlit as st
from supabase import create_client

# Четене на данните от Secrets в Streamlit Cloud
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["anon_key"]

supabase = create_client(url, anon_key)

st.title("Моите таблици от Supabase")

# Пример с таблица "kg_users"
try:
    data = supabase.table("kg_users").select("*").execute()
    st.write(data.data)
except Exception as e:
    st.error(f"Грешка при четене: {e}")
