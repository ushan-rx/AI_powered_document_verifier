import os

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas import PatientIdentification, MedicalRecord

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.0,
    top_p=1.0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# --- Identification extraction chain ---
id_parser = PydanticOutputParser(pydantic_object=PatientIdentification)
id_format_instructions = id_parser.get_format_instructions()
id_prompt = PromptTemplate(
    input_variables=["text"],
    partial_variables={"format_instructions": id_format_instructions},
    template=(
        "Extract the patient’s identification details from the text below.\n\n"
        "{text}\n\n"
        "Respond in JSON format as follows:\n"
        "{format_instructions}"
    ),
)
identification_chain = LLMChain(llm=llm, prompt=id_prompt)

# --- Medical-record extraction chain ---
med_parser = PydanticOutputParser(pydantic_object=MedicalRecord)
med_format_instructions = med_parser.get_format_instructions()
med_prompt = PromptTemplate(
    input_variables=["text"],
    partial_variables={"format_instructions": med_format_instructions},
    template=(
        "Extract these fields from the patient’s medical document:\n"
        "– name, dob, medical_record_number, diagnosis_date, diagnosis\n\n"
        "{text}\n\n"
        "Respond in JSON format as follows:\n"
        "{format_instructions}"
    ),
)
med_chain = LLMChain(llm=llm, prompt=med_prompt)
