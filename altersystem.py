# -*- coding: utf-8 -*-
"""AlterSystem

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bk1bAC_9QTfeEdXuoGSG3gvxQwi-GgN9
"""

import warnings
warnings.filterwarnings('ignore')

!pip install fiona
!pip install folium
!pip install geopandas
import pandas as pd
import fiona
import folium
import geopandas as gpd

fname = "/content/Dataset1.csv"

fiona.listlayers(fname)

!pip install folium matplotlib mapclassify

import pandas as pd
import geopandas as gpd
import folium

# Load your rainfall dataset
# Replace 'your_dataset.csv' with the actual file name
df = pd.read_csv('/content/Dataset1.csv')

# Create an 'Alerts' column based on 'ANNUAL' values
df['Alerts'] = pd.cut(df['ANNUAL'], bins=[0, 500, 1000, float('inf')],
                      labels=['Less Rainfall', 'Moderate Rainfall', 'Heavy Rainfall'])

# Add 'No Data' to the categories of 'Alerts'
df['Alerts'] = pd.Categorical(df['Alerts'], categories=['Less Rainfall', 'Moderate Rainfall', 'Heavy Rainfall', 'No Data'])

# Replace NaN values in 'Alerts' with a default category (e.g., 'No Data')
df['Alerts'].fillna('No Data', inplace=True)

# Assuming your dataset has columns like 'Latitude', 'Longitude', and 'Alerts'
geometry = gpd.points_from_xy(df['Longitude'], df['Latitude'])
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Create a folium map centered at India
m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Define marker colors for each alert level
colors = {'Heavy Rainfall': 'red', 'Moderate Rainfall': 'orange', 'Less Rainfall': 'green', 'No Data': 'gray'}

# Add markers to the map
for index, row in gdf.iterrows():
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                        radius=5,
                        color=colors[row['Alerts']],
                        fill=True,
                        fill_color=colors[row['Alerts']],
                        fill_opacity=0.7,
                        popup=f"Subdivision: {row['SUBDIVISION']}, Year: {row['YEAR']}, Alert: {row['Alerts']}").add_to(m)

# Display the map
m