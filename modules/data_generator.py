import pandas as pd
import numpy as np
import random

def generate_athlete_data(num_athletes=50):
    np.random.seed(42)
    random.seed(42)
    
    first_names = ["James", "Michael", "Robert", "John", "David", "William", "Richard", "Joseph", "Thomas", "Charles"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    teams = ["Red Hawks", "Blue Titans", "Iron Wolves", "Silver Eagles"]
    
    data = []
    for i in range(num_athletes):
        # Base features
        training_hours = round(np.random.normal(15, 4), 1)
        exertion = random.randint(1, 10)
        sleep = round(np.random.normal(7, 1.5), 1)
        injuries = random.randint(0, 3)
        jump_load = random.randint(50, 300)
        
        # Risk logic: High training, high exertion, low sleep, high jump load increases risk
        risk_score_continuous = (
            (training_hours * 0.3) + 
            (exertion * 2.0) + 
            ((10 - sleep) * 2.5) + 
            (injuries * 5.0) + 
            (jump_load * 0.05)
        )
        
        # Binary target for ML model (top 25% are high risk)
        is_high_risk = 1 if risk_score_continuous > 35 else 0
        
        # Performance Score for leaderboard (higher is better)
        performance_score = round(
            (training_hours * 5) - (exertion * 2) + (sleep * 8) - (injuries * 10) + (jump_load * 0.1) + random.uniform(0, 15), 
            1
        )
        
        data.append({
            "athlete_id": f"ATH-{1000 + i}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "team": random.choice(teams),
            "training_hours_weekly": max(2.0, training_hours),
            "perceived_exertion_1to10": exertion,
            "sleep_hours": max(3.0, sleep),
            "past_injuries": injuries,
            "jump_load_count": jump_load,
            "performance_score": max(10.0, performance_score),
            "is_high_risk": is_high_risk
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_athlete_data()
    print(f"Generated {len(df)} athletes.")
