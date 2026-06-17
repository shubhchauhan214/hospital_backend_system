from fastapi import FastAPI

from app.routes import patients, doctors, users, departments, appointments, doctor_availability, lab_services

app = FastAPI(
    title="Hospital Backend System",
    version="1.0.0"
)

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(users.router)
app.include_router(departments.router)
app.include_router(appointments.router)
app.include_router(doctor_availability.router)
app.include_router(lab_services.router)



@app.get("/")
def root():
    return {"message": "Hospital Backend API is running"}