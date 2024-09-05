from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
import joblib
from prophet.serialize import model_to_json, model_from_json

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            area =int(request.form['area'])
            year_after_lease_com =int(request.form['year_after_lease_com'])
            start_date =str(request.form['start_date'])
            end_date =str(request.form['end_date'])
            scaler = joblib.load('./models/KBinsDiscretizer.save') 
            area_bin = scaler.transform([[area]])[0][0]
            with open(f'./models/model_area{area}_year{year_after_lease_com}', 'r') as fin:
                model = model_from_json(fin.read())  # Load model
            ds = pd.date_range(start=start_date,end=end_date,freq='MS')
            df_test = pd.DataFrame(ds,columns=['ds'])
            predict = model.predict(df_test).loc[:, 'yhat']

            return render_template('results.html', prediction = str(predict))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)