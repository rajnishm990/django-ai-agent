from django.conf import settings
from langchain_openai import ChatOpenAI


def get_openai_key():
    return settings.TOGETHERAI_API_KEY

def get_openAIModel(model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    if model is None:
        model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_tokens= 1024,
        api_key = get_openai_key(),
        openai_api_base="https://api.together.xyz/v1"
        
    )

