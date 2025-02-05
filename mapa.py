# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:41:41 2025

@author: J_Aliaga
"""
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import folium
from streamlit_folium import folium_static

# Conexión a la base de datos PostgreSQL
engine = create_engine('postgresql://postgres:openpgpwd@localhost:5432/unodc')

# Función para crear un mapa con capas
def create_base_map():
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Agregar capas de mapas
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='© Esri World Imagery',
        name='Esri WorldImagery',
        overlay=False
    ).add_to(m)
    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='© OpenTopoMap contributors',
        name='OpenTopoMap',
        overlay=False
    ).add_to(m)
    
    folium.LayerControl().add_to(m)

    return m

# Función para agregar marcadores de la capa base
def add_base_markers(m, base_data):
    density_colors = {1: 'white', 2: 'yellow', 3: 'green'}
    for _, row in base_data.iterrows():
        folium.RegularPolygonMarker(
            location=[row['latitude'], row['longitude']],
            number_of_sides=6,
            radius=10,
            popup=row['cod_hex'],
            fill_color=density_colors.get(row['densiti'], 'gray'),
            fill_opacity=0.7,
            fill=True
        ).add_to(m)
    return m

# Función para agregar marcadores adicionales
def add_additional_markers(m, points_data):
    for _, row in points_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='red'
        ).add_to(m)
    return m

# **************** CONSULTAS
# Consulta a la base de datos para la capa base
query_base = "SELECT coordy as latitude, coordx as longitude, cod_hex, densidad, densiti FROM parcelas"
base_data = pd.read_sql(query_base, engine)

# Consulta a la base de datos para los puntos adicionales
query_points = "SELECT  latitud_y as latitude, longitud_x as longitude, sup_muestra, densidad FROM unodc_parcelas WHERE seleccionado = 1"
points_data = pd.read_sql(query_points, engine)

# **************** fin consultas

# Crear el mapa base
map_object = create_base_map()
map_object.location = [base_data['latitude'].mean(), base_data['longitude'].mean()]
map_object.zoom_start = 10

# Agregar los marcadores de la capa base
map_object = add_base_markers(map_object, base_data)

# Agregar los puntos adicionales al mapa
map_object = add_additional_markers(map_object, points_data)

# Mostrar el mapa en Streamlit con tamaño ampliado
# folium_static(map_object, width=800, height=600)

folium_static(map_object)
