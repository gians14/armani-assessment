"""MongoDB."""

import pandas as pd
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
db = client["db_armani"]
prices_cl = db["prices"]
transaction_cl = db["transactions"]

df_transaction = pd.read_csv("transactions.csv", sep=",")

print(df_transaction.head())

print(client.list_database_names())
