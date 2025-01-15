# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 21:22:33 2025

@author: Jose Antonio
"""

import pandas as pd
import plotly.express as px

data = pd.read_csv("data/career_change_prediction_dataset.csv")

education_mapping = {
    "High School": 1,
    "Associate Degree": 2,
    "Bachelor's Degree": 3,
    "Master's Degree": 4,
    "Doctorate": 5
}
data['Education Level Numeric'] = data['Education Level'].map(education_mapping)

# Agrupar datos por Campo de Estudio y Nivel de Educación
grouped_data = data.groupby(['Field of Study', 'Education Level']).agg(
    Avg_Job_Satisfaction=('Job Satisfaction', 'mean'),
    Avg_Work_Life_Balance=('Work-Life Balance', 'mean')
).reset_index()

# Añadir la columna numérica del nivel de educación al dataset agrupado
grouped_data['Education Level Numeric'] = grouped_data['Education Level'].map(education_mapping)

# Filtrar datos válidos (eliminar filas con NaN)
grouped_data = grouped_data.dropna(subset=['Avg_Job_Satisfaction', 'Avg_Work_Life_Balance', 'Education Level Numeric'])

# Crear el gráfico de burbujas
# fig = px.scatter(
#     grouped_data,
#     x='Avg_Job_Satisfaction',
#     y='Avg_Work_Life_Balance',  # Tamaño de burbuja basado en nivel de educación
#     color='Field of Study',
#     hover_data=['Field of Study', 'Education Level'],
#     title='Correlation between Job Satisfaction, Work-Life Balance, and Education Level by Field of Study',
#     labels={
#         'Avg_Job_Satisfaction': 'Average Job Satisfaction',
#         'Avg_Work_Life_Balance': 'Average Work-Life Balance'
#     },
#     template='simple_white'
# )

# # Personalizar diseño
# fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='black')))
# fig.update_layout(
#     xaxis=dict(title='Average Job Satisfaction (1-10)', gridcolor='lightgray'),
#     yaxis=dict(title='Average Work-Life Balance (1-10)', gridcolor='lightgray'),
#     title_font=dict(size=18),
#     legend=dict(
#         title='Field of Study',
#         font=dict(size=12),
#         bgcolor='rgba(255,255,255,0.8)',
#         bordercolor='gray',
#         borderwidth=1
#     )
# )


fig = px.scatter(
    grouped_data,
    x='Avg_Job_Satisfaction',
    y='Avg_Work_Life_Balance',
    color='Field of Study',
    # size='Education Level Numeric',  # Aumentar tamaño basado en nivel de educación
    hover_data=['Field of Study'],
    title='Correlation between Job Satisfaction, Work-Life Balance, and Education Level by Field of Study',
    labels={
        'Avg_Job_Satisfaction': 'Average Job Satisfaction (1-10)',
        'Avg_Work_Life_Balance': 'Average Work-Life Balance (1-10)'
    },
    template='simple_white',
    size_max=40
)

# Personalizar diseño
fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='black'), sizemode='area', sizeref=0.2))  # Bolas más grandes
fig.update_layout(
    title=dict(
        text='<b>Balancing Jobs and Life: Insights by Field of Study</b>',
        font=dict(size=22, family='Arial', color='black', weight='bold'),
        x=0.5,  # Centrar título
        xanchor='center'
    ),
    xaxis=dict(
        title='Average Job Satisfaction (1-10)',
        title_font=dict(size=16, family='Arial', color='black'),
        gridcolor='lightgray'
    ),
    yaxis=dict(
        title='Average Work-Life Balance (1-10)',
        title_font=dict(size=16, family='Arial', color='black'),
        gridcolor='lightgray'
    ),
    legend=dict(
        title='Field of Study',
        font=dict(size=12),
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1
    )
)



# fig = px.scatter_3d(
#     grouped_data,
#     x='Avg_Job_Satisfaction',
#     y='Avg_Work_Life_Balance',
#     z='Education Level Numeric',  # Eje Z para nivel de educación
#     color='Field of Study',  # Colores según campo de estudio
#     size='Education Level Numeric',  # Tamaño de burbujas basado en nivel de educación
#     hover_data=['Field of Study', 'Education Level'],  # Información adicional al pasar el ratón
#     title='3D Correlation: Job Satisfaction, Work-Life Balance, and Education Level by Field of Study',
#     labels={
#         'Avg_Job_Satisfaction': 'Average Job Satisfaction',
#         'Avg_Work_Life_Balance': 'Average Work-Life Balance',
#         'Education Level Numeric': 'Education Level'
#     },
#     template='simple_white'
# )

# # Personalizar diseño
# fig.update_layout(
#     scene=dict(
#         xaxis=dict(title='Average Job Satisfaction (1-10)', gridcolor='lightgray', zerolinecolor='gray'),
#         yaxis=dict(title='Average Work-Life Balance (1-10)', gridcolor='lightgray', zerolinecolor='gray'),
#         zaxis=dict(title='Education Level (Numeric)', gridcolor='lightgray', zerolinecolor='gray')
#     ),
#     legend=dict(
#         title='Field of Study',
#         font=dict(size=12),
#         bgcolor='rgba(255,255,255,0.8)',
#         bordercolor='gray',
#         borderwidth=1
#     ),
#     title_font=dict(size=18)
# )


# Mostrar el gráfico
fig.write_html("pregunta2.html")