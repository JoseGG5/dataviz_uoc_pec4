# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:28:37 2025

@author: Jose Antonio
"""

import pandas as pd
import plotly.express as px



file_path = "data/career_change_prediction_dataset.csv"
data = pd.read_csv(file_path)


data['Age Group'] = pd.cut(data['Age'], bins=[18, 25, 35, 45, 55, 65, 100], labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
gender_age_stats = data.groupby(['Gender', 'Age Group']).agg({
    'Job Opportunities': 'mean',
    'Career Change Interest': 'mean',  # Proporción de interés en cambiar de carrera
    'Age': 'count'
}).rename(columns={'Age': 'Count'}).reset_index()

# Gráfico de burbujas
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
    size_max=60,
    color_discrete_map={"Male": "#1f77b4", "Female": "#ff7f0e"}  # Colores distintivos para cada género
)

occupied_positions = []

for i, row in gender_age_stats.iterrows():
    if row['Count'] > 3000:  # Resalto grupos grandes
        if row['Gender'] == 'Male':  # Ajusto annots
            fig_bubble.add_annotation(
                x=row['Job Opportunities'],
                y=row['Career Change Interest'],
                text=f"{row['Age Group']}<br>{row['Gender']}<br>{int(row['Count'])} persons",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=80  # Anotación hacia abajo
            )
        elif row['Gender'] == 'Female':
            fig_bubble.add_annotation(
                x=row['Job Opportunities'],
                y=row['Career Change Interest'],
                text=f"{row['Age Group']}<br>{row['Gender']}<br>{int(row['Count'])} persons",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-80  # Anotación hacia arriba
            )
        

fig_bubble.update_layout(
    title={
        "text": "<b>Career Change Dynamics: Gender and Age Group Insights</b>",
        "x": 0.5,
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

fig_bubble.write_html("career_opportunities_bubble_corrected.html")
