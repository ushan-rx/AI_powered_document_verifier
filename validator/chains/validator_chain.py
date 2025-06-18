from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.documents import Document

template = """
You are an identity‐validation assistant. Given the following extracted text:
----
{text}
----
Extract these fields (if present): Name, DOB, ID_number, Issue_date, Expiry_date. 
Then identify any inconsistencies or conflicts (e.g., expiry before issue, mismatched names across docs).
Return JSON:
{{
  "fields": {{ ... }},
  "issues": [ "issue1", ... ]
}}
"""

prompt = PromptTemplate(input_variables=["text"], template=template)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = LLMChain(llm=llm, prompt=prompt)

async def validate(docs: list[Document]):
    full_text = "\n\n".join(d.page_content for d in docs)
    result = await chain.apredict(text=full_text)
    return result  # JSON‐string
