import streamlit as st
import matplotlib.pyplot as plt

st.markdown("# Analytics ")
st.sidebar.markdown("# Billings details")
add_selectbox = st.sidebar.selectbox(
    'Choose the billing period accordingly',
    ('Last month', 'Last 3-month', 'Last 6-month','Consolidated')
)


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'August', 'September', 'October', 'November'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)