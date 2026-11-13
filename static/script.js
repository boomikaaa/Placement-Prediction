document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultCard = document.getElementById('result-card');
    const resultPlaceholder = resultCard.querySelector('.result-placeholder');
    const resultContent = document.getElementById('result-content');
    
    const outcomeBadge = document.getElementById('prediction-outcome');
    const probFill = document.getElementById('prob-fill');
    const probPercent = document.getElementById('prob-percent');
    const analysisSummary = document.getElementById('analysis-summary');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading spinner
        const spinnerOverlay = document.createElement('div');
        spinnerOverlay.className = 'loading-overlay';
        spinnerOverlay.innerHTML = `
            <div class="spinner"></div>
            <p>Analyzing profile with ML model...</p>
        `;
        resultCard.appendChild(spinnerOverlay);

        // Fetch inputs
        const ssc_marks = parseFloat(document.getElementById('ssc_marks').value);
        const hsc_marks = parseFloat(document.getElementById('hsc_marks').value);
        const cgpa = parseFloat(document.getElementById('cgpa').value);
        const aptitude_score = parseFloat(document.getElementById('aptitude_score').value);
        const soft_skills = parseInt(document.getElementById('soft_skills').value);
        const internships = parseInt(document.getElementById('internships').value);
        const projects = parseInt(document.getElementById('projects').value);
        const certifications = parseInt(document.getElementById('certifications').value);
        const placement_training = document.getElementById('placement_training').value;
        const extracurricular = document.getElementById('extracurricular').value;

        const payload = {
            ssc_marks,
            hsc_marks,
            cgpa,
            aptitude_score,
            soft_skills,
            internships,
            projects,
            certifications,
            placement_training,
            extracurricular
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            // Remove spinner
            spinnerOverlay.remove();

            if (data.status === 'success') {
                // Show content, hide placeholder
                resultPlaceholder.classList.add('hidden');
                resultContent.classList.remove('hidden');

                // Update UI based on prediction
                const isPlaced = data.prediction === 'Placed';
                
                outcomeBadge.innerHTML = `<span class="outcome-badge ${isPlaced ? 'placed' : 'not-placed'}">${data.prediction}</span>`;
                
                // Animate progress bar
                probFill.style.width = '0%';
                setTimeout(() => {
                    probFill.style.width = `${data.probability}%`;
                    if (!isPlaced) {
                        // Change color to danger for low chance
                        probFill.style.background = 'linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%)';
                    } else {
                        // Reset to primary/success theme
                        probFill.style.background = 'linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-blue) 100%)';
                    }
                }, 100);
                
                probPercent.innerText = `${data.probability}%`;

                // Generate customized dynamic summary report
                let feedbackText = '';
                if (isPlaced) {
                    feedbackText = `Outstanding! The student shows a strong profile. With a CGPA of ${cgpa.toFixed(2)}, ${internships} internship(s), and ${projects} project(s), the model predicts a high likelihood of placement (${data.probability}% confidence). `;
                    if (placement_training === 'Yes') {
                        feedbackText += "Having completed the placement training program significantly bolstered their readiness.";
                    } else {
                        feedbackText += "Consider taking a mock interview/placement training program to polish skills even further.";
                    }
                } else {
                    feedbackText = `The student has a lower probability of placement (${(100 - data.probability).toFixed(2)}% chance of not being placed) based on historical student records. `;
                    
                    // Identify weak areas
                    const recommendations = [];
                    if (cgpa < 7.5) {
                        recommendations.push("aim to improve their CGPA above 7.5");
                    }
                    if (internships === 0) {
                        recommendations.push("secure at least one industry internship");
                    }
                    if (projects < 2) {
                        recommendations.push("build 1-2 more hands-on practical projects");
                    }
                    if (placement_training === 'No') {
                        recommendations.push("enroll in the placement training program");
                    }
                    if (aptitude_score < 70) {
                        recommendations.push("practice aptitude tests to improve quantitative and logical skills");
                    }

                    if (recommendations.length > 0) {
                        feedbackText += "To improve their placement prospects, they should: " + recommendations.slice(0, -1).join(", ") + ", and " + recommendations.slice(-1) + ".";
                    } else {
                        feedbackText += "Although key indicators are good, general readiness can be improved with industry certifications or specialized skill bootcamps.";
                    }
                }

                analysisSummary.innerText = feedbackText;
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            spinnerOverlay.remove();
            alert('An error occurred while connecting to the server.');
        }
    });
});
