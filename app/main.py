from fastapi import FastAPI
from app.database import engine, Base
from app import models

app = FastAPI(title="Hospital Backend System", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return{"message": "Hospital Backend API is running"}

