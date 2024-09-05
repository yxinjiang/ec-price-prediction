from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import pandas as pd
import pprint

if __name__ == '__main__':
    from helpers.request import ForecastRequest, create_forecast_index
    from registry.mlflow.handler import MLFlowHandler

else:
    from .helpers.request import ForecastRequest, create_forecast_index
    from .registry.mlflow.handler import MLFlowHandler

from typing import List

# Caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache




# Logging
import logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
logging.basicConfig(format = log_format, level = logging.INFO)

models = {}

app = FastAPI()

    
@app.get("/health/", status_code=200)
async def healthcheck():
    global handlers
    logging.info("Got handlers in healthcheck.")
    return {
        "serviceStatus": "OK",
        "modelTrackingHealth": handlers['mlflow'].check_mlflow_health()
        }

@cache(expire=30)
async def get_models(store_ids: list):
    global handlers
    global models
    models = []
    for store_id in store_ids:
        model = handlers['mlflow'].get_production_model(store_id=store_id)
        models.append(model)
    return models

async def get_model(area: str,year_after_lease_com:str):
    global handlers
    global models
    model_name = f'model_area{area}_year{year_after_lease_com}'
    if model_name not in models:
        models[model_name] = handlers['mlflow'].get_production_model(store_id=store_id)
    return models[model_name]

@app.get("/testcache", status_code=200)
async def test_cache():
    global handlers
    logging.info(pprint.pprint(str(handlers['mlflow'])))
    return {'type': str(handlers['mlflow'].get_production_model(store_id='4'))}
    

@app.post("/forecast/", status_code=200)
async def return_forecast(forecast_request: List[ForecastRequest]):
    '''
    Main route in the app for returning the forecast, steps are:
    
    1. iterate over forecast elements
    2. get model for each store, forecast request
    3. prepare forecast input time index
    4. perform forecast
    5. append to return object
    6. return
    '''
    forecasts = []
    for item in forecast_request:
        model = await get_model(item.store_id)
        forecast_input = create_forecast_index(
            begin_date=item.begin_date, 
            end_date=item.end_date
            )
        forecast_result = {}
        forecast_result['request'] = item.dict()
        model_prediction = model.predict(forecast_input)[['ds', 'yhat']]\
            .rename(columns={'ds': 'timestamp', 'yhat': 'value'})
        model_prediction['value'] = model_prediction['value'].astype(int)
        forecast_result['forecast'] = model_prediction.to_dict('records')
        forecasts.append(forecast_result)
    return forecasts    