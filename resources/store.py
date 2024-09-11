from uuid import uuid4
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items


blp = Blueprint("store", __name__, description="Operations on stores", url_prefix="/store")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        if store_id in stores:
            return {"store": stores[store_id], "store_id": store_id}, 200
        else:
            abort(404, message="Store not found") # 200 is the status code for success

    def delete(self, store_id):
        if store_id not in stores:
            abort(404, message="Store not found")
        del stores[store_id]
        return {"message": "Store deleted"}, 200
    
    def put(self, store_id): # update store
        if store_id not in stores:
            abort(404, message="Store not found") # 404 is the status code for not found
        # valdiate request data
        request_data = request.get_json()
        if "name" not in request_data:
            abort(400, message="Invalid request data")
        stores[store_id].update(request_data) # update store with new data / another option is: item |= request_data
        return stores[store_id], 200
    

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        stores_list = list(stores.values())
        return {"stores": stores_list, "stores_size": len(stores_list)}, 200 # 200 is the status code for success
    
    def post(self):
        request_data = request.get_json()
        # data validation
        if "name" not in request_data:
            abort(400, message="Invalid request data. Ensure you have a name field included in JSON payload")
        # verify if store already exists
        for store in stores.values():
            if store["name"]==request_data["name"]:
                abort(400, message="Store already exists")
        store_id = uuid4().hex # generate a random id
        # new_store = {
        #     'name': request_data['name'],
        #     'items': []
        # }
        new_store = {**request_data, "items": [], "id": store_id}
        stores[store_id] = new_store
        return new_store, 201 # 201 is the status code for created / success /200 is default


@blp.route("/store/<string:store_id>/item")
class StoreItems(MethodView):
    def get(self, store_id):
        if store_id not in stores:
            abort(404, message="Store not found")
        store = stores[store_id]
        return {"items": store["items"], "items_size": len(store["items"])}, 200
