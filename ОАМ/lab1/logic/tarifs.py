import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

# Загружаем данные
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
file_path = os.path.join(BASE_DIR, "..", "source", "Tariff_plans_change.csv")
df = pd.read_csv(file_path, na_values=["$null$"])

# Преобразуем даты
df['START_DTTM'] = pd.to_datetime(df['START_DTTM'])
df['END_DTTM'] = pd.to_datetime(df['END_DTTM'])

# Сортировка по SUBSCRIBER_ID и START_DTTM
df_sorted = df.sort_values(['SUBSCRIBER_ID', 'START_DTTM'])

# Создаем переходы между тарифами
transitions = df_sorted.groupby('SUBSCRIBER_ID').apply(
    lambda x: x.assign(next_plan = x['TARIFF_PLAN_ID'].shift(-1))
).reset_index(drop=True)

# Фильтруем только реальные переходы и убираем переходы в себя
transitions = transitions[
    (transitions['next_plan'].notna()) & 
    (transitions['TARIFF_PLAN_ID'] != transitions['next_plan'])
]

# Считаем потоки между тарифами
flows = transitions.groupby(['TARIFF_PLAN_ID', 'next_plan']).size().reset_index(name='n')
flows = flows.rename(columns={'TARIFF_PLAN_ID': 'from', 'next_plan': 'to'})
flows = flows.sort_values('n', ascending=False)

# ДОБАВЛЯЕМ МИНИМАЛЬНУЮ ТОЛЩИНУ ДЛЯ МАЛЫХ ПОТОКОВ
min_thickness = 3
max_thickness = 30
min_transitions = flows['n'].min()
max_transitions = flows['n'].max()

# Масштабируем значения для визуализации
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
print(f"\nТОП-10 наибольших потоков миграции:")
print("-" * 40)
for i, row in flows.head(10).iterrows():
    print(f"{row['from']} → {row['to']} : {row['n']} переходов")

# Создаем узлы для Sankey
all_tariffs = pd.unique(flows[['from', 'to']].values.ravel('K'))
nodes = pd.DataFrame({'name': all_tariffs})

# Сортируем узлы для последовательного отображения
nodes = nodes.sort_values('name').reset_index(drop=True)

# Создаем связи для Sankey
flows_links = flows.copy()
flows_links['source'] = flows_links['from'].map(lambda x: nodes[nodes['name'] == x].index[0])
flows_links['target'] = flows_links['to'].map(lambda x: nodes[nodes['name'] == x].index[0])

node_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
]

link_colors = []
for source_idx in flows_links['source']:
    base_color = node_colors[source_idx % len(node_colors)]
    link_colors.append(f"rgba{tuple(int(base_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.4,)}")

# Создаем улучшенную Sankey диаграмму
fig = go.Figure(go.Sankey(
    arrangement="perpendicular", 
    node=dict(
        pad=80,
        thickness=25,
        line=dict(color="black", width=2),
        label=[f"Тариф {name}" for name in nodes['name']],
        color=[node_colors[i % len(node_colors)] for i in range(len(nodes))],
        x=[0] * len(nodes),
        y=[i / max(1, len(nodes)-1) for i in range(len(nodes))],
    ),
    link=dict(
        source=flows_links['source'].tolist(),
        target=flows_links['target'].tolist(),
        value=flows_links['scaled_n'].tolist(),
        color=link_colors,
        hovertemplate='<b>%{source.label}</b> → <b>%{target.label}</b><br>'
                     'Количество переходов: <b>%{customdata}</b><extra></extra>',
        customdata=flows_links['n'].tolist()
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

# Анализ малых потоков
small_flows = flows[flows['n'] <= 10]
if len(small_flows) > 0:
    print(f"\nМалые потоки (≤ 10 переходов): {len(small_flows)}")
    print("Они усилены для видимости на диаграмме")

print(f"\nДиапазон переходов: {min_transitions} - {max_transitions}")
print(f"Масштабирование: {min_thickness}px - {max_thickness}px")

print("\nАнализ завершен!")