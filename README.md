# Patient Management System API
# 🏥 Patient Management System API

## 📖 Overview
The **Patient Management System API** is a RESTful backend application built with **FastAPI** to manage patient medical records.  
It provides endpoints to **create, read, update, delete (CRUD)** patient data and supports additional features like **sorting by BMI, weight, or height**.  

Patient data is stored in a JSON file (`patients.json`), making it lightweight and easy to run without needing a full database.

---

## 🚀 Features
- ✅ **CRUD operations** for patient records  
- ✅ **BMI calculation & health verdict** (Underweight, Normal, Overweight, Obese)  
- ✅ **Sorting** by `height`, `weight`, or `BMI`  
- ✅ **Validation** using Pydantic (age, height, weight, gender, name length)  
- ✅ **JSON file storage** (simple, lightweight)  

---

## 📂 Project Structure
PatientAPI/

-->prajwalmain.py      # FastAPI application (your code)
-->patients.json       # Stores patient records
-->requirements.txt    # Dependencies (fastapi, uvicorn, pydantic)

---
### requirements.txt
```
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.9.2

```
- fastapi --> Main framework for building APIs.
- uvicorn --> ASGI server to run FastAPI apps.
- pydantic --> Data validation and models (your Patient schemas).

---
## 📊 Data Models

### Patient (`Patient`)
<img width="493" height="291" alt="image" src="https://github.com/user-attachments/assets/8e697c80-88cb-4f5d-9d4a-296265a98426" />

### Patient Update (`PatientUpdate`)
- All fields optional.  
- Used for **PUT** requests (partial update).
---
## ⚡ API Endpoints

### 🔹 General
- `GET /` --> Welcome message  
- `GET /about` --> Project description  

### 🔹 View Patients
- `GET /view` --> Returns all patients  
- `GET /patient/{patient_id}` --> Get patient by **path parameter**  
- `GET /patient?patient_id=P001` --> Get patient by **query parameter**  

### 🔹 Sorting
- `GET /sort?sort_by=bmi&order=asc`  
  - `sort_by`: `"height"`, `"weight"`, `"bmi"`  
  - `order`: `"asc"` or `"desc"`  

### 🔹 Create
- `POST /create`  
Example:
```
{
  "id": "P001",
  "name": "Prajwal Ghotkar",
  "city": "Austin",
  "age": 24,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
```

### 🔹 Update

- PUT /update/{patient_id}
- Partial update (only send fields you want to update).

```
{
  "city": "New York",
  "weight": 75
}

```

###🔹 Delete

- DELETE /delete/{patient_id}
- Deletes a patient from the database.

---
# 🧮 BMI Calculation
```
BMI = weight / (height^2)
```
#### Verdict Categories:

- BMI < 18.5 --> Underweight
- 18.5 ≤ BMI < 25 --> Normal weight
- 25 ≤ BMI < 30 --> Overweight
- BMI ≥ 30 --> Obese

---

# 🛠️ Tech Stack

- FastAPI – API framework
- Pydantic – Data validation
- Uvicorn – ASGI server
- JSON – Lightweight data storage

---

<img width="1865" height="388" alt="Screenshot 2025-08-27 123557" src="https://github.com/user-attachments/assets/044e482f-ff43-4e4f-942b-ab25790eaa0f" />
<img width="1920" height="301" alt="Screenshot 2025-08-27 123611" src="https://github.com/user-attachments/assets/26497cca-f6ef-4c4d-b3a1-efdffa95cf9d" />
<img width="1887" height="961" alt="Screenshot 2025-08-27 123658" src="https://github.com/user-attachments/assets/2ab74010-ba78-42c7-a490-e5645f523ee3" />
<img width="1876" height="951" alt="Screenshot 2025-08-27 123708" src="https://github.com/user-attachments/assets/5978fd42-bbe2-4453-836d-5ce713de4715" />
<img width="1920" height="925" alt="Screenshot 2025-08-27 123805" src="https://github.com/user-attachments/assets/8e48d6a7-47a1-4aaa-8706-efd7c1102aed" />
<img width="1885" height="933" alt="Screenshot 2025-08-27 123827" src="https://github.com/user-attachments/assets/d914685d-f387-430f-aca1-e75ae7bff2b0" />
<img width="1781" height="892" alt="Screenshot 2025-08-27 123901" src="https://github.com/user-attachments/assets/248fcce8-a8c0-41ae-8390-6481e9177812" />






