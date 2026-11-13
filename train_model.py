import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save():
    print("Loading dataset...")
    df = pd.read_csv('placement_data.csv')
    
    # Preprocessing
    # Map Yes/No to 1/0
    df['Extracurricular_Activities'] = df['Extracurricular_Activities'].map({'Yes': 1, 'No': 0})
    df['Placement_Training'] = df['Placement_Training'].map({'Yes': 1, 'No': 0})
    
    # Map target variable Placed/Not Placed to 1/0
    df['Placement_Status'] = df['Placement_Status'].map({'Placed': 1, 'Not Placed': 0})
    
    # Split features and target
    X = df.drop('Placement_Status', axis=1)
    y = df['Placement_Status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    train_acc = model.score(X_train_scaled, y_train)
    test_acc = model.score(X_test_scaled, y_test)
    print(f"Model trained successfully!")
    print(f"Training Accuracy: {train_acc:.4f}")
    print(f"Testing Accuracy: {test_acc:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("Saved model.pkl and scaler.pkl")

if __name__ == "__main__":
    train_and_save()
