import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np


### CONFIG
st.set_page_config(
    page_title="GETAROUND ANALYSIS",
    page_icon="🚗",
    layout="wide"
  )

### TITLE AND TEXT
st.title("GETAROUND DELAY ANALYSIS 🚗")

st.markdown("""
   This Dashboard provide you analysis regarding the delay when customers do not bring back the car on time
""")

with st.expander("⏯️ If you do not know what is Getaround"):
   st.video("https://www.youtube.com/watch?v=Xn4Q298-Kgg")

@st.cache_data 
def load_data():
    data = pd.read_excel("get_around_delay_analysis.xlsx")
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

if st.checkbox('Show raw data'):
   st.subheader('Raw data')
   st.write(data) 

#Preprocessing
mask=data["time_delta_with_previous_rental_in_minutes"].notna()
data=data[mask]

mask=data["delay_at_checkout_in_minutes"].notna()
data=data[mask]
data["delay_with_next_rental"] = data["time_delta_with_previous_rental_in_minutes"] - data["delay_at_checkout_in_minutes"]




# How often are drivers late for the next check-in?  How does it impact the next driver ? 
mask = data["delay_with_next_rental" ] < 0
data_delay = data[mask]

st.markdown(f"### In average, \
            <span style='color:red'>{data_delay.shape[0]/data.shape[0]*100:.1f}%</span> \
            of drivers are late for the next check-in", unsafe_allow_html=True)


# Outliers removal
q1 = data_delay['delay_with_next_rental'].quantile(0.25)
q3 = data_delay['delay_with_next_rental'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

data_delay = data_delay[(data_delay['delay_with_next_rental'] >= lower_bound) 
                  & (data_delay['delay_with_next_rental'] <= upper_bound)]
data_delay["delay_with_next_rental"]=-data_delay["delay_with_next_rental"]

fig = px.histogram(data_delay, x="delay_with_next_rental", nbins=20, title="Distribution of delay in minutes")
st.plotly_chart(fig, use_container_width=True)



# Scope selection
selected_filter = st.radio('Select scope:', ['All', 'Mobile', 'Connect'], horizontal=True)

if selected_filter=='Connect':
    mask = data["checkin_type"]=="connect"
    data_scope = data[mask]

elif selected_filter=='Mobile':
    mask = data["checkin_type"]=="mobile"
    data_scope= data[mask]

else : 
    data_scope = data

#Thresholde selection
Threshold_value = st.slider("Threshold in minutes", min_value=data_scope["time_delta_with_previous_rental_in_minutes"].min(), 
          max_value=(data_scope["time_delta_with_previous_rental_in_minutes"].max()+1), 
          step=1.0)


col1, col2 = st.columns(2)

# Impact analysis of scope and threshold selection 
with col1 :  
    mask = (data_scope["time_delta_with_previous_rental_in_minutes"] >= Threshold_value)
    data_threshold = data_scope[mask]

    st.metric("% of impacted users", 
              f"{(data_scope.shape[0] - data_threshold.shape[0])/data_scope.shape[0]*100:.1f}%", 
              (data_scope.shape[0]-data_threshold.shape[0]),delta_color="off")
    
    fig = px.histogram(data_threshold, x="time_delta_with_previous_rental_in_minutes", nbins=20, title="Distribution of Time Delta between two rental in minutes")
    st.plotly_chart(fig, use_container_width=True)
    
with col2 :

    mask = (data_scope["delay_with_next_rental"] < 0)
    data_scope_delay=data_scope[mask]
    mask = (data_scope["delay_with_next_rental"] < (-Threshold_value))
    data_threshold = data_scope[mask]


    st.metric("% fixed issues", 
              f"{(data_scope_delay.shape[0]-data_threshold.shape[0])/data_scope.shape[0]*100:.1f}%", 
              (data_scope_delay.shape[0]-data_threshold.shape[0]),delta_color="off")
    

    q1 = data_threshold['delay_with_next_rental'].quantile(0.25)
    q3 = data_threshold['delay_with_next_rental'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    data_threshold = data_threshold[(data_threshold['delay_with_next_rental'] >= lower_bound) 
                    & (data_threshold['delay_with_next_rental'] <= upper_bound)]
    data_threshold["delay_with_next_rental"]=-data_threshold["delay_with_next_rental"]

    fig = px.histogram(data_threshold, x="delay_with_next_rental", nbins=20, title="Distribution of delay in minutes")
    st.plotly_chart(fig, use_container_width=True)
    
    