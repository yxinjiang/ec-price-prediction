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

2. The dataset is splitted in to train (2019 to 2023 ) and test (2024) set

3. I build a regression model using xgboost, the input features are: area', 'floor_range', 'price', 'district', 'market_segment', 'year','month', 'year_after_lease_com'. RMSE, MAPE, and MAE are used as performance metrics. Mlflow is used to track the experiments and log the results.


### Model serving

I create a Python API using FastAPI that exposes the ML models as a RESTful service and containerize it using Docker, and deploy in aws ec2 using github CI/CD.

Here is the link to the app: http://54.255.65.238:8000/predict_price
```bash
python3 -m uvicorn main:app --reload
```
A Dockerfile is created to containerize the app.
```base
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```

### Cloud architecture

The docker image will be pushed to AWS ECR and deployed on AWS App Runner or EC2 instance by using github actions

#### Simple description of the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

##### Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess

#### ECR URI

URI: {YOUR-ECR_URI}.dkr.ecr.ap-southeast-1.amazonaws.com
repo name: ec-price


### Model monitoring
RMSE and MAE are used to measure the model performance and recorded in csv file saved in reports folder. These metrics are also logged by using Mlflow 

### Automation the processs
- for the feature engineering, since this is a time series regression problem, we can use TSFresh to automate the feature engineering, and apply other ML models like Random Forest, Linear Regression, et. 
- for the model selection, automl can be used to auto-train models and seleting the best model based on performance metric, mlflow can be used to visulize the model performance during model training, and log the model, parameters, and other artifacts.

- for the monitoring of model, we can use grafana to monitering the model real-time perforance. 
