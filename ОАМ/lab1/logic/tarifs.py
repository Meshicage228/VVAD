import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
file_path = os.path.join(BASE_DIR, "..", "source", "Tariff_plans_change.csv")
df = pd.read_csv(file_path, na_values=["$null$"])

df['START_DTTM'] = pd.to_datetime(df['START_DTTM'])
df['END_DTTM'] = pd.to_datetime(df['END_DTTM'])

df_sorted = df.sort_values(['SUBSCRIBER_ID', 'START_DTTM'])

transitions = df_sorted.groupby('SUBSCRIBER_ID').apply(
    lambda x: x.assign(next_plan=x['TARIFF_PLAN_ID'].shift(-1))
).reset_index(drop=True)

transitions = transitions[
    (transitions['next_plan'].notna()) &
    (transitions['TARIFF_PLAN_ID'] != transitions['next_plan'])
]

flows = transitions.groupby(['TARIFF_PLAN_ID', 'next_plan']).size().reset_index(name='n')
flows = flows.rename(columns={'TARIFF_PLAN_ID': 'from', 'next_plan': 'to'})
flows = flows.sort_values('n', ascending=False)

min_thickness = 3
max_thickness = 30
min_transitions = flows['n'].min()
max_transitions = flows['n'].max()

def scale_thickness(value):
    if max_transitions == min_transitions:
        return min_thickness
    scaled = min_thickness + (value - min_transitions) * (max_thickness - min_thickness) / (max_transitions - min_transitions)
    return max(min_thickness, scaled)

flows['scaled_n'] = flows['n'].apply(scale_thickness)

print("="*50)
print("АНАЛИЗ ПЕРЕХОДОВ МЕЖДУ ТАРИФНЫМИ ПЛАНАМИ")
print("="*50)

print(f"\nВсего переходов за период: {len(transitions)}")
print(f"\nВсе потоки миграции:")
print("-" * 40)
for i, row in flows.iterrows():
    print(f"{row['from']} → {row['to']} : {row['n']} переходов")

unique_tariffs = sorted(pd.unique(flows[['from', 'to']].values.ravel('K')))

nodes = pd.DataFrame({
    'name': [f"Текущий {t}" for t in unique_tariffs] + [f"Следующий {t}" for t in unique_tariffs]
})

flows_links = flows.copy()
flows_links['source'] = flows_links['from'].map(lambda x: unique_tariffs.index(x))
flows_links['target'] = flows_links['to'].map(lambda x: unique_tariffs.index(x) + len(unique_tariffs))

node_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'
]
link_colors = [node_colors[int(f)-1 % len(node_colors)] for f in flows_links['from']]

x_positions = [0]*len(unique_tariffs) + [1]*len(unique_tariffs)
y_positions = [i/(len(unique_tariffs)-1) for i in range(len(unique_tariffs))]*2

fig = go.Figure(go.Sankey(
    arrangement="freeform",
    node=dict(
        pad=50,
        thickness=25,
        line=dict(color="black", width=1),
        label=nodes['name'],
        color=node_colors * 2,
        x=x_positions,
        y=y_positions
    ),
    link=dict(
        source=flows_links['source'],
        target=flows_links['target'],
        value=flows_links['scaled_n'],
        color=link_colors,
        hovertemplate='<b>%{source.label}</b> → <b>%{target.label}</b><br>'
                     'Количество переходов: <b>%{value}</b><extra></extra>'
    )
))

fig.update_layout(
    title_text="<b>Миграция между тарифными планами</b><br>",
    title_x=0.5,
    font_size=14,
    width=1400,
    height=900,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

output_dir = os.path.join(BASE_DIR, "visualisation")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "sankey_diagram.html")
fig.write_html(output_file)

print(f"\nИсправленная Sankey-диаграмма сохранена: {output_file}")

small_flows = flows[flows['n'] <= 10]
if len(small_flows) > 0:
    print(f"\nМалые потоки (≤ 10 переходов): {len(small_flows)}")
    print("Они усилены для видимости на диаграмме")

print(f"\nДиапазон переходов: {min_transitions} - {max_transitions}")
print(f"Масштабирование: {min_thickness}px - {max_thickness}px")

print("\nАнализ завершен!")