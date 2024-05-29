import streamlit as st
# pip install psycopg2
import psycopg2
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Coffee Shop Visitor Tracker", layout="wide")

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
rows = run_query("select *, msg_datetime::date visit_date from logs")
data=pd.DataFrame(rows)
data.columns=['ids','msg_datetime','obj_track_id','labels','scores','left_coords','upper_coords','right_coords','down_coords','created_at', 'visit_date']



# Create the dashboard
st.title("Coffee Shop Visitor Tracker")

# Create a big number counter for new visitors
st.subheader("Today Visitors")
today_visitors = pd.DataFrame(run_query("select distinct obj_track_id, msg_datetime::date visit_date from logs")) #WHERE msg_datetime::date = CURRENT_DATE
today_visitors.columns=['obj_track_id', 'visit_date']

new_visitors = len(today_visitors)
st.markdown(f"<h1 style='text-align: center; color: green;'>{new_visitors}</h1>", unsafe_allow_html=True)
# new_visitors = run_query("select count(*) from (select distinct obj_track_id from logs) AS TTS")


# st.markdown(f"<h1 style='text-align: center; color: blue;'>{new_visitors}</h1>", unsafe_allow_html=True)

# Display the data
st.subheader("Visitor Data")
data_aliases = data.rename(columns={'visit_date': 'Visit Date', 'obj_track_id': 'Person ID'})
st.table(data_aliases[['Visit Date','Person ID']].drop_duplicates())



# Create a line chart for visitor count over time
st.subheader("Visitor Count Over Time")
line_chart = alt.Chart(data).mark_line().encode(
    x='msg_datetime',
    y='count(ids)'
)
st.altair_chart(line_chart, use_container_width=True)

# Create a bar chart for visitor count by label
st.subheader("Visitor Count by Label")
bar_chart = alt.Chart(data).mark_bar().encode(
    x='labels',
    y='count(ids)'
)
st.altair_chart(bar_chart, use_container_width=True)

# # Create a scatter plot for visitor coordinates
# st.subheader("Visitor Coordinates")
# scatter_plot = alt.Chart(data).mark_circle().encode(
#     x='left_coords',
#     y='upper_coords',
#     color='labels'
# )
# st.altair_chart(scatter_plot, use_container_width=True)

# Create a visitors growth chart
st.subheader("Visitors Growth")
visitors_growth = data.groupby(pd.to_datetime(data['msg_datetime']).dt.date).apply(lambda x: x['obj_track_id'].nunique()).reset_index(name='unique_visitors')
visitors_growth['cumulative_visitors'] = visitors_growth['unique_visitors'].cumsum()
growth_chart = alt.Chart(visitors_growth).mark_line().encode(
    x='msg_datetime:T',
    y='cumulative_visitors'
)
st.altair_chart(growth_chart, use_container_width=True)




# rows = run_query("select * from logs")


# data=pd.DataFrame(rows)
# data.columns=['ids','msg_datetime','obj_track_id','labels','scores','left_coords','upper_coords','right_coords','down_coords','created_at']
# st.table(data)

# # streamlit_app.py

# import streamlit as st

# # Initialize connection.
# conn = st.connection("postgresql", type="sql")

# # Perform query.
# df = conn.query('SELECT * FROM mytable;', ttl="10m")

# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")