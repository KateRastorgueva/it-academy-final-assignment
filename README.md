# it-academy-final-assignment
# Оценка стоимости недвижимости

## О проекте
Модель машинного обучения для предсказания стоимости единицы площади недвижимости в Тайбэе (Тайвань) по 6 характеристикам: возраст дома, расстояние до метро, количество магазинов в пешей доступности, широта, долгота, дата сделки.

**Датасет:** UCI Real Estate Valuation (414 записей, 2012-2013 гг.)
## Источники
- **Датасет:** [UCI Real Estate Valuation](https://archive.ics.uci.edu/dataset/477/real+estate+valuation+data+set)
- **Colab:** [Google Colab](https://colab.research.google.com/drive/1KYkxQccefZv1SSsVsw8jMWxVn7e6nprg)
## Результаты
Лучшая модель: **RandomForest**
- RMSE: 1.25 тыс. NTD/Ping
- MAE: 0.88 тыс. NTD/Ping  
- R²: 0.833

## Использованные модели
| Модель | R² |
|--------|-----|
| LinearRegression (baseline) | 0.672 |
| **RandomForest** | **0.833** |
| CatBoost | 0.82 |
| Нейросеть | 0.75 |

## Ключевые выводы
Самое сильное влияние на цену оказывает расстояние до метро (корреляция -0.714). Обнаружена нелинейная зависимость для возраста дома (разница Пирсон/Phi-k = 0.27). Дома 1990-х годов стоят дешевле из-за экономического кризиса

## Технологии
Python, pandas, numpy, scikit-learn, catboost, PyTorch, SHAP, MLflow, seaborn, matplotlib, phik, Streamlit

## Установка и запуск

1. Клонировать репозиторий
```bash
git clone https://github.com/KateRastorgueva/real-estate-valuation.git
cd real-estate-valuation
Установить зависимости

```bash
pip install -r requirements.txt
Запустить Streamlit-приложение

```bash
streamlit run app.py
real-estate-valuation/
├── итоговое задание.ipynb (Colab)
├── app.py
├── ensemble.pkl 
├── requirements.txt
└── README.md
