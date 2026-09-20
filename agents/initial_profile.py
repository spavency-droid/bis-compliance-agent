import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from models.product_profile import ProductProfile


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


SYSTEM_PROMPT = """
You extract an initial product profile from a manufacturer's
product description.

Rules:
1. Extract only information explicitly supported by the description.
2. Do not invent missing information.
3. Leave unknown fields empty.
4. Return ONLY valid JSON.
5. The JSON must contain exactly these fields:
   product_name
   product_type
   materials
   age_group
   power_type
   intended_use
   features

Field types:
- product_name: string
- product_type: string
- materials: list of strings
- age_group: string
- power_type: string
- intended_use: string
- features: list of strings

Do not include markdown or ```json.
"""


def extract_product_profile(
    product_description: str,
) -> ProductProfile:

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Manufacturer's product description:

{product_description}

Extract the initial product profile.

Return ONLY the complete JSON profile.
"""
        ),
    ]

    response = llm.invoke(messages)

    response_text = response.content.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    data = json.loads(response_text)

    return ProductProfile(**data)