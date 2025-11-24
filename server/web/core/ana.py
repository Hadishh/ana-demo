import os
import pytz
import re
from datetime import datetime
import asyncio

from chat.models import Message


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.debug_report = str()
        self.persona = f"User's Name: {user.name}\nUser's Age: {user.age}\nUser's City: {user.city}\nCurrent time:{str(datetime.now())}"


    async def answer(self, dialogue):
        from core.agents import main_agent
        from core.function_calls import tool_map, Executor, functions_references
        curr_exec = Executor(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            funcs_ref=functions_references
        )
        
        print(dialogue)
        response, log_string = await main_agent.generate_functions_and_responses(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            persona=self.persona, 
            dialogue=dialogue, 
            executor=curr_exec)

        self.debug_report = log_string
        return response, "other"
