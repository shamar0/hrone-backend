🗃️ MongoDB Database Setup
This project uses MongoDB to store data for the e-commerce backend.

Database Name: hrone_db

Collections Used:
products: Stores all the product details like name, price, and available sizes.
orders: Stores orders placed by users along with product details, quantity and total price.

The MongoDB connection is established using the pymongo library, and the connection URI is securely managed via the .env file.



🧩 Pydantic Models for Data Validation
This project uses Pydantic (FastAPI's standard for data validation) to define structured models for input and output data. 
It ensures all incoming request bodies are validated.

📦 Models Used:
class Size(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class ProductDetails(BaseModel):
    name: str
    id: str

class Items(BaseModel):
    productDetails: ProductDetails
    qty: int

class Order(BaseModel):
    userId: str
    items: List[Items]
    total: float

class ItemsReq(BaseModel): 
    productId: str
    qty: int

class OrderReq(BaseModel): #when user send post request for order
    userId: str
    items: List[ItemsReq]



🔄 Pagination Logic Explained
Pagination is implemented for both GET /products and GET /orders/{userId}.

📌 Fields:
offset: The number of documents to skip while paginating (sorted by _id)
limit: number of items to return
next: starting index for the next page
previous: starting index for the previous page

🔍 Examples:
| Total Count | Offset | Limit | Next | Previous |
| ----------- | ------ | ----- | ---- | -------- |
| 2           | 0      | 5     | null | null     |
| 10          | 1      | 3     | 5    | null     |
| 10          | 3      | 3     | 7    | 1        |

✅ next is set only if more records are available after current set
✅ previous is set if you are past the first page
✅ If you're on the last page or data is less than limit, next is null
✅ If you're on the first page, previous is null






