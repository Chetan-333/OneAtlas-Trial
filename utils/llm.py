import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from gateway.model_router import get_model_for_stage

load_dotenv()


def get_groq_model(model_name: str):
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model_name
    )


def get_gemini_model(model_name: str):
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def generate_response(prompt: str, stage_name: str):
    model_config = get_model_for_stage(stage_name)

    provider = model_config["primary"]
    model_name = model_config["model"]

    try:
        if provider == "groq":
            llm = get_groq_model(model_name)
            response = llm.invoke(prompt)
            return response.content

        elif provider == "gemini":
            llm = get_gemini_model(model_name)
            response = llm.invoke(prompt)
            return response.content

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as primary_error:
        fallback_provider = model_config.get("fallback")

        if fallback_provider == "gemini":
            llm = get_gemini_model("gemini-1.5-flash")
            response = llm.invoke(prompt)
            return response.content

        if fallback_provider == "groq":
            llm = get_groq_model("llama-3.3-70b-versatile")
            response = llm.invoke(prompt)
            return response.content

        raise primary_error