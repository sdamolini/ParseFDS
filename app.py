import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# create flask app
app = Flask(__name__)

# load model
model = pickle.load(open('model.pkl', 'rb'))

# home page
@app.route('/')
def home():
    return render_template('index.html')

# post page
@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    # extract fields features
    int_features = [int(x) for x in request.form.values()]
    # store features for predictions
    final_features = [np.array(int_features)]
    # make predictions
    prediction = model.predict(final_features)
    # format output
    output = round(prediction[0], 2)

    # render index with adder inputs
    output = "Employee Salary should be $ {0}\n\nExperience={1}\nTest Score={2}\nInterview Score={3}".format(output,*int_features).split('\n')
    return render_template('index.html', prediction_text=output)

if __name__ == "__main__":
    app.run(debug=True)