import streamlit as st
# pip install psycopg2
import psycopg2
import pandas as pd


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from mytable")

data=pd.DataFrame(rows)
data.columns=['name','pet']
st.table(data)

# # streamlit_app.py

# import streamlit as st

# # Initialize connection.
# conn = st.connection("postgresql", type="sql")

# # Perform query.
# df = conn.query('SELECT * FROM mytable;', ttl="10m")

# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")