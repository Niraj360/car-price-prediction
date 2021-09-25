#Importing the libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

#Initialising the application
app = Flask(__name__)

#Loading the model
loadedModel=pickle.load(open('car_price.pkl','rb'))

#Rendering the template
@app.route("/")
def Home():
    return render_template('car_price.html')
    
#Getting the prediction and returning it to the template
@app.route("/predict" ,methods=['POST'])
def predict():
    year = request.form['Year']
    present_price = request.form['Present_Price']
    Kms_driven = request.form['Kms_driven']
    Transmission= request.form['Transmission']
    Fuel_Type= request.form['Fuel_Type']

    if Transmission=="Manual":
        Transmission=1
    else:
        Transmission=0


    if Fuel_Type=="CNG":
        Petrol=0
        Diesel=0
    elif Fuel_Type=="Petrol":
        Petrol=1
        Diesel=0
    elif Fuel_Type=="Diesel":
        Petrol=0
        Diesel=1

    prediction=loadedModel.predict([[ year,  present_price, Kms_driven,Transmission,Diesel,Petrol]])[0]

    if prediction < 0:
        prediction = "less than 1"
    else:
        prediction = round(prediction, 2)
    
    with open('history.csv','a') as file:
        file.write("\n" + str(year) + "," + str(present_price) + "," + str(Kms_driven) + "," + str(Transmission) + "," + Fuel_Type + "," + str(prediction))
    
    
    return render_template('car_price.html', selling_price=str(prediction) + " lakhs") 

#Starting the application
if __name__=='__main__':
    app.run(debug=True)
    
