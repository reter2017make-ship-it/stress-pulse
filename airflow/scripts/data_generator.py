import numpy as np
import pandas as pd
import random

def generate_stress_data(n_samples=10000):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for i in range(n_samples):
        sleep_quality = np.random.randint(1, 11)
        mood = np.random.randint(1, 11)
        work_hours = np.random.randint(0, 17)
        coffee_cups = np.random.randint(0, 11)
        social_media_hours = round(np.random.uniform(0, 8), 1)
        hours_since_last_meal = round(np.random.uniform(0, 8), 1)
        deadlines = random.choice([0, 1])
        exercise_today = random.choice([0, 1])
        conflicts = random.choice([0, 1])
        enough_water = random.choice([0, 1])
        fresh_air = random.choice([0, 1])
        smoking = random.choice([0, 1])
        
        stress_score = 100
        stress_score -= sleep_quality * 2
        stress_score -= mood * 2
        stress_score -= exercise_today * 8
        stress_score -= enough_water * 5
        stress_score -= fresh_air * 5
        stress_score += work_hours * 3
        stress_score += coffee_cups * 2
        stress_score += social_media_hours * 2
        stress_score += deadlines * 15
        stress_score += conflicts * 20
        stress_score += smoking * 10
        
        if hours_since_last_meal > 4:
            stress_score += (hours_since_last_meal - 4) * 3
        
        stress_score = max(0, min(100, stress_score))
        
        if stress_score < 30:
            stress_category = "Низкий"
        elif stress_score < 60:
            stress_category = "Средний"
        else:
            stress_category = "Высокий"
        
        record = {
            'sleep_quality': sleep_quality,
            'mood': mood,
            'work_hours': work_hours,
            'coffee_cups': coffee_cups,
            'social_media_hours': social_media_hours,
            'hours_since_last_meal': hours_since_last_meal,
            'deadlines': deadlines,
            'exercise_today': exercise_today,
            'conflicts': conflicts,
            'enough_water': enough_water,
            'fresh_air': fresh_air,
            'smoking': smoking,
            'stress_score': stress_score,
            'stress_category': stress_category
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_stress_data(10000)
    df.to_csv('/opt/airflow/data/stress_data.csv', index=False)
    print(f"Сгенерировано {len(df)} записей")
    print(df['stress_category'].value_counts())
