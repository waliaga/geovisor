# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 10:41:41 2025

@author: J_Aliaga
"""
import os
import streamlit as st
import pandas as pd
import json

# Lee el archivo JSON completo y muestra su estructura
# with open('C:/py-streamlit/geovisor/static/geojson/unodc_parcelas_json.json', 'r') as f:
# with open('/static/geojson/unodc_parcelas_json.json', 'r') as f:
    #data = json.load(f)

# Obtiene la ruta del archivo JSON relativo al directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'static', 'geojson', 'unodc_parcelas_json.json')

# Lee el archivo JSON completo y muestra su estructura
# Lee el archivo JSON completo y muestra su estructura
with open(file_path, 'r') as f:
    data = json.load(f)

# Accede a la clave 'unodc_parcelas' y conviértelo en un DataFrame
df = pd.DataFrame(data['unodc_parcelas'])

# Muestra los nombres de las columnas y las primeras filas del DataFrame
# st.write("Columnas del DataFrame:", df.columns)
# st.write("Primeras filas del DataFrame:", df.head())

# Selecciona únicamente las columnas de latitud y longitud si están presentes
if 'latitud_y' in df.columns and 'longitud_x' in df.columns:
    df = df[['latitud_y', 'longitud_x']]
    # Renombra columnas para que sean compatibles con st.map()
    df.columns = ['lat', 'lon']
    
    # Crea un mapa con los datos
    st.map(df)
else:
    st.write("Las columnas 'latitud_y' y 'longitud_x' no están presentes en el DataFrame.")