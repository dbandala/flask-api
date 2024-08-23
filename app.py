from uuid import uuid4
from flask import Flask, request, jsonify
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)



###########################################################################
#### GET METHODS
###########################################################################
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}, 200 # 200 is the status code for success

# get information from store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    if store_id in stores:
        return {"store": stores[store_id], "store_id": store_id}, 200
    else:
        abort(404, message="Store not found") # 200 is the status code for success

# get items from store
@app.get("/store/<string:store_id>/item")
def get_items_from_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found")
    return {"items": stores[store_id]["items"], "store_name": stores[store_id]["name"], "store_id": store_id, "message": "Items found"}, 200
    # for store in stores:
    #     if store["name"]==name:
    #         return {"items": store["items"], "store": store["name"], "store_id": stores.index(store), "message": "Items found"}, 200 # 200 is the status code for success
    # return {"message": "Store not found"}, 404 # 404 is the status code for not found

# get items from store
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}, 200 # 200 is the status code for success

# get information from item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    if item_id in items:
        return {"item": items[item_id], "item_id": item_id}, 200
    else:
        abort(404, message="Item not found")



###########################################################################
#### GET METHODS
###########################################################################
@app.post("/store")
def create_store():
    request_data = request.get_json()
    store_id = uuid4().hex # generate a random id
    # new_store = {
    #     'name': request_data['name'],
    #     'items': []
    # }
    new_store = {**request_data, "items": [], "id": store_id}
    stores[store_id] = new_store
    return new_store, 201 # 201 is the status code for created / success /200 is default

# create items within stores
#@app.post("/store/<string:name>/item")
@app.post("/item")
def create_item_in_store():
    request_data = request.get_json()
    # validate fields
    if "store_id" not in request_data or "name" not in request_data or "price" not in request_data:
        abort(400, message= "Invalid request data") # 400 is the status code for bad request
    if request_data["store_id"] not in stores:
        abort(404, message= "Store not found")

    # verify if store exists
    # store = next(filter(lambda x: x["name"]==name, stores), None)
    # if store is None:
    #     abort(404, message="Store not found")

    store = stores[request_data["store_id"]]
    
    # verify if item already exists
    if next(filter(lambda x: x["name"]==request_data["name"], store["items"]), None) is not None:
        abort(400, message="Item already exists")
    
    item_id = uuid4().hex
    new_item = {**request_data, "id": item_id}
    items[item_id] = new_item

    # append item to store
    store["items"].append(new_item)

    # for store in stores:
    #     if store["name"]==name:
    #         new_item = {
    #             'name': request_data['name'],
    #             'price': request_data['price']
    #         }
    #         store["items"].append(new_item)
    #         return new_item, 201

    return new_item, 201


###########################################################################
#### DELETE METHODS
###########################################################################
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found")
    del stores[store_id]
    return {"message": "Store deleted"}, 200

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
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
    
    return {"message": "Item deleted"}, 200



###########################################################################
#### PUT METHODS
###########################################################################
@app.put("/store/<string:store_id>")
def update_store(store_id):
    if store_id not in stores:
        abort(404, message="Store not found") # 404 is the status code for not found
    # valdiate request data
    request_data = request.get_json()
    if "name" not in request_data:
        abort(400, message="Invalid request data")
    stores[store_id].update(request_data) # update store with new data / another option is: item |= request_data
    return stores[store_id], 200

@app.put("/item/<string:item_id>")
def update_item(item_id):
    if item_id not in items:
        abort(404, message="Item not found") # 404 is the status code for not found
    # valdiate request data
    request_data = request.get_json()
    if "name" not in request_data or "price" not in request_data:
        abort(400, message="Invalid request data") # 400 is the status code for bad request
    items[item_id].update(request_data)
    return items[item_id], 200