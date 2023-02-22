# Imports 
import streamlit as st
import requests
import json

# Get data from external API
URL = "https://www.tdtchannels.com/lists/tv.json"

# Cache data to avoid multiple calls to the API
@st.cache_data
def obtain_data(URL):
    res = requests.get(URL)
    data = res.json()
    return data

data = obtain_data(URL)

# Save data to json
# with open("tdt.json", "w") as f:
#     json.dump(data, f)

st.title("TDT Channels")

# Get countries
def get_countries(data):
    return [c['name'] for c in data['countries']]

countries = get_countries(data)

# Get ambits
def get_ambits(data, country):
    pais = [c for c in data['countries'] if c['name'] == country][0]
    return [a['name'] for a in pais['ambits']]

# Get options
def get_url(options):
    if options:
        return options[0]['url']
    else:
        return ''


# Get channels
def get_channels(data, country, ambit):
    pais = [c for c in data['countries'] if c['name'] == country][0]
    ambito = [a for a in pais['ambits'] if a['name'] == ambit][0]
    return [{'name': c['name'], 
            'url': get_url(c['options']),
            'logo': c['logo']}
            for c in ambito['channels']]


# Example of how to use the functions:

# Select country via radio
selected_country = st.radio("Select country", countries)

# Get ambits for selected country and select ambit via selectbox
ambits = get_ambits(data, selected_country)
selected_ambit = st.selectbox("Select ambit", ambits)

# Get channels for selected country and ambit and show them
channels = get_channels(data, selected_country, selected_ambit)
for c in channels:
    imagen = (f"![{c['name']}]({c['logo']})")
    st.markdown(f"[{imagen}]({c['url']})")