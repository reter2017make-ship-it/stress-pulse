# StressPulse: ML Pipeline для предсказания уровня стресса
## 📋 Описание проекта
End-to-end ML pipeline, развернутый в Yandex Cloud, с использованием:
- **Terraform** — инфраструктура как код
- **MLflow** — трекинг экспериментов и регистрация моделей
- **Airflow** — оркестрация пайплайнов
- **FastAPI** — сервинг модели
- **Yandex Cloud** — облачная инфраструктура

## 🏗️ Архитектура
(добавь схему позже)

## 🚀 Быстрый старт
1. Настройка инфраструктуры:
```bash
cd terraform
terraform init
terraform apply
```

2. Запуск MLflow и Airflow на серверах
3. Запуск DAG в Airflow

## 📊 Фичи модели
- Качество сна (1-10)
- Настроение (1-10)
- Рабочие часы
- Чашки кофе
- Дедлайны (да/нет)
- Спорт (да/нет)
- И другие...

## 🛠️ Технологии
- Python, scikit-learn, XGBoost
- MLflow, Airflow
- Terraform, Docker
- Yandex Cloud
