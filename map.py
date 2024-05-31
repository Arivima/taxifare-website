import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime
import requests

# Initializing the Streamlit app
st.title("New York taxi estimator")
st.markdown('''
##### Please select date, time and number of passengers for the ride
''')
# Asking for user input : date
d = st.date_input(
    "Input date of the ride",
    datetime.date.today(),
    datetime.date.today()
    )
# Asking for user input : time
current_time = datetime.datetime.now().time()
t = st.time_input(
    "Input time of the ride",
    current_time
    )
date_and_time = datetime.datetime.combine(d, t)
# Asking for user input : number of passengers
passengers = st.number_input('Input number of passengers', 0, 8,1,1)


# Asking for user input : pickup and dropoff points
st.markdown('''
##### click the map to select pickup and dropoff locations
''')

# Setting initial map location
center_lat, center_lon = (40.5 + 40.9 ) / 2, (-74.3 + -73.7) / 2
bounds = {
    'lat' : {
        'min' : 40.5,
        'max' : 40.9
    },
    'lng' : {
        'min' : -74.3,
        'max' : -73.7
    }
}

# Initialize session state for markers
if 'pickup' not in st.session_state:
    st.session_state.pickup = None
if 'dropoff' not in st.session_state:
    st.session_state.dropoff = None

# Create a folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Draw bounds
southwest = (bounds['lat']['min'], bounds['lng']['min'])
northeast = (bounds['lat']['max'], bounds['lng']['max'])
rectangle_bounds = [southwest, northeast]
folium.Rectangle(
    bounds=rectangle_bounds,
    color='red',
    fill=True,
    fill_opacity=0).add_to(m)

# Add existing markers if they exist
if st.session_state.pickup:
    folium.Marker(
        location=st.session_state.pickup,
        popup='Pickup Location',
        icon=folium.Icon(color='green')
    ).add_to(m)

if st.session_state.dropoff:
    folium.Marker(
        location=st.session_state.dropoff,
        popup='Dropoff Location',
        icon=folium.Icon(color='red')
    ).add_to(m)

# Render the map and handle clicks
map_data = st_folium(m, width=700, height=500)

# Update session state based on the last clicked location
if map_data and 'last_clicked' in map_data and map_data['last_clicked'] is not None:
    last_clicked = map_data['last_clicked']

    if last_clicked['lat'] < bounds['lat']['min'] \
    or last_clicked['lat'] > bounds['lat']['max'] \
    or last_clicked['lng'] < bounds['lng']['min'] \
    or last_clicked['lng'] > bounds['lng']['max']:
        if st.session_state.pickup is None:
            st.warning('pickup point out of bounds')
        else:
            st.warning('dropoff point out of bounds')

    if st.session_state.pickup is None:
        st.session_state.pickup = (last_clicked['lat'], last_clicked['lng'])
    elif st.session_state.dropoff is None:
        st.session_state.dropoff = (last_clicked['lat'], last_clicked['lng'])
    else:
        st.session_state.pickup = (last_clicked['lat'], last_clicked['lng'])
        st.session_state.dropoff = None

    # Re-render the map with updated markers
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    if st.session_state.pickup:
        folium.Marker(
            location=st.session_state.pickup,
            popup='Pickup Location',
            icon=folium.Icon(color='green')
        ).add_to(m)
    if st.session_state.dropoff:
        folium.Marker(
            location=st.session_state.dropoff,
            popup='Dropoff Location',
            icon=folium.Icon(color='red')
        ).add_to(m)
    st_folium(m, width=700, height=500)

# Display the coordinates
pickup = st.session_state.pickup
dropoff = st.session_state.dropoff

# if pickup:
#     st.write(f"Pickup Location: {pickup[0]}, {pickup[1]}")
# if dropoff:
#     st.write(f"Dropoff Location: {dropoff[0]}, {dropoff[1]}")

# API call
try:
    params = {
        'pickup_datetime':date_and_time,
        'pickup_longitude':pickup[0],
        'pickup_latitude':pickup[1],
        'dropoff_longitude':dropoff[0],
        'dropoff_latitude':dropoff[1],
        'passenger_count':passengers
    }
    url = 'https://taxifare.lewagon.ai/predict'

    response = requests.get(url, params=params)
    fare = response.json()
    st.write('For a ride on ', d, 'at', t, 'with', passengers, 'passengers')
    st.write('expected fare :', round(fare['fare'], 2))
except:
    st.write('For a ride on ', d, 'at', t, 'with', passengers, 'passengers')
