from fastapi import FastAPI

from app.routes import patients, doctors, users, departments, appointments, doctor_availability, lab_services, lab_requests, lab_reports, wards, beds, admissions, bills

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
app.include_router(lab_requests.router)
app.include_router(lab_reports.router)
app.include_router(wards.router)
app.include_router(beds.router)
app.include_router(admissions.router)
app.include_router(bills.router)


@app.get("/")
def root():
    return {"message": "Hospital Backend API is running"}