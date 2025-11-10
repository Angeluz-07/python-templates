
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

from abc import ABC, abstractmethod

class Item(BaseModel):
    pass

# Repository Interface
class Repository(ABC):
    @abstractmethod
    def get_all(self, id: int) -> Item | None:
        pass
    
    @abstractmethod
    def add(self, item: Item):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Item | None:
        pass

class Task(Item):
    id : int
    name: str
    status: bool

class InMemoryTasksRepository(Repository):
    tasks: List[str]
    
    def __init__(self):
        self.tasks = [
            Task(id=1,name="My first task", status=False), 
            Task(id=2,name="My second task",status=False), 
            Task(id=3,name="My third task", status=False)
        ]

    def get_all(self):
        return self.tasks
    
    def add(self, task: Task):
        self.tasks.append(task)

    def get_by_id(self, id):
        for x in self.tasks:
            if x.id == id:
                return x
        return None


get_repository = lambda : InMemoryTasksRepository()

# NoSql Repo

import config 
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps # Used to correctly serialize ObjectId for printing

def get_mongo_client():
    """Establishes and returns a MongoDB client connection."""
    try:
        client = MongoClient(config.MONGO_URI)
        # The ismaster command is a lightweight way to verify a connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # In a real app, you would raise an exception or handle the error gracefully
        return None


class MongoDBTasksRepository(Repository):
    #client
    #collection
    #tasks: List[str]
    
    def __init__(self):
        self.client = get_mongo_client()
        if not self.client:
            print("Cannot proceed without a database connection. Please ensure Docker/Db is running.")
            return

        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.COLLECTION_NAME]

        # Clear previous data 
        self.collection.delete_many({})
        #print(f"\n--- Cleared all items from '{COLLECTION_NAME}' collection. ---\n")

        initial_items = [
            {"id":1 ,"name":"My first task", "status":False},
            {"id":2 ,"name":"My second task", "status":False},
            {"id":3 ,"name":"My third task", "status":False}
        ]
        result_many = self.collection.insert_many(initial_items)
        #print(f"1. Added {len(result_many.inserted_ids)} initial items. IDs: {result_many.inserted_ids}")
    

    def get_all(self):
        all_items_cursor = self.collection.find()
        # Use dumps to serialize the MongoDB documents (including ObjectIds) to JSON string for readable output
        # print(dumps(list(all_items_cursor), indent=2))
        return [self.custom_serializer(x) for x in all_items_cursor]
    
    def add(self, task: Task):
        single_item = {"id":task.id ,"name":task.name, "status":task.status}
        result_one = self.collection.insert_one(single_item)
        #print(f"\n2. Added a single item. ID: {result_one.inserted_id}")
        #self.tasks.append(task)

    def get_by_id(self, id):
        # 4. GET BY ID (Simulated Request 4)
        #print(f"\n4. [Request 4] Retrieving the first item by its ID: {item_id_to_find}")
        
        try:
            # We must convert the string ID to an ObjectId object for MongoDB to query correctly
            query_result = self.collection.find_one({"id": id})
            if query_result:
                print(dumps(query_result, indent=2))
                return self.custom_serializer(query_result)
            else:
                return None
                print("Item not found.")
        except Exception as e:
            print(f"Error finding item by ID: {e}")

    def custom_serializer(self, task_data):
        #task_date={\"_id\": {\"$oid\": \"690bafb9d98fa236275529cf\"}, \"id\": 1, \"name\": \"My first task\", \"status\": false},
        id = task_data.get("id", -1)
        name = task_data.get("name", "none")
        status = task_data.get("status", 0)
        return Task(id=id, name=name, status=status)

# get_repository = lambda : MongoDBTasksRepository()

# get_repository = lambda : PostgreSQLTasksRepository()


# # --- CRUD Operations ---

# def get_db():
#     """Dependency that creates a new session and ensures it's closed."""
#     if not engine:
#         raise ConnectionError("Database connection failed during startup.")
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def add_multiple_items(db: Session):
#     """Adds a list of products to the database."""
#     items = [
#         Product(name="Desk", price=250.00, in_stock=True, category="Furniture"),
#         Product(name="Chair", price=120.00, in_stock=True, category="Furniture"),
#         Product(name="Lamp", price=45.99, in_stock=False, category="Lighting"),
#     ]
#     db.add_all(items)
#     db.commit()
#     print(f"1. Added {len(items)} initial items to the products table.")
#     # Return the ID of the first item for demonstration purposes
#     return items[0].id 


# def add_one_item(db: Session):
#     """Adds a single product to the database."""
#     item = Product(name="Notebook", price=5.99, in_stock=True, category="Stationery")
#     db.add(item)
#     db.commit()
#     db.refresh(item) # Fetches the auto-generated ID from the DB
#     print(f"2. Added a single item (ID: {item.id}).")


# def get_all_items(db: Session) -> List[Product]:
#     """Retrieves all products from the database."""
#     print("\n3. Retrieving all items:")
#     # Query for all instances of the Product model
#     products = db.query(Product).all()
#     return products


# def get_by_id(db: Session, product_id: int) -> Optional[Product]:
#     """Retrieves a single product by its primary key ID."""
#     print(f"\n4. Retrieving item by ID: {product_id}")
#     # Query the Product model using the primary key
#     product = db.query(Product).filter(Product.id == product_id).first()
#     return product


# def main_demonstration():
#     """Runs the full CRUD demonstration."""
#     if not engine:
#         print("Cannot run demonstration without a successful database connection.")
#         return

#     # Use the generator function to safely get and close the session
#     db_generator = get_db()
#     db = next(db_generator) # Get the session instance

#     try:
#         # 1. Clear and Add Multiple Items
#         db.query(Product).delete()
#         db.commit()
#         print("\n--- Cleared all items from 'products' table. ---")
#         first_item_id = add_multiple_items(db)

#         # 2. Add One Item
#         add_one_item(db)

#         # 3. Get All Items
#         all_products = get_all_items(db)
#         for product in all_products:
#             print(f"   -> Found: {product}")

#         # 4. Get By ID
#         found_product = get_by_id(db, first_item_id)
#         if found_product:
#             print(f"   -> Found item: {found_product}")
#         else:
#             print(f"   -> Item with ID {first_item_id} not found.")

#     except Exception as e:
#         print(f"\nAn error occurred during database operations: {e}")
#     finally:
#         # Close the session after use
#         try:
#             db_generator.close()
#         except:
#             pass # Ignore if already closed


# if __name__ == "__main__":
#     # Ensure your Docker service is running before executing this script:
#     # docker compose --env-file dev.env up -d
#     main_demonstration()