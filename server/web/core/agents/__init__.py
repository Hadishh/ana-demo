

from config.settings.base import *

from .Graphiti import GraphitiAgent
from .DeepSeekR1 import DeepSeekAgent


graphiti_agent = GraphitiAgent(
        api_key=OPENAI_API_KEY, 
        llm_name=LLM_MODEL_NAME,
        llm_url=OPENAI_BASE_URL_LLM,
        embedder_name=EMBEDDER_MODEL_NAME,
        embedder_url=OPENAI_BASE_URL_EMBEDDING,
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD
    )

main_agent = DeepSeekAgent(
        llm_url=OPENAI_BASE_URL_LLM, 
        llm_name=LLM_MODEL_NAME, 
        api_key=OPENAI_API_KEY
    )