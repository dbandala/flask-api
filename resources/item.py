from uuid import uuid4
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items


blp = Blueprint("Items", __name__, description="Operations on items", url_prefix="/item")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        if item_id in items:
            return {"item": items[item_id], "item_id": item_id}, 200
        else:
            abort(404, message="Item not found")

    def delete(self, item_id):
        if item_id not in items:
            abort(404, message="Item not found")

        # remove item from store
        for store in stores.values():
            for item in store["items"]:
                if item["id"]==item_id:
                    store["items"].remove(item)
                    break
        
        # remove item from items
        del items[item_id]
        # return success message
        return {"message": "Item deleted"}, 200
    
    def put(self, item_id): # update item
        if item_id not in items:
            abort(404, message="Item not found") # 404 is the status code for not found
        # valdiate request data
        request_data = request.get_json()
        # data validation
        if "name" not in request_data or "price" not in request_data:
            abort(400, message="Invalid request data") # 400 is the status code for bad request
        # update item with new data
        items[item_id].update(request_data)
        return items[item_id], 200
    

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        items_list = list(items.values())
        return {"items": items_list, "items_size": len(items_list)}, 200
    
    def post(self):
        request_data = request.get_json()
        # validate fields
        if "store_id" not in request_data or "name" not in request_data or "price" not in request_data:
            abort(400, message= "Invalid request data. Ensure store_id, name and price keys are provided in JSON payload.") # 400 is the status code for bad request
        if request_data["store_id"] not in stores:
            abort(404, message= "Store not found")

        store = stores[request_data["store_id"]]
        
        # verify if item already exists
        if next(filter(lambda x: x["name"]==request_data["name"], store["items"]), None) is not None:
            abort(400, message="Item already exists")
        
        item_id = uuid4().hex
        new_item = {**request_data, "id": item_id}
        items[item_id] = new_item

        # append item to store
        store["items"].append(new_item)

        return new_item, 201
