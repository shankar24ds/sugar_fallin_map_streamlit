import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import st_folium

def cust():
    df = pd.read_csv("data/raw/sales_enriched2.csv")
    df = df[['sale_date', 'latitude', 'longitude']].sort_values('sale_date').dropna()
    df['sale_date'] = pd.to_datetime(df['sale_date'], format='%d-%m-%Y')
    m = folium.Map(location=[11.063003, 77.083743], zoom_start=11)
    features = []

    for index, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['longitude'], row['latitude']]
            },
            'properties': {
                'time': row['sale_date'].strftime('%Y-%m-%d'),  # Format date as string
                'popup': f"Date: {row['sale_date'].strftime('%Y-%m-%d')}<br>Latitude: {row['latitude']}<br>Longitude: {row['longitude']}"
            }
        }
        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    TimestampedGeoJson(geojson,
                    period='P10D',  # Animation interval (1 day in this case)
                    add_last_point=True,  # Add the last point after animation
                    auto_play=True).add_to(m)
    return m

def main():
    st.set_page_config(layout="wide")
    st.title("Delivery Plot 2021 & 2022")
    map_ = cust()
    st_folium(map_, width = 1400)

if __name__ == '__main__':
    main()