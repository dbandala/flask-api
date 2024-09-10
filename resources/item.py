import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items


blp = Blueprint("item", __name__, description="Operations on items", url_prefix="/item")

@blp.route("/item/<string:item_id>")
class Store(MethodView):
    def get(self, store_id):
        if store_id in stores:
            return {"store": stores[store_id], "store_id": store_id}, 200
        else:
            abort(404, message="Store not found") # 200 is the status code for success

    def delete(self, store_id):
        pass
