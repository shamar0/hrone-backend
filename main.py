from typing import Union
from fastapi import FastAPI, status, Query
from db import product_collection
from db import order_collection
from models import Product
from models import Order
from models import OrderReq
from models import Items
from typing import Optional
from bson import ObjectId

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
   

@app.post('/products', status_code=status.HTTP_201_CREATED)
def createProduct(product : Product):
    product_dict = product.dict()
    result = product_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@app.get('/products',  status_code=status.HTTP_200_OK)
def getProduct(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = {"$regex": f"^{size}$", "$options": "i"}


    total_count = product_collection.count_documents(query)

    result = product_collection.find(query).sort("_id").skip(offset).limit(limit)
   
    products = []
    for product in result:
        products.append({
          "id": str(product["_id"]),
          "name" : product["name"],
          "price" : product["price"],
        })

    if(offset>total_count):
        previous = total_count - limit + 1
    elif(offset<limit):
        previous = None
    else:
        previous = offset - limit + 1

    page_info = {
        "next": offset+limit+1 if(offset+limit) < total_count else None,
        "limit": len(products),
        "previous": previous,
    }

    return {
        "data": products,
        "page": page_info
    }

@app.post('/orders', status_code=status.HTTP_201_CREATED)
def createOrder(order: OrderReq):
    order_dict = order.dict()
    user_id = order_dict["userId"]
    total_price = 0
    items: Items = []
    for item in order_dict["items"]:
        product_id = ObjectId(item["productId"])
        res = product_collection.find_one({"_id": product_id})
        total_price += item["qty"] * res["price"]
        items.append({
            "productDetails":{
                "name":res["name"],
                "id": str(res["_id"])
            },
            "qty": item["qty"]
        })

    result = order_collection.insert_one(
               { "userId": order_dict["userId"],
                 "items": items,
                 "total": total_price
               })
    return{"id": str(result.inserted_id)}
    

@app.get('/orders/{userId}', status_code=status.HTTP_200_OK)
def getOrder(
    userId: str,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10 
    ):
    print(f"userId {userId}")
    result = order_collection.find({"userId": userId}).sort("_id").skip(offset).limit(limit)
    total_count = order_collection.count_documents({"userId": userId})

    orders = []
    for order in result:
        orders.append({
          "id": str(order["_id"]),
          "items" : order["items"],
          "total" : order["total"],
        })

    if(offset>total_count):
        previous = total_count - limit + 1
    elif(offset<limit):
        previous = None
    else:
        previous = offset - limit + 1
    
    page_info = {
        "next": offset+limit+1 if(offset+limit) < total_count else None,
        "limit": len(orders),
        "previous": previous
    }

    return {
        "data": orders,
        "page": page_info
    }

