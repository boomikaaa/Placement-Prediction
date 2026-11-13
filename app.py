from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load model and scaler
model_path = 'model.pkl'
scaler_path = 'scaler.pkl'

model = None
scaler = None

if os.path.exists(model_path) and os.path.exists(scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
else:
    print("Warning: Model or Scaler file not found. Please run train_model.py first.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model, scaler
    if model is None or scaler is None:
        # Try loading again just in case they were generated after server start
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
        else:
            return jsonify({'error': 'Model not trained yet. Please train the model first.'}), 500
            
    try:
        data = request.json
        
        # Extract features in the correct order
        # SSC_Marks, HSC_Marks, CGPA, Internships, Projects, Certifications, Aptitude_Score, Soft_Skills_Rating, Extracurricular_Activities, Placement_Training
        ssc_marks = float(data.get('ssc_marks', 0))
        hsc_marks = float(data.get('hsc_marks', 0))
        cgpa = float(data.get('cgpa', 0))
        internships = int(data.get('internships', 0))
        projects = int(data.get('projects', 0))
        certifications = int(data.get('certifications', 0))
        aptitude_score = float(data.get('aptitude_score', 0))
        soft_skills = int(data.get('soft_skills', 1))
        
        # Map Yes/No to 1/0
        extracurricular = 1 if data.get('extracurricular', 'No') == 'Yes' else 0
        placement_training = 1 if data.get('placement_training', 'No') == 'Yes' else 0
        
        # Prepare input array
        features = np.array([[
            ssc_marks,
            hsc_marks,
            cgpa,
            internships,
            projects,
            certifications,
            aptitude_score,
            soft_skills,
            extracurricular,
            placement_training
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        placement_status = "Placed" if prediction == 1 else "Not Placed"
        probability = probabilities[prediction] * 100
        
        return jsonify({
            'status': 'success',
            'prediction': placement_status,
            'probability': round(probability, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
