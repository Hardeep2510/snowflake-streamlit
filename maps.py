import random
import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from streamlit_folium import folium_static
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt

# Read the CSV file
main_df = pd.read_csv(r"C:\Users\Aashish\Downloads\what_if_output_2024_07_08_15_30_44.csv")

# Function to convert multipolygon strings to DataFrame
def convert_multipolygon(multipolygon):
    # Check if the input is a string
    if not isinstance(multipolygon, str) or multipolygon.startswith('POLYGON'):
        return []  # Return an empty list or some default value

    # Remove 'MULTIPOLYGON (((', ')))', and 'POLYGON Z (('
    multipolygon = (multipolygon.replace('MULTIPOLYGON (((', '')
                                .replace(')))', ''))

    # Split into individual polygons
    polygons = multipolygon.split(')), ((')
    data = []
    for coordinates in polygons:
        coordinates = coordinates.split(",")
        for coordinate in coordinates:
            parts = coordinate.strip().split()
            if len(parts) == 2:  # Ensure there are exactly two parts
                lat, lon = map(float, parts)
                data.append({'lat': lon, 'lon': lat})  # Fixing the lat-lon order
            else:
                print(f"Skipping invalid coordinate: {coordinate.strip()}")
    return data

def convert_lat_lon(multipolygon):
    # Check if the input is a string
    if not isinstance(multipolygon, str) or multipolygon.startswith('POLYGON'):
        return []  # Return an empty list or some default value

    # Remove 'MULTIPOLYGON (((', ')))', and 'POLYGON Z (('
    multipolygon = (multipolygon.replace('MULTIPOLYGON (((', '')
                                .replace(')))', ''))

    # Split into individual polygons
    polygons = multipolygon.split(')), ((')
    data = []
    for coordinates in polygons:
        coordinates = coordinates.split(",")
        for coordinate in coordinates:
            coordinate= coordinate.lstrip()
            cord= [float(i) for i in coordinate.split(" ")]
            data.append(cord)    
    return data

# Extract unique INET_IDs
inet_ids = main_df['INET_ID'].unique().tolist()

# Streamlit app
st.title("Scatterplot of Multiple DataFrames on a Map")

# User selection for INET_ID and plotting library
selected_inet_id = st.selectbox("Select INET_ID", inet_ids)
selected_library = st.selectbox("Select plotting library", ["Pydeck", "Folium", "Plotly", "Matplotlib", 'Streamlit'])

# Filter the main DataFrame based on the selected INET_ID
filtered_df = main_df[main_df['INET_ID'] == selected_inet_id]

# Dictionary to store DataFrames for each row
df_dict = {}

# Convert each row and store in df_dict
for row_index, row in filtered_df['geometry'].items():
    converted_row = convert_multipolygon(row)
    converted_row2 = convert_lat_lon(row)
    if converted_row:  # Only add if the conversion returned data
        df_dict[f"df_{row_index}"] = pd.DataFrame(converted_row)

# Remove entries without valid lat/lon data
df_dict = {k: v for k, v in df_dict.items() if not v.empty}

# Combine all DataFrames with an identifier and their respective colors
combined_df_list = []
for key, df in df_dict.items():
    df['source'] = key  # Add an identifier column
    df['color'] = [[random.randint(0, 255) for _ in range(3)]] * len(df)  # Assign a random color
    combined_df_list.append(df)

if combined_df_list:
    combined_df = pd.concat(combined_df_list)
    polygons = [{
    'coordinates': [[
        [row['lon'], row['lat']] for idx, row in combined_df.iterrows()]]}]
    polygon_df = pd.DataFrame({
        'polygon': polygons,
        # 'color': combined_df['color'].iloc[0].append(100)  # Assuming a single color for the entire polygon
    })

    # Plot based on selected library
    if selected_library == "Pydeck":
        layer = pdk.Layer(
        'PolygonLayer',
        polygon_df,
        stroked = False,
        get_polygon='polygon.coordinates',
        get_fill_color=[100,0,0,100],
        pickable=True,
        # extruded=True,
        # elevation_scale=500,
        # elevation_range=[0, 1000],
    )
        view_state = pdk.ViewState(
        longitude=combined_df['lon'].mean(),
        latitude=combined_df['lat'].mean(),
        zoom=1
    )
        deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": str(selected_inet_id)}
    )
        st.pydeck_chart(deck)

    elif selected_library == "Folium":
        m = folium.Map(location=[combined_df['lat'].mean(), combined_df['lon'].mean()], zoom_start=1)
        # for i, row in combined_df.iterrows():
        # folium.Polygon(locations=[row['lat'], row['lon']], popup=f"{row['lat']}, {row['lon']}").add_to(m)
        folium.Polygon(locations=converted_row2,weight = 6, fill= True).add_to(m)    
        folium_static(m)

    elif selected_library == "Plotly":
        fig = px.scatter_mapbox(combined_df, lat="lat", lon="lon", color="source", zoom=1, height=600)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)

    elif selected_library == "Matplotlib":
        gdf = gpd.GeoDataFrame(combined_df, geometry=gpd.points_from_xy(combined_df.lon, combined_df.lat))
        fig, ax = plt.subplots()
        gdf.plot(ax=ax, marker='o', color='red', markersize=5)
        st.pyplot(fig)
        
    elif selected_library == "Streamlit":
        st.map(combined_df)
    
else:
    st.write("No valid latitude and longitude data available for the selected INET_ID.")
