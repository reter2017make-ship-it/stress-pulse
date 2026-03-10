# StressPulse: ML Pipeline для предсказания уровня стресса
## 📋 Описание проекта
End-to-end ML pipeline, развернутый в Yandex Cloud, с использованием:
- **Terraform** — инфраструктура как код
- **MLflow** — трекинг экспериментов и регистрация моделей
- **Airflow** — оркестрация пайплайнов
- **FastAPI** — сервинг модели
- **Yandex Cloud** — облачная инфраструктура

# StressPulse: Production ML Pipeline for Stress Prediction

[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.17.2-blue)](https://mlflow.org/)
[![Airflow](https://img.shields.io/badge/Airflow-2.7.1-red)](https://airflow.apache.org/)
[![Terraform](https://img.shields.io/badge/Terraform-1.5-purple)](https://www.terraform.io/)
[![Yandex Cloud](https://img.shields.io/badge/Yandex%20Cloud-live-green)](https://cloud.yandex.com/)

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interface Layer                       │
│  ┌─────────────┐         ┌─────────────┐                       │
│  │ Web Form    │ ──────► │ FastAPI     │                       │
│  │ (HTML/CSS)  │         │ /predict    │                       │
│  └─────────────┘         └─────────────┘                       │
│                                │                                │
└────────────────────────────────│────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Model Serving Layer                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  FastAPI Application                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Load Model  │─►│ Preprocess  │─►│  Predict    │       │  │
│  │  │ from MLflow │  │   Input     │  │  Stress     │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ MLflow API
┌─────────────────────────────────────────────────────────────────┐
│                      MLflow Tracking Layer                       │
│  ┌─────────────┐         ┌─────────────┐                        │
│  │ PostgreSQL  │◄───────►│ MLflow      │                        │
│  │ (metadata)  │         │ Server      │                        │
│  └─────────────┘         └─────────────┘                        │
│                                │                                 │
│                                ▼                                 │
│                        ┌─────────────┐                          │
│                        │ Yandex      │                          │
│                        │ Object      │                          │
│                        │ Storage     │                          │
│                        │ (artifacts) │                          │
│                        └─────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ Airflow triggers training
┌─────────────────────────────────────────────────────────────────┐
│                      Airflow Orchestration                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  DAG: stress_prediction_pipeline (scheduled daily)        │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │ Generate    │─►│ Train       │─►│ Log to      │       │  │
│  │  │ Data        │  │ Models      │  │ MLflow      │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ Terraform provisions
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ MLflow VM   │    │ Airflow VM  │    │ Yandex VPC  │         │
│  │ 158.160.32.249 │  │ 158.160.57.186 │  │ & Security  │         │
│  │ port 5000   │    │ port 8080   │    │ Groups      │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Infrastructure** | Terraform + Yandex Cloud | Create and manage cloud resources |
| **Orchestration** | Apache Airflow | Schedule ML pipelines |
| **Experiment Tracking** | MLflow | Log parameters, metrics, models |
| **Model Registry** | MLflow | Version and promote models |
| **Model Serving** | FastAPI | REST API for predictions |
| **Database** | PostgreSQL | Store MLflow metadata |
| **Storage** | Yandex Object Storage | Store model artifacts |

## 🔄 Data Flow

1. **User** → Web form → FastAPI → Model → Stress score + Recommendations
2. **Airflow** (daily) → Generate data → Train models → Log to MLflow
3. **MLflow** → Store experiments → Update Model Registry
4. **FastAPI** → Load best model → Serve predictions

## 📊 Model Features

| Feature | Range | Description |
|---------|-------|-------------|
| sleep_quality | 1-10 | How well did you sleep? |
| mood | 1-10 | Current mood |
| work_hours | 0-16 | Hours worked today |
| coffee_cups | 0-10 | Coffee consumed |
| deadlines | 0/1 | Have deadlines? |
| exercise_today | 0/1 | Did you exercise? |
| conflicts | 0/1 | Any conflicts today? |
| social_media_hours | 0-8 | Time on social media |

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/reter2017make-ship-it/stress-pulse.git
cd stress-pulse

# 2. Deploy infrastructure
cd terraform
terraform init
terraform apply

# 3. Set up MLflow and Airflow on provisioned VMs
# See instructions in /docs folder
```

## 📈 Results

After running the pipeline, MLflow shows:
- **Random Forest**: MAE ~5.2
- **XGBoost**: MAE ~4.8  
- **Gradient Boosting**: MAE ~5.0

Best model is automatically promoted to Production.





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
