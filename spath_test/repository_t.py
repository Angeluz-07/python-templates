
import os
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, or_, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session,relationship
from sqlalchemy.exc import OperationalError
from pydantic import BaseModel
import config
from repository import Repository

class Item(BaseModel):
    pass

class Customer(Item):
    id : int
    name: str
    email: str

# Base class for declarative table definition
Base = declarative_base()

# --- Database Model (Table Definition) ---
class CustomerBase(Base):
    """
    Defines the 'tasks' table structure in PostgreSQL.
    """
    __tablename__ = "customers"

    # In SQL, the primary key (id) is typically an auto-incrementing integer.
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, index=True, nullable=False)
    email = Column(String, default=True, nullable=False)

    # def __repr__(self):
    #     return f"Product(id={self.id}, name='{self.name}', stat={self.status})"

class SubscriptionPlanBase(Base):
    """
    Defines the 'tasks' table structure in PostgreSQL.
    """
    __tablename__ = "subscriptionplans"

    # In SQL, the primary key (id) is typically an auto-incrementing integer.
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, index=True, nullable=False)
    price = Column(Float, default=10)
    billing_cycle = Column(String, default=True, nullable=False)

    # def __repr__(self):
    #     return f"Product(id={self.id}, name='{self.name}', stat={self.status})"

class SubscriptionBase(Base):
    """
    Defines the 'tasks' table structure in PostgreSQL.
    """
    __tablename__ = "subscriptions"
    # In SQL, the primary key (id) is typically an auto-incrementing integer.
    id = Column(Integer, primary_key=True, index=True) 
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('subscriptionplans.id'), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Boolean)

    customer = relationship("CustomerBase") 

    plan = relationship("SubscriptionPlanBase")

# --- Database Engine and Session Setup ---
try:
    # Create the SQLAlchemy engine. 'echo=True' prints SQL statements to the console.
    engine = create_engine(config.SQLALCHEMY_DATABASE_URL, echo=False)

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all defined tables in the database (only if they don't exist)
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL Engine and table creation successful.")
    
except OperationalError as e:
    print(f"\nFATAL: Could not connect to PostgreSQL. Is Docker running?")
    print(f"Connection Error: {e}\n")
    engine = None # Ensure engine is None if connection fails
# --- CRUD Operations ---

def get_db():
    """Dependency that creates a new session and ensures it's closed."""
    if not engine:
        raise ConnectionError("Database connection failed during startup.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostgreSQLCustomerRepository(Repository):
    def __init__(self):    
        # Use the generator function to safely get and close the session
        db_generator = get_db()
        db = next(db_generator) # Get the session instance
    
        # 1. Clear and Add Multiple Items
        db.query(SubscriptionBase).delete()
        db.query(CustomerBase).delete()
        db.query(SubscriptionPlanBase).delete()
        db.commit()

        import random
        items = [
            CustomerBase(id=1,name="alfa", email="sample1@gmail.com"), 
            CustomerBase(id=2,name="beta", email="sample2@gmail.com"), 
            CustomerBase(id=3,name="gama", email="sample3@gmail.com"),
            SubscriptionPlanBase(id=1, name="simple", price=20, billing_cycle="monthly"),# to fix
            SubscriptionPlanBase(id=2, name="ultra", price=40, billing_cycle="yearly")
        ]
        
        db.add_all(items)
        db.commit()
        self.db=db

    def get_all(self):
        result = self.db.query(CustomerBase).all()
        return result

    def add(self, c:Customer):
        item = CustomerBase(id=c.id, name=c.name, email=c.email)
        self.db.add(item)
        self.db.commit()

    def get_by_id(self):
        pass



class PostgreSQLSubscriptionRepository(Repository):
    def __init__(self):    
        # Use the generator function to safely get and close the session
        db_generator = get_db()
        db = next(db_generator) # Get the session instance
    
        # 1. Clear and Add Multiple Items
        db.query(SubscriptionBase).delete()
        db.commit()

        self.db=db

    def get_all(self):
        result = self.db.query(SubscriptionBase).all()
        return result

    def subscribe(self, cid, pid):
        from datetime import datetime
        item = SubscriptionBase(customer_id=cid, plan_id=pid, start_date=datetime.now(), end_date=datetime.now(), status=True)
        self.db.add(item)
        self.db.commit()

    def add(self, c:SubscriptionBase):
        pass

    def get_by_id(self):
        pass

get_customer_repository = lambda : PostgreSQLCustomerRepository()
get_subscription_repository = lambda : PostgreSQLSubscriptionRepository()

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

class MongoDBEventRepository(Repository):
    #client
    #collection
    #tasks: List[str]
    
    def __init__(self):
        self.client = get_mongo_client()
        if not self.client:
            print("Cannot proceed without a database connection. Please ensure Docker/Db is running.")
            return

        self.db = self.client[config.DATABASE_NAME]
        self.collection = self.db[config.COLLECTION_NAME] #use same coll name

        # Clear previous data 
        self.collection.delete_many({})
        #print(f"\n--- Cleared all items from '{COLLECTION_NAME}' collection. ---\n")

        # initial_items = [
        #     {"id":1 ,"name":"My first task", "status":False},
        #     {"id":2 ,"name":"My second task", "status":False},
        #     {"id":3 ,"name":"My third task", "status":False}
        # ]
        # result_many = self.collection.insert_many(initial_items)
        #print(f"1. Added {len(result_many.inserted_ids)} initial items. IDs: {result_many.inserted_ids}")
    

    def get_all(self):
        all_items_cursor = self.collection.find()
        # Use dumps to serialize the MongoDB documents (including ObjectIds) to JSON string for readable output
        print(dumps(list(all_items_cursor), indent=2))
        #return [self.custom_serializer(x) for x in all_items_cursor]
    
    def add_event(self, customer_id, plan_id, amount, timestamp, status):
        single_item = {"customer_id":customer_id ,"plan_id":plan_id, "amount":amount,"timestamp":timestamp, "status":status}
        result_one = self.collection.insert_one(single_item)
        self.get_all()

    def add(self, i: Item):
        pass
        # single_item = {"id":task.id ,"name":task.name, "status":task.status}
        # result_one = self.collection.insert_one(single_item)
        #print(f"\n2. Added a single item. ID: {result_one.inserted_id}")
        #self.tasks.append(task)

    def get_by_id(self, id):
        pass
        # # 4. GET BY ID (Simulated Request 4)
        # #print(f"\n4. [Request 4] Retrieving the first item by its ID: {item_id_to_find}")
        
        # try:
        #     # We must convert the string ID to an ObjectId object for MongoDB to query correctly
        #     query_result = self.collection.find_one({"id": id})
        #     if query_result:
        #         print(dumps(query_result, indent=2))
        #         return self.custom_serializer(query_result)
        #     else:
        #         return None
        #         print("Item not found.")
        # except Exception as e:
        #     print(f"Error finding item by ID: {e}")

    # def custom_serializer(self, task_data):
    #     #task_date={\"_id\": {\"$oid\": \"690bafb9d98fa236275529cf\"}, \"id\": 1, \"name\": \"My first task\", \"status\": false},
    #     id = task_data.get("id", -1)
    #     name = task_data.get("name", "none")
    #     status = task_data.get("status", 0)
    #     return Task(id=id, name=name, status=status)