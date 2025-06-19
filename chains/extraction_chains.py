from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser

from validator.schemas import PatientIdentification, MedicalRecord

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# --- Identification extraction chain ---
# parse the output into a PatientIdentification schema
id_parser = PydanticOutputParser(pydantic_object=PatientIdentification)
id_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Extract the patient’s identification details from the text below.\n\n"
        "{text}\n\n"
        "Return ONLY valid JSON matching this schema:\n"
        "{id_parser.schema}"
    ),
)
identification_chain = LLMChain(llm=llm, prompt=id_prompt)

# --- Medical-record extraction chain ---
# parse the output into a MedicalRecord schema
med_parser = PydanticOutputParser(pydantic_object=MedicalRecord)
med_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Extract these fields from the patient’s medical document:\n"
        "– name, dob, medical_record_number, diagnosis_date, diagnosis\n\n"
        "{text}\n\n"
        "Return ONLY valid JSON matching this schema:\n"
        "{med_parser.schema}"
    ),
)
med_chain = LLMChain(llm=llm, prompt=med_prompt)