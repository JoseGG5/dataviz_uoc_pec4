# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:59:37 2025

@author: Jose Antonio
"""

import pandas as pd
from pyvis.network import Network

# Cargar tu archivo CSV
df = pd.read_csv('data/career_change_prediction_dataset.csv')

field_col = 'Field of Study'
occupation_col = 'Current Occupation'

transition_counts = df.groupby([field_col, occupation_col]).size().reset_index(name='count')  # Conteo transiciones


net = Network(height='1200px', width='100%', notebook=False, directed=True)

top_transitions = transition_counts.nlargest(30, 'count')  # TOP 30

for _, row in top_transitions.iterrows():
    field = row[field_col]
    occupation = row[occupation_col]
    count = row['count']

    net.add_node(field, label=field, color='blue', size=25, title=f"Field of Study: {field}", alpha=0.5)
    net.add_node(occupation, label=occupation, color='orange', size=25, title=f"Current Occupation: {occupation}", alpha=0.5)

    net.add_edge(field, occupation, value=count, width=count / 2, title=f"Count: {count}", color='black')

# Física de la red
net.set_options("""
var options = {
  "nodes": {
    "shape": "dot",
    "size": 16
  },
  "edges": {
    "arrows": {
      "to": {
        "enabled": true
      }
    },
    "color": {
      "inherit": true
    },
    "smooth": {
      "enabled": true,
      "type": "dynamic"
    }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -20000,
      "springLength": 250
    },
    "minVelocity": 0.75
  }
}
""")

html_path = "top_30_transitions_graph.html"
net.save_graph(html_path)

# Añado leyenda y título al html

legend_html = """
<div style="position: absolute; top: 85px; left: 10px; background-color: white; border: 1px solid black; padding: 10px; z-index: 1000;">
    <b>Legend:</b>
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li><span style="background-color: blue; padding: 5px; margin-right: 5px; display: inline-block;"></span> Field of Study</li>
        <li><span style="background-color: orange; padding: 5px; margin-right: 5px; display: inline-block;"></span> Current Occupation</li>
    </ul>
</div>
"""

title_html = """
<h1 style="text-align: center; margin-top: 20px; font-size: 20px; font-weight: bold;">Career Transitions: Top 30 Patterns</h1>
"""


with open(html_path, "r") as file:
    html_content = file.read()


html_content = html_content.replace("<body>", f"<body>\n{title_html}\n{legend_html}")


with open(html_path, "w") as file:
    file.write(html_content)

print(f"Graph with title and legend saved to {html_path}")