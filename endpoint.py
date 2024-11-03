import requests
import json

# URL for the web service, should be similar to:
# 'http://8530a665-66f3-49c8-a953-b82a2d312917.eastus.azurecontainer.io/score'
scoring_uri = 'http://1e3f4d52-ca2b-4d46-9186-6e68fc4868d4.southcentralus.azurecontainer.io/score'
# If the service is authenticated, set the key or token
key = 'HSUOKsrTzmgsLaONaKJPlJo2rQswEVYe'

# Two sets of data to score, so we get two results back
data = {"data":
        [
            {
                "person_age": 22.0,
                "person_gender": "female",
                "person_education": "Master",
                "person_income": 71948.0,
                "person_emp_exp": 0,
                "person_home_ownership": "RENT",
                "loan_amnt": 35000.0,
                "loan_intent": "PERSONAL",
                "loan_int_rate": 16.02,
                "loan_percent_income": 0.49,
                "cb_person_cred_hist_length": 3.0,
                "credit_score": 561,
                "previous_loan_defaults_on_file": "No"
            },
            {
                "person_age": 21.0,
                "person_gender": "female",
                "person_education": "High School",
                "person_income": 12282.0,
                "person_emp_exp": 0,
                "person_home_ownership": "OWN",
                "loan_amnt": 1000.0,
                "loan_intent": "EDUCATION",
                "loan_int_rate": 11.14,
                "loan_percent_income": 0.08,
                "cb_person_cred_hist_length": 2.0,
                "credit_score": 504,
                "previous_loan_defaults_on_file": "Yes"
            }]
        }
header_data = {
    "Inputs": data,
    "GlobalParameters": {
        "method": "predict"
    }
}
# Convert to JSON string
input_data = json.dumps(header_data)
with open("data.json", "w") as _f:
    _f.write(input_data)

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {key}'

# Make the request and display the response
resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.json())
