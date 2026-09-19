# BIS Compliance Advisor Agent

An Agentic AI system that helps small manufacturers identify potentially applicable Indian Standards based on their product description.

## Problem

Small manufacturers may find it difficult to identify which Indian Standard may apply to their product. The BIS Compliance Advisor uses conversational clarification, standards retrieval, ranking, and an early-exit mechanism to narrow down relevant standards.

## Key Features

* Conversational product clarification
* Maximum 4 clarification questions
* Adaptive question selection
* Curated BIS standards dataset
* Standards retrieval
* Explainable scoring and ranking
* Early-exit decision based on score margin
* Compliance recommendation report
* Streamlit-based user interface

## Product Categories

The initial prototype focuses on:

1. Toys
2. Electronics / IT Products
3. Food Packaging
4. Textiles

## Technology Stack

* Python
* LangGraph
* LangChain
* Groq API
* Streamlit
* Pandas
* Pydantic
* FAISS
* Git / GitHub

## Architecture

```text
User
  ↓
Streamlit UI
  ↓
LangGraph Workflow
  ↓
Clarification Agent
  ↓
Product Profile
  ↓
Standards Retrieval
  ↓
Scoring Engine
  ↓
Early-Exit Controller
  ├── Continue → Ask Question
  └── Stop → Recommendation
                    ↓
              Report Generation
```

## Important Note

The system provides a recommendation based on the information available in the curated dataset. It is not a substitute for official BIS confirmation or professional compliance advice.

## Team

Built for the Saksham — National Level Agentic AI Hackathon.
