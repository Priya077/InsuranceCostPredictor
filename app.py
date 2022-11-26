from flask import Flask, request, url_for, redirect, render_template
import pickle

import numpy as np
import csv


app = Flask(__name__, template_folder='./templates', static_folder='./static')

Pkl_Filename = "rf_tuned.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    model = pickle.load(file)
@app.route('/')

def hello_world():
    return render_template('home.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    temp = tuple()
    for x in request.form.values():
        temp += (x,)
    features = []
    for x in range(1, len(temp)):
        features.append(int(temp[x]))
    print(features)
    print(temp)
    
    
    final = np.array(features).reshape((1,6))
    print(final)
    pred = model.predict(final)[0]
    print(pred)
    features += ('{0:.3f}'.format(pred), )
    temp += ('{0:.3f}'.format(pred), )
    with open('Patient.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(temp)
    with open('insurance.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(features)

    if pred < 0:
        return render_template('op.html', pred='Error calculating Amount!')
    else:
        return render_template('op.html', pred='Expected amount is {0:.3f}'.format(pred))
    
    

    

if __name__ == '__main__':
    app.run(debug=True)