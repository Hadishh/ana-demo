import os
import pytz
import re
from datetime import datetime

from chat.models import Message


class ChatBot:
    def __init__(self, user) -> None:
        self.user = user
        self.debug_report = str()


    def answer(self, message):
        from core.agents import main_agent
        from core.function_calls import tool_map, Executor, functions_references
        curr_exec = Executor(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            funcs_ref=functions_references
        )

        response = main_agent.generate_functions_and_responses(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            persona=None, 
            dialogue=None, 
            executor=curr_exec)

        return response, "other"
