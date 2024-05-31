import streamlit as st

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

import datetime

d = st.date_input(
    "Input date of the ride",
    datetime.date.today()
    )
t = st.time_input(
    "Input time of the ride",
    # datetime.time.now().strftime("%H:%M")
    )

passengers = st.number_input('Input number of passengers', 0, 8,1,1)

st.write('For a ride on ', d, 'at', t)
st.write('with', passengers, 'passengers')


import folium

from streamlit_folium import st_folium

fg = folium.FeatureGroup(name="markers")

pickup = dropoff = 0, 0

map = folium.Map(
    location=[(40.5 + 40.9 ) / 2, (-74.3 + -73.7) / 2],
    zoom_start=10
    )

fg.add_child(
    folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")
)

st_data = st_folium(
    map,
    feature_group_to_add=fg,
    width=300,
    height=300,
    )
# if st.button('confirm pickup'):
#     pickup = st_data['last_clicked']['lat'], st_data['last_clicked']['lng']

# if st.button('confirm dropoff'):
#     dropoff = st_data['last_clicked']['lat'], st_data['last_clicked']['lng']


# if pickup:
#     fg.add_child(
#         folium.Marker(
#             [pickup[0], pickup[1]],
#             popup="pickup",
#             tooltip="pickup",
#         )
#     )

# if dropoff:
#     fg.add_child(
#         folium.Marker(
#             [dropoff[0], dropoff[1]],
#             popup="dropoff", tooltip="dropoff"
#         )
#     )



st.write('pickup', pickup, 'dropoff' ,dropoff)



'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
