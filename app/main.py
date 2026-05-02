from fastapi import FastAPI

from app.routes import patients, doctors

app = FastAPI(
    title="Hospital Backend System",
    version="1.0.0"
)

app.include_router(patients.router)
app.include_router(doctors.router)



@app.get("/")
def root():
    return {"message": "Hospital Backend API is running"}