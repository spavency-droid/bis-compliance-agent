import os

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
You are a Product Compliance Clarification Agent.

Your job is to ask ONE useful clarification question
about a product so that a BIS standard can be identified.

The product profile may contain missing information.

Important rules:
1. Ask only ONE question at a time.
2. Ask about information that is currently missing.
3. Prefer information that can distinguish between possible BIS standards.
4. Do not ask for information that is already known.
5. Keep the question short and easy for a manufacturer to answer.
6. Never invent a BIS standard.
7. Possible information includes:
   - product type
   - material
   - age group
   - power type
   - intended use
   - important product features
"""


def generate_clarification_question(profile: ProductProfile) -> str:
    """
    Generate one clarification question based on the current
    product profile.
    """

    profile_text = profile.model_dump_json(indent=2)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Here is the current product profile:

{profile_text}

Generate the ONE most useful clarification question
that should be asked next.
"""
        ),
    ]

    response = llm.invoke(messages)

    return response.content.strip()