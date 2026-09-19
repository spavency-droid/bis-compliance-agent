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
You update a product profile using the user's latest answer.

Rules:
1. Update only information supported by the user's answer.
2. Keep existing information unchanged unless the user clearly corrects it.
3. Do not invent information.
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


def update_product_profile(
    profile: ProductProfile,
    user_answer: str
) -> ProductProfile:

    current_profile = profile.model_dump_json(indent=2)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Current product profile:

{current_profile}

User's latest answer:

{user_answer}

Update the profile based only on the user's answer.

Return ONLY the complete updated JSON profile.
"""
        ),
    ]

    response = llm.invoke(messages)

    response_text = response.content.strip()

    # Remove markdown fences if the model adds them
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    updated_data = json.loads(response_text)

    return ProductProfile(**updated_data)