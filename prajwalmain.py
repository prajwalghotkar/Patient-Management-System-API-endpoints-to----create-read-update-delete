from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Full legal name of the patient", examples=["Prajwal Ghotkar"], min_length=2, max_length=100)]
    city: Annotated[str, Field(..., description="The city where the patient resides", examples=["Austin"])]
    age: Annotated[int, Field(..., description="Current age of the patient in years", examples=[24], ge=0, le=120)]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, min_length=2, max_length=100)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, ge=0, le=120)]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.get("/")
def read_root():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {'message': 'This is the Patient Management System API, designed to manage patient records efficiently.'}

@app.get('/view')
def view_all_patients():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient_by_id(patient_id: str = Path(..., description="ID of the patient in the database")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found in database")

@app.get("/patient")
def get_patient_by_query(
    patient_id: str = Query(..., description="ID of the patient in the database")
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found in database")

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, or bmi"),
    order: str = Query("asc", description="Sort in asc or desc order")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Select between 'asc' and 'desc'")
    
    data = load_data()

    sort_order = True if order == "desc" else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # Load existing data 
    data = load_data()

    # Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists in the database")

    # Add new patient to the database
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Save the updated data to the JSON file
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "New patient added successfully."})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found in database")
    
    # Get existing patient data
    existing_data = data[patient_id]
    
    # Update only the fields that are provided
    update_data = patient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        existing_data[field] = value
    
    # Recalculate BMI and verdict by creating a temporary Patient object
    temp_patient_data = {"id": patient_id, **existing_data}
    updated_patient = Patient(**temp_patient_data)
    
    # Update the data with recalculated fields
    data[patient_id] = updated_patient.model_dump(exclude=["id"])
    
    # Save the updated data
    save_data(data)
    
    return {"message": "Patient updated successfully"}

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found in database")
    
    del data[patient_id]
    save_data(data)
    
    return {"message": "Patient deleted successfully"}