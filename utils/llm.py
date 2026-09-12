import os
import itertools
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from gateway.model_router import get_model_for_stage

load_dotenv()


def _load_groq_keys():
    raw = os.getenv("GROQ_API_KEYS") or os.getenv("GROQ_API_KEY", "")
    keys = [k.strip() for k in raw.split(",") if k.strip()]

    if not keys:
        raise RuntimeError(
            "No Groq API keys configured. Set GROQ_API_KEY (single) or "
            "GROQ_API_KEYS (comma-separated, for rotation) in .env"
        )

    return keys


_GROQ_KEYS = _load_groq_keys()
_groq_key_cycle = itertools.cycle(range(len(_GROQ_KEYS)))


def get_groq_model(model_name: str, api_key: str):
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name
    )


def get_gemini_model(model_name: str):
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def _call_groq_with_rotation(prompt: str, model_name: str):
    """Try every configured Groq key before giving up, so one rate-limited
    key doesn't take the whole stage down. Round-robins the starting key
    across calls so load spreads evenly instead of hammering key #1."""
    start = next(_groq_key_cycle)
    last_error = None

    for offset in range(len(_GROQ_KEYS)):
        index = (start + offset) % len(_GROQ_KEYS)

        try:
            llm = get_groq_model(model_name, _GROQ_KEYS[index])
            response = llm.invoke(prompt)
            return response.content
        except Exception as error:
            last_error = error
            continue

    raise last_error


def generate_response(prompt: str, stage_name: str):
    model_config = get_model_for_stage(stage_name)

    provider = model_config["primary"]
    model_name = model_config["model"]

    try:
        if provider == "groq":
            return _call_groq_with_rotation(prompt, model_name)

        elif provider == "gemini":
            llm = get_gemini_model(model_name)
            response = llm.invoke(prompt)
            return response.content

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as primary_error:
        fallback_provider = model_config.get("fallback")

        if fallback_provider == "groq":
            return _call_groq_with_rotation(prompt, "openai/gpt-oss-120b")

        if fallback_provider == "gemini":
            llm = get_gemini_model("gemini-2.5-flash")
            response = llm.invoke(prompt)
            return response.content

        raise primary_error
