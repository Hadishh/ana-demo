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


    def answer(self, message):
        from core.agents import main_agent
        from core.function_calls import tool_map, Executor, functions_references
        curr_exec = Executor(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            funcs_ref=functions_references
        )
        dialogue = Message.objects.filter(owner=self.user).order_by("-date")[:10]
        
        dialogue = [
            {"id": utterance.id, "text": utterance.text} for utterance in dialogue
        ]
        dialogue.insert(0, {"id": -1, "text": message["text"]})
        print(dialogue)
        response = asyncio.run(main_agent.generate_functions_and_responses(
            tool_registry=tool_map, 
            action_registry={"function_registry": {}}, 
            persona=self.persona, 
            dialogue=dialogue, 
            executor=curr_exec))

        return response, "other"
