from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Load the trained model (replace this with your actual model loading code)
model = joblib.load('titanic_model.pkl')

def salary_pclass(salary):
    if salary >= 100000:
        return 1
    elif 99999 <= salary <= 50000:
        return 2
    elif salary < 50000:
        return 3
    else:
        return "Incorrect"

@app.route('/predict', methods=['POST'])
def predict_survival():
    try: 
        data = request.get_json()  # Get data from the request
        print(f"Received data: {data}")  # Log the received data

        salary = float(data['salary'])  # Convert salary to float
        sex = data['sex']
        age = data['age']

        if salary is None or sex is None or age is None:
            return jsonify({'error': 'Missing input data'}), 400

        # Ensure salary is a valid number
        try:
            salary = float(salary)
        except ValueError:
            return jsonify({'error': 'Invalid salary input'}), 400
        # Map sex to numerical values (0 for male, 1 for female)
        sex = 0 if sex == 'male' else 1
        print(f"Received data - Salary: {salary}, Sex: {sex}, Age: {age}")

        pclass = salary_pclass(salary)

        # Create a DataFrame with user input
        user_data = pd.DataFrame({
            'Pclass': [pclass],
            'Sex': [sex],
            'Age': [age],
            'SibSp': [0],  # Default value
            'Parch': [0],  # Default value
            'Fare': [50],  # Default value
            'Embarked': [0]  # Default value (S)
        })

        # Predict survival probability
        survival_prob = model.predict_proba(user_data)[0][1]
        return jsonify({'survival_probability': survival_prob * 100})  # Return the prediction as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors and return a message

if __name__ == '__main__':
    app.run(debug=True)
