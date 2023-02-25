"""Api."""

from flask import Flask, request
from flask_restful import Api, Resource
from pymongo.database import Database
from pymongo.mongo_client import MongoClient


def get_mongo_client(params: dict) -> Database:
    """Spawn MongoDB client."""
    # Spawn client and return dbc
    client = MongoClient(
        f"mongodb://{params['DB_USERNAME']}:"
        f"{params['DB_PASSWORD']}@"
        f"{params['DB_IP_ADDR']}:"
        f"{params['DB_PORT']}/"
    )
    return client[params["DB_NAME"]]


params = {
    "DB_USERNAME": "root",
    "DB_PASSWORD": "example",
    "DB_IP_ADDR": "localhost",
    "DB_PORT": "27017",
    "DB_NAME": "db_armani",
}


class Ean(Resource):
    """Class to manage API requests."""

    @staticmethod
    def get():
        """Get method."""
        db = get_mongo_client(params)
        data_in = request.args.to_dict()
        if "ean" not in data_in:
            return "BESTEMMIA"
        else:
            doc = db["transaction_cl"].find_one(
                {"EAN": data_in["ean"]}, projection={"_id": False}
            )
            return doc


app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":

    # Add endpoints
    api.add_resource(Ean, "/get_ean")

    # Run Flask API
    app.run(debug=False, host="0.0.0.0", port=5000)
