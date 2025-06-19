from pydantic import BaseModel, Field

class PatientIdentification(BaseModel):
    name: str = Field(..., description="Full name on the ID")
    dob: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    id_number: str = Field(..., description="National ID or Passport number")

class MedicalRecord(BaseModel):
    name: str = Field(..., description="Patient’s name as in medical record")
    dob: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    medical_record_number: str = Field(..., description="Hospital medical record #")
    diagnosis_date: str = Field(..., description="Date of initial cancer diagnosis (YYYY-MM-DD)")
    diagnosis: str = Field(..., description="Cancer type / ICD-10 code")