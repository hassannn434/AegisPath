import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import shap

def train_safety_scoring_model():
    # Simulated training dataset representing road segments
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'lighting_density': np.random.uniform(0.1, 1.0, n_samples), # 1 = high light, 0 = dark
        'historical_crime_rate': np.random.uniform(0.0, 5.0, n_samples), # lower is better
        'commercial_activity': np.random.uniform(0.0, 1.0, n_samples), # 1 = active 24/7
        'distance_to_police_station': np.random.uniform(50, 3000, n_samples) # meters
    })
    
    # Target variable: Safety Score (0 to 100)
    # Higher lighting & commercial activity, lower crime & distance increase safety score
    data['safety_score'] = (
        (data['lighting_density'] * 40) +
        (data['commercial_activity'] * 30) -
        (data['historical_crime_rate'] * 5) -
        (data['distance_to_police_station'] / 100) + 30
    )
    data['safety_score'] = data['safety_score'].clip(0, 100)
    
    X = data[['lighting_density', 'historical_crime_rate', 'commercial_activity', 'distance_to_police_station']]
    y = data['safety_score']
    
    # Train Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    print("Machine Learning Safety Model Trained Successfully!")
    return model, X

if __name__ == "__main__":
    model, X_train = train_safety_scoring_model()
    
    # Generate SHAP explanations for explainable AI metrics
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train.iloc[:5])
    print("SHAP explainability pipeline initialized for road segment risk evaluation.")