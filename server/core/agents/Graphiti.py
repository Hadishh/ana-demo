import os
import json
import asyncio
from datetime import datetime

from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.nodes import EpisodeType
from tqdm import tqdm

class GraphitiAgent:
    async def initialize_database(self):
        await self.graphiti.build_indices_and_constraints()
        with open("kg/initial_docs.txt", "r") as f:
                for i, line in enumerate(tqdm(f.readlines())): 
                    try:
                        await self.graphiti.add_episode(
                            name=f"import:data:{i}",
                            episode_body=line.strip(),
                            source=EpisodeType.text,
                            source_description="docstring data",
                            reference_time=datetime.now(),
                        )
                    except:
                        print(f"Ignoring doc : {line}")
                    
        result = await self.graphiti.search("who is the son of arthur morgan?")
        pass


    def __init__(self, 
                 api_key, 
                 llm_name, llm_url, 
                 embedder_name, embedder_url, 
                 neo4j_uri, neo4j_user, neo4j_password
                ):
        
        
        llm_config = LLMConfig(
            api_key=api_key,
            model=llm_name,
            base_url=llm_url
        )
        self.llm_client = OpenAIClient(config=llm_config)
        embedder_config = OpenAIEmbedderConfig(
            api_key=api_key,
            embedding_model=embedder_name,
            base_url=embedder_url,
            embedding_dim=1024
        )
        self.embedder = OpenAIEmbedder(config=embedder_config)

        self.graphiti = Graphiti(
            uri=neo4j_uri,
            user=neo4j_user,
            password=neo4j_password,
            llm_client=self.llm_client,
            embedder=self.embedder
        )

