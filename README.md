# Armani Assessment

A brief description of what this project does and who it's for.

# Goal
Starting from the following csv tables:
1. transaction.csv --> Details about sold products in a period
2. prices.csv --> Prices list of products in all countries

Analyze data in order to find misalignment and generate product statistics.
Make statistics queryable via Rest Api.

# Stats for each EAN

1. COUNTRY_RATIO_PRICE --> Check if EAN is sold, on average, over or under list price in each Country.
2. RATIO_PRICE -> Check if EAN is sold, on average, over or under list price overall.
3. SOLD_QUANTITY --> Sold overall
4. SOLD_TOTAL_AMOUNT --> For each Country

# Components
## 1. MongoDB
The MongoDB server in the image listens on the standard MongoDB port, 27017.
You can find a collection called "ean_coll" that contains all the genereted stats.
The service run on Docker Container.

## 2. Mongo-Express
Mongo-Express is a web-based MongoDB admin interface.
The service run on Docker Container.
UI can be reached at this address:

<a href="https://localhost:8081" target="_blank">Mongo-Express</a>

## 3. Flask API Exposer
Service that runs on a specific container useful to expose api for stats interaction. User can interact with the statistics through specific Rest Api.

<a href="http://localhost:5000/apidocs" target="_blank">Api-Doc</a>

## 4. Stats Generator

Python script created to analyze data and create statistics.
The statistics generated are entered into the NoSql MongoDB Database.


# Set up & Go

Make sure you have Docker and Python installed on your environment.

<a href="https://docs.docker.com/get-docker/" target="_blank">Docker</a>
| <a href="https://www.python.org/downloads/" target="_blank">Python</a>


## Execution Docker Services
To run all the container explained above, execute the following command:

```bash
docker compose up
```

Wait a few seconds and the services will be available.

## Execution Python Script - Stats Generator

1. Go to Project Directory Root
2. Set Up Python Venv
```bash
python3 -m venv env
```
```bash
source env/bin/activate
```
```bash
pip install -r stats_generator/requirements.txt
```
```bash
python3 stats_generator/app.py
```

## Authors

- [@gians14](https://github.com/gians14/)
