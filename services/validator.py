import json
import logging
from pydantic import ValidationError

from validator.chains.extraction_chains import identification_chain, med_chain, id_parser, med_parser
from langchain.schema import Document

logger = logging.getLogger(__name__)

async def extract_structured(chain: LLMChain, parser: PydanticOutputParser, docs_text: str) -> dict:
    raw_output = await chain.apredict(text=docs_text)
    try:
        parsed_model = parser.parse(raw_output)
        parsed_json  = json.loads(parsed_model.json())
        return {"raw": raw_output, "parsed": parsed_json, "errors": None}
    except ValidationError as e:
        logger.error(f"Couldn’t extract fields: {e}\nRaw LLM output:\n{raw_output}")
        return {"raw": raw_output, "parsed": None, "errors": e.errors()}


def match_patient(id_data: dict | None, med_data: dict | None) -> list[str]:
    issues = []
    if id_data and med_data:
        if id_data["name"].lower().strip() != med_data["name"].lower().strip():
            issues.append(
                f"Name mismatch: ID='{id_data['name']}' vs. Medical='{med_data['name']}'"
            )
        if id_data["dob"] != med_data["dob"]:
            issues.append(
                f"DOB mismatch: ID='{id_data['dob']}' vs. Medical='{med_data['dob']}'"
            )
    else:
        issues.append("Couldn’t perform match because one or both extractions failed.")
    return issues

async def validate_and_match(id_docs: list[Document], med_docs: list[Document]) -> dict:
    id_text  = "\n\n".join(d.page_content for d in id_docs)
    med_text = "\n\n".join(d.page_content for d in med_docs)

    id_result  = await extract_structured(id_chain,  id_parser,  id_text)
    med_result = await extract_structured(med_chain, med_parser, med_text)

    issues = match_patient(id_result["parsed"], med_result["parsed"])

    return {
        "id_raw":     id_result["raw"],
        "id_parsed":  id_result["parsed"],
        "id_errors":  id_result["errors"],
        "med_raw":    med_result["raw"],
        "med_parsed": med_result["parsed"],
        "med_errors": med_result["errors"],
        "match_issues": issues,
    }