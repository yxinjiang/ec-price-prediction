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
Show in 'data model diagram.pptx

### Model building
1. After EDA, I found that the resale EC price is highly correlated to the floor area of the unit, the years after lease commencing, less correlated to the location of the EC



2. I use Prophet to build several time-series forecasting models based on the years after 