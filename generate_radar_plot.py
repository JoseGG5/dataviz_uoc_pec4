# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 20:14:30 2025

@author: Jose Antonio
"""


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import shap


file_path = "data/career_change_prediction_dataset.csv"
data = pd.read_csv(file_path)


categorical_mappings = {
    'Industry Growth Rate': {'Low': 1, 'Medium': 2, 'High': 3},
    'Family Influence': {'Low': 1, 'Medium': 2, 'High': 3}
}
for column, mapping in categorical_mappings.items():
    if column in data.columns:
        data[column] = data[column].map(mapping)

# Preprocessing
features = ['Job Opportunities', 'Salary', 'Work-Life Balance', 'Job Security', 'Industry Growth Rate', 'Family Influence']
data = data.dropna(subset=features + ['Career Change Interest']) 
X = data[features]
y = data['Career Change Interest']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Modelo para ver importancia de features
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
feature_importances = model.feature_importances_
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# Crear un gráfico de radar para visualizar la importancia
categories = importance_df['Feature'].tolist()
values = importance_df['Importance'].tolist()
values.append(values[0])  # Cerrar el gráfico del radar
categories.append(categories[0])

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    fillcolor='rgba(0, 128, 255, 0.4)',  # Color de relleno con opacidad
    line_color='blue',  # Color del borde
    line_width=2,  # Grosor del borde
    name='Importance'
))

fig_radar.update_layout(
    title={
        'text': "<b>Key Factors Driving Career Changes</b>",
        'x': 0.48,  # Centrado
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 20,
            "color": "#000000",
            "family": "Arial, sans-serif"
        }
    },
    polar=dict(
        bgcolor='rgba(240, 248, 255, 0.9)',  # Fondo de la trama polar
        radialaxis=dict(
            visible=True,
            showgrid=True,
            gridcolor='lightgray',  # Color de la cuadrícula
            gridwidth=1,
            range=[0, 0.5],  # Rango del eje
            tickfont=dict(size=12, color='black'),  # Fuente de las etiquetas
        ),
        angularaxis=dict(
            showline=True,
            linecolor='gray',  # Color de los ejes angulares
            linewidth=1,
            tickfont=dict(size=14, color='darkblue'),  # Fuente de las categorías
        )
    ),
    showlegend=True,
    legend=dict(
        font=dict(size=12, color='darkblue'),
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1
    )
)

fig_radar.write_html("career_change_factors_radar.html")
print("El gráfico de radar de los factores se ha guardado como 'career_change_factors_radar.html'.")