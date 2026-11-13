import pandas as pd
import numpy as np

def generate_placement_data(num_samples=1000):
    np.random.seed(42)
    
    # 1. SSC Marks (Percentage: 50 to 100)
    ssc_marks = np.random.uniform(50, 100, num_samples)
    
    # 2. HSC Marks (Percentage: 50 to 100)
    hsc_marks = np.random.uniform(50, 100, num_samples)
    
    # 3. CGPA (Scale 5.0 to 10.0)
    # CGPA usually has some correlation with SSC/HSC, adding a slight correlation
    base_cgpa = (ssc_marks + hsc_marks) / 20.0 
    cgpa = np.clip(base_cgpa + np.random.normal(0, 0.8, num_samples), 5.0, 10.0)
    
    # 4. Internships (0 to 3)
    internships = np.random.choice([0, 1, 2, 3], num_samples, p=[0.4, 0.4, 0.15, 0.05])
    
    # 5. Projects (1 to 5)
    projects = np.random.choice([1, 2, 3, 4, 5], num_samples, p=[0.1, 0.3, 0.4, 0.15, 0.05])
    
    # 6. Workshops/Certifications (0 to 5)
    certifications = np.random.choice([0, 1, 2, 3, 4, 5], num_samples, p=[0.2, 0.3, 0.25, 0.15, 0.08, 0.02])
    
    # 7. Aptitude Test Score (Percentage: 40 to 100)
    aptitude_score = np.random.uniform(40, 100, num_samples)
    
    # 8. Soft Skill Rating (Scale 1 to 5)
    soft_skills = np.random.choice([1, 2, 3, 4, 5], num_samples, p=[0.05, 0.15, 0.4, 0.3, 0.1])
    
    # 9. Extracurricular Activities (Yes/No)
    extracurricular = np.random.choice(['Yes', 'No'], num_samples, p=[0.6, 0.4])
    
    # 10. Placement Training (Yes/No)
    placement_training = np.random.choice(['Yes', 'No'], num_samples, p=[0.7, 0.3])
    
    # Create a DataFrame
    df = pd.DataFrame({
        'SSC_Marks': np.round(ssc_marks, 2),
        'HSC_Marks': np.round(hsc_marks, 2),
        'CGPA': np.round(cgpa, 2),
        'Internships': internships,
        'Projects': projects,
        'Certifications': certifications,
        'Aptitude_Score': np.round(aptitude_score, 2),
        'Soft_Skills_Rating': soft_skills,
        'Extracurricular_Activities': extracurricular,
        'Placement_Training': placement_training
    })
    
    # 11. Placement Status (Target Variable)
    # Calculate a custom 'employability score' to determine placement
    employability_score = (
        (df['CGPA'] * 10 * 0.3) + 
        (df['Aptitude_Score'] * 0.25) + 
        (df['Soft_Skills_Rating'] * 20 * 0.15) + 
        (df['Internships'] * 10) + 
        (df['Projects'] * 5) + 
        (df['Certifications'] * 2)
    )
    
    # Boost score slightly if they have training or extracurriculars
    training_bonus = (df['Placement_Training'] == 'Yes') * 5
    extra_bonus = (df['Extracurricular_Activities'] == 'Yes') * 3
    employability_score += training_bonus + extra_bonus
    
    # Determine Placement based on threshold and some randomness
    threshold = np.percentile(employability_score, 40) # Assume top 60% get placed roughly
    df['Placement_Status'] = np.where(employability_score > threshold + np.random.normal(0, 5, num_samples), 'Placed', 'Not Placed')
    
    return df

if __name__ == "__main__":
    print("Generating synthetic placement dataset...")
    df = generate_placement_data(2000) # Generate 2000 records
    df.to_csv("placement_data.csv", index=False)
    print(f"Dataset generated successfully with {len(df)} records!")
    print(df.head())
    print(f"\nPlacement Status Distribution:\n{df['Placement_Status'].value_counts(normalize=True)*100}")
