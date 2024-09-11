from fastapi import FastAPI,UploadFile
import joblib
import pandas as pd 

app = FastAPI()

@app.post('/predict_price')
async def predict_price(area:float,floor_range:str,district:str,market_segment:str,year:int,month:int,year_after_lease_com:int):
    area =float(area)
    floor_range = str(floor_range)
    district = str(district)
    market_segment = str(market_segment)
    year = int(year)
    month = int(month)
    year_after_lease_com =int(year_after_lease_com)

    model = joblib.load('./models/model.pkl')  # Load model
    data = pd.DataFrame([{'area': area,
                        'floor_range': floor_range,
                        'district': district,
                        'market_segment': market_segment,
                        'year': year,
                        'month': month,
                        'year_after_lease_com': year_after_lease_com}
                        ])
                        
    predict = model.predict(data).loc[:, 'yhat'].to_frame().to_json()
    response = {
        'Prediction':predict,
                }
    return response


