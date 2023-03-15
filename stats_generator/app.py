import time

import pymongo
from EanStats import *

if __name__ == "__main__":

    try:
        df_transaction_read = pd.read_csv(
            "stats_generator/files/transactions.csv", sep=","
        )
        df_prices_read = pd.read_csv("stats_generator/files/prices.csv", sep=",")

        ean_stats = EanStats(df_transaction_read, df_prices_read)

        df_transaction = ean_stats.transaction_preparation()
        df_prices = ean_stats.prices_preparation()

        df_for_stats = ean_stats.pre_stats(df_transaction, df_prices)
        df_stats = ean_stats.stats(df_for_stats)
        to_insert = list(df_stats.apply(lambda x: x.dropna().to_dict(), axis=1))

    except Exception as e:
        print(e)
        raise

    time.sleep(10)
    written = False
    while written == False:
        try:
            client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
            db = client["db_armani"]
            ean_coll = db["ean_coll"]
            ean_coll.drop()
            db.ean_coll.insert_many(to_insert)
            written = True
            print("Written")
        except Exception as e:
            print(f"MongoDb Step Problem: {e}")
