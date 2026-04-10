import folium
import math


# Данные о городах (с count)
cities_data = [
    {"city": "Санкт-Петербург", "lat": 59.9386, "lon": 30.3141, "count": 150},
    {"city": "Новокузнецк", "lat": 53.7557, "lon": 87.1099, "count": 1},
    {"city": "Нижний Новгород", "lat": 56.3287, "lon": 44.002, "count": 1},
    {"city": "Южно-Сахалинск", "lat": 46.9541, "lon": 142.736, "count": 1},
    {"city": "Воронеж", "lat": 51.672, "lon": 39.1843, "count": 1},
    {"city": "Москва", "lat": 55.7522, "lon": 37.6156, "count": 12},
    {"city": "Владивосток", "lat": 43.1056, "lon": 131.874, "count": 2},
    {"city": "Шлиссельбург", "lat": 59.9371, "lon": 31.028, "count": 1},
    {"city": "Гусиноозёрск", "lat": 51.2833, "lon": 106.5, "count": 2},
    {"city": "Пермь ", "lat": 58.0105, "lon": 56.2502, "count": 1},
    {"city": "Екатеринбург", "lat": 56.8519, "lon": 60.6122, "count": 3},
    {"city": "Чебоксары", "lat": 56.1322, "lon": 47.2519, "count": 1},
    {"city": "Казань", "lat": 55.7887, "lon": 49.1221, "count": 1},
    {"city": "Тихвин", "lat": 59.6451, "lon": 33.5294, "count": 1},
    {"city": "Старый Оскол", "lat": 51.2967, "lon": 37.8417, "count": 1},
    {"city": "Соликамск", "lat": 59.6316, "lon": 56.7685, "count": 2},
    {"city": "Пенза", "lat": 53.2007, "lon": 45.0046, "count": 1},
    {"city": "Кудрово", "lat": 59.907, "lon": 30.512, "count": 1},
    {"city": "Белгород", "lat": 50.6107, "lon": 36.5802, "count": 1},
    {"city": "Ижевск", "lat": 56.8498, "lon": 53.2045, "count": 1},
    {"city": "Курск", "lat": 51.7369, "lon": 36.1924, "count": 1},
    {"city": "Северобайкальск", "lat": 55.63695, "lon": 109.32297, "count": 1},
    {"city": "Оренбург", "lat": 51.7727, "lon": 55.0988, "count": 1},
    {"city": "Псков", "lat": 57.8136, "lon": 28.3496, "count": 1},
    {"city": "Сосновый Бор", "lat": 59.8996, "lon": 29.0857, "count": 1},
    {"city": "Заречный", "lat": 56.811, "lon": 61.3254, "count": 1},
    {"city": "Орёл ", "lat": 52.9651, "lon": 36.0785, "count": 2},
    {"city": "Тюмень", "lat": 57.1522, "lon": 65.5272, "count": 2},
    {"city": "Волгоград", "lat": 48.7194, "lon": 44.5018, "count": 1},
    {"city": "Северодвинск", "lat": 64.5635, "lon": 39.8302, "count": 1},
    {"city": "Бузулук", "lat": 52.7807, "lon": 52.2635, "count": 1},
    {"city": "Новосибирск", "lat": 55.03020, "lon": 82.92043, "count": 2},
]

# Цвета для количества респондентов
color_map = {
    1: "#39FF14",
    2: "#FFD700",
    3: "#FF7F00",
    12: "#FF0000",
    150: "#CC0000",
}

# Города, которые будут подписаны текстом (крупные и удалённые)
cities_with_labels = [
    "Санкт-Петербург",
    "Москва",
    "Екатеринбург",
    "Новосибирск",
    "Южно-Сахалинск",
    "Владивосток",
    "Волгоград",  "Пенза", "Воронеж", "Бузулук",
    "Северодвинск",
    "Новокузнецк",
    "Нижний Новгород", "Белгород",
    "Казань", "Оренбург",
    "Пермь ", "Соликамск",
    "Тюмень", "Орёл ",
    "Гусиноозёрск", "Псков",  "Шлиссельбург" ,
    "Северобайкальск"
]


# СПЕЦИАЛЬНЫЕ города с подписью СВЕРХУ
special_cities_top = ["Новосибирск", "Соликамск", "Орёл ", "Тюмень", "Нижний Новгород", "Москва",  "Шлиссельбург" ,"Бузулук"]

# Нумеруем маленькие города
small_cities = [c for c in cities_data if c["city"] not in cities_with_labels]
small_cities.sort(key=lambda x: x["city"])
number_map = {city["city"]: idx+1 for idx, city in enumerate(small_cities)}

# Легенда для цифр (без знака =)
legend_items = []
for city in small_cities:
    num = number_map[city["city"]]
    legend_items.append(f"{num} {city['city']}")

# Две колонки
half = len(legend_items) // 2 + len(legend_items) % 2
col1 = legend_items[:half]
col2 = legend_items[half:]
legend_html_cols = "<div style='display: flex; justify-content: space-between;'>"
legend_html_cols += "<div style='margin-right: 20px;'>" + "<br>".join(col1) + "</div>"
if col2:
    legend_html_cols += "<div>" + "<br>".join(col2) + "</div>"
legend_html_cols += "</div>"

# Легенда (слева внизу)
legend_html = f'''
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000; background-color: white; padding: 12px; border-radius: 8px; border: 2px solid grey; font-family: Arial; font-size: 11px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); max-width: 320px;">
    <b>Количество респондентов:</b><br>
    <i style="background: #39FF14; width: 20px; height: 20px; display: inline-block;"></i> 1<br>
    <i style="background: #FFD700; width: 20px; height: 20px; display: inline-block;"></i> 2<br>
    <i style="background: #FF7F00; width: 20px; height: 20px; display: inline-block;"></i> 3<br>
    <i style="background: #FF0000; width: 20px; height: 20px; display: inline-block;"></i> 12<br>
    <i style="background: #CC0000; width: 20px; height: 20px; display: inline-block;"></i> 150<br>
    <hr>
    <b>Цифровые метки:</b><br>
    {legend_html_cols}
</div>
'''

# Карта
m = folium.Map(location=[62.0, 100.0], zoom_start=3, tiles='CartoDB positron')

# Добавляем маркеры
for city in cities_data:
    cnt = city["count"]
    radius = 6 + math.log(cnt + 1) * 3
    color = color_map.get(cnt, "#CCCCCC")
    
    if city["city"] in cities_with_labels:
        # КРУПНЫЕ города: кружок
        folium.CircleMarker(
            location=[city["lat"], city["lon"]],
            radius=radius,
            popup=f"<b>{city['city']}</b><br>Респондентов: {cnt}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            weight=2
        ).add_to(m)
        
        # ТЕКСТ: СВЕРХУ для СПЕЦИАЛЬНЫХ, СНИЗУ для остальных
        if city["city"] in special_cities_top:
            # СВЕРХУ точки
            folium.map.Marker(
                [city["lat"], city["lon"]],
                icon=folium.DivIcon(
                    icon_size=(len(city["city"])*8, 20),
                    icon_anchor=(0, radius + 15),  # ← СВЕРХУ
                    html=f'<div style="font-size: 11px; font-weight: bold; color: #000; background-color: rgba(255,255,255,0.9); padding: 2px 5px; border-radius: 3px; white-space: nowrap; box-shadow: 0 1px 3px rgba(0,0,0,0.3);"> {city["city"]} </div>'
                )
            ).add_to(m)
        else:
            # СНИЗУ точки
            folium.map.Marker(
                [city["lat"], city["lon"]],
                icon=folium.DivIcon(
                    icon_size=(len(city["city"])*8, 20),
                    icon_anchor=(0, -radius - 5),  # ← СНИЗУ
                    html=f'<div style="font-size: 11px; font-weight: bold; color: #000; background-color: rgba(255,255,255,0.9); padding: 2px 5px; border-radius: 3px; white-space: nowrap;box-shadow: 0 1px 3px rgba(0,0,0,0.3);">{city["city"]}</div>'
                )
            ).add_to(m)
    else:
        # Маленькие города: цифра внутри кружка
        number = number_map[city["city"]]
        html_circle = f'''
        <div style="
            width: {radius*2}px;
            height: {radius*2}px;
            background-color: {color};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: {max(10, radius-2)}px;
            color: black;
            border: 1px solid #333;
            box-shadow: 0 0 2px rgba(0,0,0,0.5);
        ">{number}</div>
        '''
        folium.Marker(
            location=[city["lat"], city["lon"]],
            icon=folium.DivIcon(
                icon_size=(radius*2, radius*2),
                icon_anchor=(radius, radius),
                html=html_circle
            ),
            popup=f"<b>{city['city']}</b><br>Респондентов: {cnt}"
        ).add_to(m)

# Добавляем легенду
m.get_root().html.add_child(folium.Element(legend_html))

# Сохраняем
m.save('russia_map_final.html')
