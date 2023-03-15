import json

import pymongo
from bson import json_util
from flasgger import Swagger
from flasgger.utils import swag_from
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
swagger = Swagger(app)


def get_db():
    client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
    return client


@app.route("/")
def ping_server():
    return "Welcome to Armani Mongo DB."


@app.route("/ean/<ean>")
@swag_from("swagger_doc/ean.yml")
def get_specific_ean(ean):
    """Return specific EAN"""
    db = ""
    try:
        client = get_db()
        result = client.db_armani.ean_coll.find_one({"EAN": ean})
        print(result)
        if result is None:
            result = {}
        return json.loads(json_util.dumps(result))
    except:
        raise "Errore"
    finally:
        if type(db) == MongoClient:
            db.close()


@app.route("/lt_ratio_price/<th>")
@swag_from("swagger_doc/lt_ratio_price.yml")
def lt_ratio_price(th):
    db = ""
    try:
        client = get_db()
        result = client.db_armani.ean_coll.find(
            {"RATIO_PRICE" : {"$lt": float(th)}},
            {
                "EAN": True,
                "RATIO_PRICE": True,
                "COUNTRY_RATIO_PRICE": True,
                "_id": False,
            },
        ).sort([("RATIO_PRICE", 1)])
        print(result)
        if result is None:
            result = {}
        return json.loads(json_util.dumps(result))
    except:
        raise "Errore"
    finally:
        if type(db) == MongoClient:
            db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
