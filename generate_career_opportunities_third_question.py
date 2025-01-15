# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:28:37 2025

@author: Jose Antonio
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random


# Cargar el dataset
file_path = "data/career_change_prediction_dataset.csv"
data = pd.read_csv(file_path)

# Analizar distribución de Job Opportunities
def analyze_job_opportunities(data):
    job_opportunities_stats = data['Job Opportunities'].describe()
    print("Estadísticas de 'Job Opportunities':")
    print(job_opportunities_stats)

    # Crear un histograma
    fig_hist = px.histogram(
        data,
        x='Job Opportunities',
        nbins=20,
        title="Distribución de 'Job Opportunities'",
        labels={"Job Opportunities": "Oportunidades de Carrera"},
        template="plotly"
    )
    fig_hist.write_html("job_opportunities_distribution.html")
    print("El histograma de 'Job Opportunities' se ha guardado como 'job_opportunities_distribution.html'.")

# Analizar la distribución de Job Opportunities
analyze_job_opportunities(data)

# Calcular estadísticas por género y grupo de edad
data['Age Group'] = pd.cut(data['Age'], bins=[18, 25, 35, 45, 55, 65, 100], labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
gender_age_stats = data.groupby(['Gender', 'Age Group']).agg({
    'Job Opportunities': 'mean',
    'Career Change Interest': 'mean',  # Proporción de interés en cambiar de carrera
    'Age': 'count'
}).rename(columns={'Age': 'Count'}).reset_index()

# Crear un gráfico de burbujas mejorado
fig_bubble = px.scatter(
    gender_age_stats,
    x='Job Opportunities',
    y='Career Change Interest',
    size='Count',
    color='Gender',
    hover_name='Age Group',
    title="Career Change Dynamics: Gender and Age Group Insights",
    labels={
        "Job Opportunities": "Career Opportunities",
        "Career Change Interest": "Proportion of Interest in Changing Careers",
        "Count": "Group size",
        "Gender": "Gender"
    },
    # template="plotly",
    size_max=60,  # Ajuste del tamaño máximo de las burbujas
    color_discrete_map={"Male": "#1f77b4", "Female": "#ff7f0e"}  # Colores distintivos para cada género
)

occupied_positions = []

# Añadir anotaciones para resaltar los puntos más significativos
for i, row in gender_age_stats.iterrows():
    if row['Count'] > 3000:  # Resaltar grupos grandes
        # fig_bubble.add_annotation(
        #     x=row['Job Opportunities'],
        #     y=row['Career Change Interest'],
        #     text=f"{row['Age Group']}<br>{row['Gender']}<br>{int(row['Count'])} personas",
        #     showarrow=True,
        #     arrowhead=2,
        #     ax=40,
        #     ay=-80
        # )
        # Ajustar las anotaciones dependiendo del color o la posición relativa
        if row['Gender'] == 'Male':  # Suponiendo que Male es la bola azul
            fig_bubble.add_annotation(
                x=row['Job Opportunities'],
                y=row['Career Change Interest'],
                text=f"{row['Age Group']}<br>{row['Gender']}<br>{int(row['Count'])} persons",
                showarrow=True,
                arrowhead=2,
                ax=0,  # Desplazamiento horizontal centrado
                ay=80  # Anotación hacia abajo
            )
        elif row['Gender'] == 'Female':  # Suponiendo que Female es la bola naranja
            fig_bubble.add_annotation(
                x=row['Job Opportunities'],
                y=row['Career Change Interest'],
                text=f"{row['Age Group']}<br>{row['Gender']}<br>{int(row['Count'])} persons",
                showarrow=True,
                arrowhead=2,
                ax=0,  # Desplazamiento horizontal centrado
                ay=-80  # Anotación hacia arriba
            )
        

# Mejorar la visualización de los ejes
# fig_bubble.update_layout(
#     xaxis=dict(title="Mean Career Opportunities", gridcolor='lightgrey'),
#     yaxis=dict(title="Proportion of Interest in Changing Careers", gridcolor='lightgrey'),
#     legend=dict(title="Gender"),
#     title_font=dict(size=18)
# )

fig_bubble.update_layout(
    title={
        "text": "<b>Career Change Dynamics: Gender and Age Group Insights</b>",
        "x": 0.5,  # Centrado
        "y": 0.95,
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20, "color": "#000000", "family": "Arial, sans-serif"}
    },
    paper_bgcolor="rgba(245, 247, 250, 1)",  # Fondo suave
    plot_bgcolor="white",  # Fondo del área del gráfico
    margin=dict(l=40, r=40, t=80, b=40),  # Márgenes ajustados
    legend=dict(
        title="Gender",
        font=dict(size=14),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1
    )
)

# Ejes personalizados
fig_bubble.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="lightgray",
    linecolor="gray",
    linewidth=1,
    tickfont=dict(size=12, color="black")
)
fig_bubble.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="lightgray",
    linecolor="gray",
    linewidth=1,
    tickfont=dict(size=12, color="black")
)


# Guardar el gráfico como archivo HTML
fig_bubble.write_html("career_opportunities_bubble_corrected.html")
print("El gráfico de burbujas corregido se ha guardado como 'career_opportunities_bubble_corrected.html'.")
