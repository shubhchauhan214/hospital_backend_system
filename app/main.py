from fastapi import FastAPI

from app.routes import patients, doctors, users, departments, appointments

app = FastAPI(
    title="Hospital Backend System",
    version="1.0.0"
)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(users.router)
app.include_router(departments.router)
app.include_router(appointments.router)



@app.get("/")
def root():
    return {"message": "Hospital Backend API is running"}