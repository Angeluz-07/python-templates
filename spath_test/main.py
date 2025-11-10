from fastapi import FastAPI
from repository import get_repository, Task
from fastapi.middleware.cors import CORSMiddleware
from repository_t import get_customer_repository,get_subscription_repository, Customer

app = FastAPI()

# Handle CORS in local dev
origins= [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_methods=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}

# repository
repository = get_repository()

@app.get("/tasks")
def get_tasks():
    return {"tasks": repository.get_all()}


@app.post("/tasks")
def add_task(new_task: Task):
    repository.add(new_task)
    return {"message": repository.get_all()}
    

@app.post("/tasks/{id}/")
def update_task_status(id: int):
    item = repository.get_by_id(id)
    item.status = not (item.status)
    return {"task": item}

customer_repository = get_customer_repository()
@app.get("/customers")
def get_customers():
    return {"customers": customer_repository.get_all()}


@app.post("/customers")
def add_customer(new_item: Customer):
    customer_repository.add(new_item)
    return {"message": customer_repository.get_all()}

subscriptions_repository = get_subscription_repository()
@app.post("/subscriptions")
def subscribe_customer(customer_id: int, plan_id:int ):
    subscriptions_repository.subscribe(customer_id, plan_id)
    return {"message": subscriptions_repository.get_all()}


from repository_t import MongoDBEventRepository
event_repo = MongoDBEventRepository()            
@app.post("/payments/simulate")
def subscribe_customer(customer_id: int, plan_id:int , amount:float):
    from datetime import datetime
    timestamp =datetime.now()
    status=True
    event_repo.add_event(customer_id, plan_id, amount, timestamp, status)
    return {"message": "payment succesful"}
