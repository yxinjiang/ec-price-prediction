# ec-price-prediction

### Background
HDB is interested to monitor price trends for Executive Condominiums (ECs), a type of residential property developed and sold by private developers (i.e. with facilities similar to condominiums) yet subsidised to some degree by the government (first-time buyers are eligible for CPF housing grants, similar to HDB flats, if they buy a new EC during its launch).
HDB is particularly interested to predict the price of new EC flats at two specific points in time:
- 5 years after lease commencement, when an EC reaches its Minimum Occupancy Period (MOP), resulting in a significant number of flats flooding the resale market; and
- 10 years after lease commencement, when an EC becomes privatised and generally indistinguishable from comparable private condominiums.

### Postgress run in docker
1. Create a docker compose file in postgresql-setup folder
2. Start the PostgreSQL container
```bash
docker-compose up -d
docker exec -it postgres-db psql -U myuser -d mydatabase
```

### Data model
Show in 'all diagram.pptx'

### Model building
1. After EDA, I found that the resale EC price is highly correlated to the floor area of the unit, the years after lease commencing, less correlated to the location of the EC, and it is also highly correlated with the time effect.

2. I use Prophet to build several time-series forecasting models based on the years after lease commencing, and the area of the units. The continous value of unit area is transformed into discrete value by using KBinsDiscretizer 


### Model serving

I create a Python API using FastAPI that exposes the ML models as a RESTful service and containerize it using Docker. 
Please find the script in main.py

```bash
python3 -m uvicorn main:app --reload
```
A Dockerfile is created to containerize the app.
```base
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

### Cloud architecture

The docker image will be pushed to AWS ECR and deployed on AWS App Runner or EC2 instance by using github actions ()


### Model monitoring
RMSE and MAE are used to measure the model performance and recorded in csv file saved in reports folder. These metrics are also logged by using Mlflow 

### Automation the processs
- for the feature engineering, since this is a time series regression problem, we can use TSFresh to automate the feature engineering, and apply other ML models like Random Forest, Linear Regression, et. 
- for the model selection, mlflow can be used to visulize the model performance during model training, and log the model, parameters, and other artifacts.
- for the monitoring of model, we can use grafana to monitering the model real-time perforance. 
