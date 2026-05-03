# core/dependencies.py

from services.llm_service import LLMService


def get_llm_service():
    return LLMService()