from mlflow.client import MlflowClient
import mlflow
from mlflow.pyfunc import PyFuncModel
from pprint import pprint
import os 
from dotenv import load_dotenv


load_dotenv()
MLFLOW_TRACKING_URI=os.getenv('MLFLOW_TRACKING_URI')
MLFLOW_TRACKING_USERNAME=os.getenv('MLFLOW_TRACKING_USERNAME')
MLFLOW_TRACKING_PASSWORD=os.getenv('MLFLOW_TRACKING_PASSWORD')

class MLFlowHandler:
    def __init__(self) -> None:
        self.client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    def check_mlflow_health(self) -> None:
        try:
            experiments = self.client.search_experiments()   
            for rm in experiments:
                pprint(dict(rm), indent=4)
                return 'Service returning experiments'
        except:
            return 'Error calling MLFlow'
        
    def get_production_model(self, store_id: str) -> PyFuncModel:
        model_name = f"prophet-retail-forecaster-store-{store_id}"
        model = mlflow.pyfunc.\
            load_model(model_uri=f"models:/{model_name}/production")
        return model
            
'''
# Handle this properly later ...
def check_mlflow_health():
    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI) 
    try:
        experiments = client.search_experiments()   
        for rm in experiments:
            pprint(dict(rm), indent=4)
        return 'Service returning experiments'
    except:
        return 'Error calling MLFlow'

'''    
    
    