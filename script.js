document.addEventListener('DOMContentLoaded', function () {
    function predictSurvival() {
        // Get user input
        const salary = document.getElementById("salary").value;
        const sex = document.querySelector('input[name="sex"]:checked').value;
        const age = document.getElementById("age").value;

        console.log(`Salary: ${salary}, Sex: ${sex}, Age: ${age}`);

        // Send a POST request to backend
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                salary: salary,
                sex: sex,
                age: age
            })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerHTML = `Survival Probability: ${data.survival_probability}%`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("result").innerHTML = "Error: Unable to fetch data.";
        });
    }

    // Attach the predictSurvival function to the button click event
    document.querySelector('button').onclick = predictSurvival;
});
