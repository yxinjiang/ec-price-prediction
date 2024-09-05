from fastapi import FastAPI,UploadFile
from prophet.serialize import model_from_json
import joblib
import pandas as pd 


app = FastAPI()

@app.post('/get_predictions')
async def get_predictions(area:int,year_after_lease_com:int,date_start:str,date_end:str):
    area =int(area)
    year_after_lease_com =int(year_after_lease_com)
    start_date =str(date_start)
    end_date =str(date_end)
    scaler = joblib.load('./models/KBinsDiscretizer.save') 
    area_bin = int(scaler.transform([[area]])[0][0])
    with open(f'./models/model_area{area_bin}_year{year_after_lease_com}.json', 'r') as fin:
        model = model_from_json(fin.read())  # Load model
    ds = pd.date_range(start=start_date,end=end_date,freq='MS')
    df_test = pd.DataFrame(ds,columns=['ds'])
    predict = model.predict(df_test).loc[:, 'yhat'].to_frame().to_json()
    response = {
        'Prediction':predict,
                }
    return response


