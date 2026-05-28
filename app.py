import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
import csv
import os
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
import folium
from streamlit_folium import st_folium
warnings.filterwarnings('ignore')
LOG_FILE = 'predictions_log.csv'
if os.path.exists(LOG_FILE):
    try:
        pd.read_csv(LOG_FILE)
    except:
        os.remove(LOG_FILE)
TAIPEI_BOUNDS = {
    'lat_min': 24.90,
    'lat_max': 25.20,
    'lon_min': 121.40,
    'lon_max': 121.65
}

MRT_STATIONS = [
    {'name': 'Taipei Nangang Exhibition Center', 'lat': 25.05670, 'lon': 121.61690},
    {'name': 'Nangang Software Park', 'lat': 25.05840, 'lon': 121.60940},
    {'name': 'Donghu', 'lat': 25.06850, 'lon': 121.60620},
    {'name': 'Huzhou', 'lat': 25.06890, 'lon': 121.60070},
    {'name': 'Dahu Park', 'lat': 25.08080, 'lon': 121.60050},
    {'name': 'Neihu', 'lat': 25.08250, 'lon': 121.58670},
    {'name': 'Wende', 'lat': 25.07920, 'lon': 121.57990},
    {'name': 'Gangqian', 'lat': 25.08290, 'lon': 121.57320},
    {'name': 'Xihu', 'lat': 25.08310, 'lon': 121.56660},
    {'name': 'Jiannan Road', 'lat': 25.08270, 'lon': 121.55340},
    {'name': 'Dazhi', 'lat': 25.07960, 'lon': 121.54550},
    {'name': 'Songshan Airport', 'lat': 25.06420, 'lon': 121.55210},
    {'name': 'Zhongshan Junior High School', 'lat': 25.05860, 'lon': 121.54440},
    {'name': 'Nanjing Fuxing', 'lat': 25.05180, 'lon': 121.54460},
    {'name': 'Zhongxiao Fuxing', 'lat': 25.04190, 'lon': 121.54390},
    {'name': 'Daan', 'lat': 25.03320, 'lon': 121.54350},
    {'name': 'Technology Building', 'lat': 25.02590, 'lon': 121.54340},
    {'name': 'Liuzhangli', 'lat': 25.02110, 'lon': 121.54470},
    {'name': 'Linguang', 'lat': 25.01820, 'lon': 121.54900},
    {'name': 'Xinhai', 'lat': 25.00530, 'lon': 121.54830},
    {'name': 'Wanfang Hospital', 'lat': 24.99950, 'lon': 121.55710},
    {'name': 'Wanfang Community', 'lat': 24.99860, 'lon': 121.56800},
    {'name': 'Muzha', 'lat': 24.98980, 'lon': 121.57310},
    {'name': 'Taipei Zoo', 'lat': 24.99820, 'lon': 121.58130},
    {'name': 'Tamsui', 'lat': 25.16930, 'lon': 121.44630},
    {'name': 'Hongshulin', 'lat': 25.15240, 'lon': 121.46080},
    {'name': 'Zhuwei', 'lat': 25.13870, 'lon': 121.46240},
    {'name': 'Guandu', 'lat': 25.12500, 'lon': 121.46690},
    {'name': 'Zhongyi', 'lat': 25.11700, 'lon': 121.47300},
    {'name': 'Fuxinggang', 'lat': 25.10670, 'lon': 121.47900},
    {'name': 'Beitou', 'lat': 25.12660, 'lon': 121.49670},
    {'name': 'Qiyan', 'lat': 25.12250, 'lon': 121.50040},
    {'name': 'Qilian', 'lat': 25.11670, 'lon': 121.50260},
    {'name': 'Shipai', 'lat': 25.10850, 'lon': 121.51130},
    {'name': 'Mingde', 'lat': 25.10270, 'lon': 121.51750},
    {'name': 'Zhishan', 'lat': 25.09570, 'lon': 121.52240},
    {'name': 'Shilin', 'lat': 25.09250, 'lon': 121.52680},
    {'name': 'Jiantan', 'lat': 25.08180, 'lon': 121.52140},
    {'name': 'Yuanshan', 'lat': 25.07270, 'lon': 121.52040},
    {'name': 'Minquan West Road', 'lat': 25.06360, 'lon': 121.52120},
    {'name': 'Shuanglian', 'lat': 25.05750, 'lon': 121.52150},
    {'name': 'Zhongshan', 'lat': 25.05310, 'lon': 121.52120},
    {'name': 'Taipei Main Station', 'lat': 25.04770, 'lon': 121.51700},
    {'name': 'NTU Hospital', 'lat': 25.04080, 'lon': 121.51870},
    {'name': 'Chiang Kai-shek Memorial Hall', 'lat': 25.03470, 'lon': 121.52080},
    {'name': 'Dongmen', 'lat': 25.03340, 'lon': 121.52860},
    {'name': 'Daan Park', 'lat': 25.03000, 'lon': 121.53680},
    {'name': 'Xinyi Anhe', 'lat': 25.03310, 'lon': 121.55250},
    {'name': 'Taipei 101/World Trade Center', 'lat': 25.03360, 'lon': 121.56070},
    {'name': 'Xindian', 'lat': 24.95880, 'lon': 121.53690},
    {'name': 'Xindian District Office', 'lat': 24.96760, 'lon': 121.54070},
    {'name': 'Qizhang', 'lat': 24.97700, 'lon': 121.54110},
    {'name': 'Dapinglin', 'lat': 24.98490, 'lon': 121.54220},
    {'name': 'Jingmei', 'lat': 24.99290, 'lon': 121.54180},
    {'name': 'Wanlong', 'lat': 25.00190, 'lon': 121.53960},
    {'name': 'Gongguan', 'lat': 25.01230, 'lon': 121.53410},
    {'name': 'Taipower Building', 'lat': 25.01900, 'lon': 121.53040},
    {'name': 'Guting', 'lat': 25.02610, 'lon': 121.52790},
    {'name': 'Xiaonanmen', 'lat': 25.03700, 'lon': 121.51290},
    {'name': 'Ximen', 'lat': 25.04250, 'lon': 121.50800},
    {'name': 'Longshan Temple', 'lat': 25.03620, 'lon': 121.49610},
    {'name': 'Jiangzicui', 'lat': 25.03090, 'lon': 121.47940},
    {'name': 'Xinpu', 'lat': 25.02570, 'lon': 121.46750},
    {'name': 'Banqiao', 'lat': 25.01490, 'lon': 121.46370},
    {'name': 'Fuzhong', 'lat': 25.00850, 'lon': 121.45520},
    {'name': 'Far Eastern Hospital', 'lat': 24.99770, 'lon': 121.45160},
    {'name': 'Haishan', 'lat': 24.98800, 'lon': 121.45100},
    {'name': 'Tucheng', 'lat': 24.97840, 'lon': 121.44660},
    {'name': 'Yongning', 'lat': 24.96860, 'lon': 121.44070},
    {'name': 'Dingpu', 'lat': 24.95640, 'lon': 121.42350},
    {'name': 'Nanshijiao', 'lat': 24.99050, 'lon': 121.50700},
    {'name': 'Jingan', 'lat': 24.99920, 'lon': 121.50230},
    {'name': 'Yongan Market', 'lat': 25.00790, 'lon': 121.50870},
    {'name': 'Dingxi', 'lat': 25.01620, 'lon': 121.51620},
    {'name': 'Huilong', 'lat': 25.02180, 'lon': 121.42520},
    {'name': 'Danfeng', 'lat': 25.02780, 'lon': 121.42890},
    {'name': 'Fu Jen University', 'lat': 25.03390, 'lon': 121.43320},
    {'name': 'Xinzhuang', 'lat': 25.04060, 'lon': 121.44920},
    {'name': 'Touqianzhuang', 'lat': 25.04570, 'lon': 121.46010},
    {'name': 'Xianse Temple', 'lat': 25.05270, 'lon': 121.46720},
    {'name': 'Sanchong', 'lat': 25.06050, 'lon': 121.47610},
    {'name': 'Cailiao', 'lat': 25.06330, 'lon': 121.48300},
    {'name': 'Taipei Bridge', 'lat': 25.06340, 'lon': 121.49590},
    {'name': 'Daqiaotou', 'lat': 25.06310, 'lon': 121.50670},
    {'name': 'Luzhou', 'lat': 25.09130, 'lon': 121.46400},
    {'name': 'Sanmin Senior High School', 'lat': 25.08420, 'lon': 121.47030},
    {'name': 'St. Ignatius High School', 'lat': 25.07810, 'lon': 121.47570},
    {'name': 'Sanhe Junior High School', 'lat': 25.07520, 'lon': 121.48510},
    {'name': 'Sanchong Elementary School', 'lat': 25.06960, 'lon': 121.49260},
    {'name': 'Zhongshan Elementary School', 'lat': 25.06440, 'lon': 121.52650},
    {'name': 'Xingtian Temple', 'lat': 25.06520, 'lon': 121.53350},
    {'name': 'Zhongxiao Xinsheng', 'lat': 25.03950, 'lon': 121.53410},
    {'name': 'Kunyang', 'lat': 25.05100, 'lon': 121.59150},
    {'name': 'Houshanpi', 'lat': 25.04370, 'lon': 121.58090},
    {'name': 'Yongchun', 'lat': 25.04040, 'lon': 121.57390},
    {'name': 'Taipei City Hall', 'lat': 25.04070, 'lon': 121.56480},
    {'name': 'Sun Yat-Sen Memorial Hall', 'lat': 25.04010, 'lon': 121.55720},
    {'name': 'Zhongxiao Dunhua', 'lat': 25.04100, 'lon': 121.54990},
    {'name': 'Shandao Temple', 'lat': 25.04400, 'lon': 121.52850},
    {'name': 'Xiaobitan', 'lat': 24.97220, 'lon': 121.53600},
    {'name': 'Xinbeitou', 'lat': 25.13170, 'lon': 121.50610},
]

EXPECTED_COLUMNS = [
    'X1 transaction date', 'X2 house age', 'X3 distance to the nearest MRT station',
    'X4 number of convenience stores', 'X5 latitude', 'X6 longitude',
    'epoch_СССР', 'epoch_современные', 'store_category_много', 'store_category_средне'
]

NTD_TO_RUB = 2.8
PING_TO_SQM = 3.3
DEFAULT_AGE = 20
DEFAULT_STORES = 5
DEFAULT_LAT = 25.033
DEFAULT_LON = 121.565
ZOOM_START = 13
MAP_WIDTH = 600
MAP_HEIGHT = 450


def init_log():
    """Создаёт файл лога с заголовками, если он ещё не существует, хранит историю запросов даты, координат, параметры объекта и предсказания."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'address', 'lat', 'lon', 'age', 'distance',
                'stores', 'prediction_ntd', 'prediction_rub', 'nearest_station'
            ])


def save_to_log(address, lat, lon, age, distance, stores, prediction_ntd, prediction_rub, nearest_station):
    """Добавляет запись в CSV-лог с временем, координатами, характеристики объекта, предсказанной ценой в NTD и рублях, ближайшей станцей метро."""
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        address_clean = address.replace(',', ';').replace('\n', ' ')
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            address_clean, lat, lon, age, distance, stores,
            round(prediction_ntd, 2), round(prediction_rub, 2), nearest_station
        ])


@st.cache_resource
def load_model():
    """ Загружает обученную модель и все необходимые объекты из ensemble.pkl с random_forest(модель), scaler_X для масштабирования числовых признаков,
        scaler_y для обратного масштабирования целевой переменной, encoder для кодирования категорий эпохи и магазинов, boxcox_lambda выступает параметром обратного преобразования Бокса — Кокса"""
    ensemble = joblib.load('ensemble.pkl')
    return (ensemble['random_forest'],
            ensemble['scaler_X'],
            ensemble['scaler_y'],
            ensemble['encoder'],
            ensemble['boxcox_lambda'])
def validate_coordinates(lat, lon):
    """Проверяет находятся ли координаты внутри прямоугольника, ограничивающего Тайбэй, возвращает True, если точка внутри, иначе False.
        lat широта точки,а lon долгота"""
    if lat is None or lon is None:
        return False
    return (TAIPEI_BOUNDS['lat_min'] <= lat <= TAIPEI_BOUNDS['lat_max'] and
            TAIPEI_BOUNDS['lon_min'] <= lon <= TAIPEI_BOUNDS['lon_max'])
def haversine(lat1, lon1, lat2, lon2):
    """Вычисляет расстояние между двумя точками на сфере, используется для поиска расстояния до ближайшей станции метро.
        lat1, lon1 координаты широты и долготы объекта недвижимости, lat2, lon2 координаты станции метро"""
    R_Earth = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    R_Earth_metre = R_Earth * c * 1000
    return R_Earth_metre


def get_distance_to_mrt(lat, lon):
    """Определяет ближайшую станцию метро и расстояние до неё, возвращает минимальное расстояние и название станции. lat широта точки, а lon долгота"""
    min_distance = float('inf')
    nearest_station = None
    for station in MRT_STATIONS:
        dist = haversine(lat, lon, station["lat"], station["lon"])
        if dist < min_distance:
            min_distance = dist
            nearest_station = station["name"]
    return min_distance, nearest_station

def inverse_boxcox(y_boxcox, lambda_opt):
    """ Обратное преобразование Бокса — Кокса возвращает исходную цену из преобразованной"""
    if lambda_opt == 0:
        return np.exp(y_boxcox)
    else:
        return (y_boxcox * lambda_opt + 1) ** (1 / lambda_opt)
def get_epoch(year):
    if year < 1991:
        return 'СССР'
    elif year < 2000:
        return '1990е'
    else:
        return 'современные'
def get_store_category(stores):
    if stores <= 2:
        return 'мало'
    elif stores <= 5:
        return 'средне'
    else:
        return 'много'
st.set_page_config(
    page_title="Оценка недвижимости Тайбэй",
    page_icon="favicon.jpg",
    layout="wide"
)
st.title("Предсказание стоимости недвижимости в Тайбэе")
init_log()
if 'map_lat' not in st.session_state:
    st.session_state.map_lat = DEFAULT_LAT
    st.session_state.map_lon = DEFAULT_LON
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Координаты")
    lat = st.number_input("Широта", format="%.5f", value=st.session_state.map_lat, key="lat_input")
    lon = st.number_input("Долгота", format="%.5f", value=st.session_state.map_lon, key="lon_input")
    if st.button("Обновить по координатам"):
        st.session_state.map_lat = lat
        st.session_state.map_lon = lon
        st.rerun()
with col2:
    st.subheader("Выберите точку на карте")
    m = folium.Map(location=[st.session_state.map_lat, st.session_state.map_lon], zoom_start=ZOOM_START)
    folium.Rectangle(
        bounds=[[TAIPEI_BOUNDS['lat_min'], TAIPEI_BOUNDS['lon_min']],
                [TAIPEI_BOUNDS['lat_max'], TAIPEI_BOUNDS['lon_max']]],
        color='red',
        weight=2,
        fill=True,
        fill_opacity=0.1,
        popup='Границы Тайбэя'
    ).add_to(m)
    folium.Marker(
        [st.session_state.map_lat, st.session_state.map_lon],
        popup=f"Точка: {st.session_state.map_lat:.5f}, {st.session_state.map_lon:.5f}",
        icon=folium.Icon(color='green', icon='info-sign'),
        draggable=True
    ).add_to(m)
    map_data = st_folium(m, width=MAP_WIDTH, height=MAP_HEIGHT, key="map")
    if map_data and map_data.get('last_clicked'):
        st.session_state.map_lat = map_data['last_clicked']['lat']
        st.session_state.map_lon = map_data['last_clicked']['lng']
        st.rerun()
    if map_data and map_data.get('last_object_clicked'):
        if map_data['last_object_clicked'].get('lat'):
            st.session_state.map_lat = map_data['last_object_clicked']['lat']
            st.session_state.map_lon = map_data['last_object_clicked']['lng']
            st.rerun()
lat = st.session_state.map_lat
lon = st.session_state.map_lon
st.info(f"Текущая точка: широта {lat:.5f}, долгота {lon:.5f}")
if validate_coordinates(lat, lon):
    distance_to_mrt, nearest_station = get_distance_to_mrt(lat, lon)
    st.success(f"Ближайшая станция метро: {nearest_station} (расстояние {distance_to_mrt:.0f} м)")
else:
    st.error("Координаты за пределами Тайбэя")
    distance_to_mrt = 1000
    nearest_station = "Неизвестно"
st.subheader("Характеристики объекта")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Возраст дома", min_value=0, max_value=100, value=DEFAULT_AGE, step=1, key="age_input")
    stores = st.number_input("Количество магазинов", min_value=0, max_value=30, value=DEFAULT_STORES, step=1,
                             key="stores_input")
if st.button("Рассчитать стоимость", type="primary"):
    best_rf, scaler_X, scaler_y, encoder, boxcox_lambda = load_model()
    construction_year = 2013 - age
    epoch = get_epoch(construction_year)
    store_cat = get_store_category(stores)
    input_data = pd.DataFrame([{
        'X1 transaction date': 2013.0,
        'X2 house age': float(age),
        'X3 distance to the nearest MRT station': float(distance_to_mrt),
        'X4 number of convenience stores': stores,
        'X5 latitude': lat,
        'X6 longitude': lon,
        'epoch': epoch,
        'store_category': store_cat
    }])
    categorical_cols = ['epoch', 'store_category']
    encoded = encoder.transform(input_data[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))
    X = input_data.drop(categorical_cols, axis=1)
    X = pd.concat([X, encoded_df], axis=1)
    for col in EXPECTED_COLUMNS:
        if col not in X.columns:
            X[col] = 0
    X = X[EXPECTED_COLUMNS]
    X_scaled = scaler_X.transform(X)
    prediction_ntd_boxcox = best_rf.predict(X_scaled)[0]
    prediction_ntd = inverse_boxcox(prediction_ntd_boxcox, boxcox_lambda)
    prediction_rub = prediction_ntd / PING_TO_SQM * NTD_TO_RUB
    save_to_log(f"{lat:.5f}, {lon:.5f}", lat, lon, age, distance_to_mrt, stores,prediction_ntd, prediction_rub, nearest_station)
    st.success(f"### {prediction_rub:.2f} тыс. руб/м²")
    st.info(f"Цена: {prediction_ntd:.0f} тыс. NTD/Ping")
with st.expander("Тестирование модели на реальных данных"):
    if st.button("Запустить тест на 5 объектах"):
        try:
            X_test = pd.read_csv('X_test.csv')
            y_test = pd.read_csv('y_test.csv')
            best_rf, scaler_X, scaler_y, encoder, boxcox_lambda = load_model()
            lambda_opt = boxcox_lambda
            y_test_original = inverse_boxcox(y_test.values.flatten(), lambda_opt)
            results = []
            for i in range(min(5, len(X_test))):
                X_sample = X_test.iloc[i:i + 1]
                real_price = y_test_original[i]

                X_scaled = scaler_X.transform(X_sample)
                pred_scaled = best_rf.predict(X_scaled)[0]
                pred_price = inverse_boxcox(pred_scaled, lambda_opt)

                error_percent = abs(real_price - pred_price) / real_price * 100

                results.append({
                    'Объект': i,
                    'Реальная цена': round(real_price, 2),
                    'Предсказанная': round(pred_price, 2),
                    'Ошибка %': round(error_percent, 1)
                })
            st.dataframe(pd.DataFrame(results))
            avg_error = np.mean([r['Ошибка %'] for r in results])
            st.metric("Средняя ошибка", f"{avg_error:.1f}%")
        except FileNotFoundError:
            st.error("Файлы X_test.csv и y_test.csv не найдены")
with st.expander("История запросов"):
    if os.path.exists(LOG_FILE):
        try:
            df_log = pd.read_csv(LOG_FILE)
            st.dataframe(df_log.sort_values('timestamp', ascending=False), use_container_width=True)
        except:
            st.error("Файл логов повреждён")
        if st.button("Очистить историю"):
            os.remove(LOG_FILE)
            init_log()
            st.rerun()
