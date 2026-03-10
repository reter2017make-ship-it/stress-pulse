import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, 
GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, 
r2_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import mlflow
import mlflow.sklearn
import joblib
import os
from datetime import datetime

os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://storage.yandexcloud.net'

mlflow.set_tracking_uri("http://158.160.32.249:5000")

def prepare_features(df):
    feature_columns = [
        'sleep_quality', 'mood', 'work_hours', 'coffee_cups',
        'social_media_hours', 'hours_since_last_meal', 'deadlines',
        'exercise_today', 'conflicts', 'enough_water', 'fresh_air', 
'smoking'
    ]
    X = df[feature_columns].copy()
    y = df['stress_score']
    X = X.fillna(X.mean())
    return X, y

def train_and_log_model(model, model_name, X_train, X_test, y_train, 
y_test, params):
    with 
mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
        mlflow.log_params(params)
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        
        mlflow.log_metrics({
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_r2': train_r2,
            'test_r2': test_r2
        })
        
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(X_train.columns, 
model.feature_importances_))
            mlflow.log_dict(feature_importance, 'feature_importance.json')
        
        mlflow.sklearn.log_model(model, model_name)
        
        return {
            'test_mae': test_mae,
            'test_r2': test_r2,
            'run_id': mlflow.active_run().info.run_id
        }

def main():
    print("Начинаем обучение моделей...")
    df = pd.read_csv('/opt/airflow/data/stress_data.csv')
    print(f"Загружено {len(df)} записей")
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
test_size=0.2, random_state=42)
    
    rf_params = {'n_estimators': 100, 'max_depth': 10, 'random_state': 42}
    rf_model = RandomForestRegressor(**rf_params)
    rf_results = train_and_log_model(rf_model, 'random_forest', X_train, 
X_test, y_train, y_test, rf_params)
    print(f"Random Forest: MAE={rf_results['test_mae']:.2f}")
    
    xgb_params = {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 
0.1, 'random_state': 42}
    xgb_model = xgb.XGBRegressor(**xgb_params)
    xgb_results = train_and_log_model(xgb_model, 'xgboost', X_train, 
X_test, y_train, y_test, xgb_params)
    print(f"XGBoost: MAE={xgb_results['test_mae']:.2f}")
    
    gb_params = {'n_estimators': 100, 'max_depth': 5, 'learning_rate': 
0.1, 'random_state': 42}
    gb_model = GradientBoostingRegressor(**gb_params)
    gb_results = train_and_log_model(gb_model, 'gradient_boosting', 
X_train, X_test, y_train, y_test, gb_params)
    print(f"Gradient Boosting: MAE={gb_results['test_mae']:.2f}")
    
    results = [rf_results, xgb_results, gb_results]
    best_model = min(results, key=lambda x: x['test_mae'])
    print(f"\nЛучшая модель: {best_model['run_id']} 
MAE={best_model['test_mae']:.2f}")

if __name__ == "__main__":
    main()
