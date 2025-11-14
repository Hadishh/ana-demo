import os
from datetime import datetime
import copy
from openai import OpenAI

from config.settings.base import REPLY_PROMPT_PATH, FUNCTION_CALLS_PROMPT_PATH
from .agent_base import Agent
from .utils import read_file


class DeepSeekAgent(Agent):
    def __load_llm_client(self, url, api_key):
        self.llm_client = OpenAI(
            base_url=url,
            api_key=api_key,
        )

    def __init__(self, llm_url, llm_name, api_key):
        super().__init__()
        self.model_name= llm_name
        self.__load_llm_client(llm_url, api_key)

        self.MAX_NEW_TOKENS = 16384
        self.temperature= 0.6
    
    async def generate_functions_and_responses(self, tool_registry, action_registry, persona, dialogue, executor):
        log_string = str()
        functions = self._create_message_for_functions(tool_registry, action_registry, dialogue, persona)
        res = self.llm_client.completions.create(
            model=self.model_name,
            prompt=functions,
            max_tokens=self.MAX_NEW_TOKENS,
            temperature=0.6
        )

        items = res.choices[0].text.split("</think>")[-1].split("\n")
        final_functions = []
        res_item = {}
        for item in items:
            item = item.lower()
            if "function name: " in item:
                if "name" in res_item:
                    final_functions.append(copy.deepcopy(res_item))
                    res_item = {}
                res_item["name"] = item.replace("function name: ", "").split(",")[0]
                res_item["parameters"] = {}
            elif "argument name: " in item:
                arg_name = ""
                arg_val = ""
                if "value: " in item:
                    arg_name = item.split("value: ")[0].replace("argument name: ", "").split(",")[0]
                    arg_val = item.split("value: ")[1]

                if arg_name != "":
                    if not "parameters" in res_item:
                        res_item["parameters"] = {}
                    res_item["parameters"][arg_name] = arg_val
                    
        if "name" in res_item:
            final_functions.append(res_item)

        function_results = await executor.execute(final_functions)
        log_string = "Calling Functions:"

        for item in function_results:
            output = function_results[item]["output"]
            log_string += f'\n{item}\nOutput:\n{output}'
        
        log_string += "\n==================End of Functions========================="

        log_string += f"\nPersonal Information:\n{persona}"
        log_string += "\n==================End of Personal Information=============="
        dialogue_prompt = self._create_dialogue_message(persona, dialogue, function_results)
        response = self.llm_client.completions.create(
            model=self.model_name,
            prompt=dialogue_prompt,
            max_tokens=self.MAX_NEW_TOKENS,
            temperature=0.6
        )

        response = response.choices[0].text.split("</think>")[-1]

        return response.strip(), log_string

    def _create_message_for_functions(self, tool_functions, action_functions, dialogue, user_info):
        prompt = read_file(FUNCTION_CALLS_PROMPT_PATH)

        # Prepare function information by concatenating all function names and docstrings. 
        function_information = []
        for tool_name in tool_functions['function_registry'].keys():
            tool_ = tool_functions['function_registry'][tool_name]
            tool_prompt = (
                "# Function Name: {}\n"
                "# Function Docstring: {}\n"
            ).format(tool_['name'], tool_['description'])
            function_information.append(tool_prompt)
        for action_name in action_functions['function_registry'].keys():
            action_ = action_functions['function_registry'][action_name]
            action_prompt = (
                "# Function Name: {}\n"
                "# Function Docstring: {}\n"
            ).format(action_['name'], action_['description'])
            function_information.append(action_prompt)
        function_information_agg = '\n'.join(function_information)
        
        input_text = dialogue[0]["text"] # sorted from new to old

        prompt = prompt.replace("{functions}", function_information_agg) \
                        .replace("{context}", user_info) \
                        .replace("{history}", "\n".join([h["text"] for h in dialogue]))
        
        return prompt
    
    def _create_dialogue_message(self, user_info, history, function_results):
        
        prompt = read_file(REPLY_PROMPT_PATH)

        funciton_outputs = ""
        for result in function_results:
            result = function_results[result]
            funciton_outputs = funciton_outputs + f"Function {result['name']} Output:\n{result['output']}\n"
        
        prompt = prompt.replace("{external_kg}", funciton_outputs) \
                        .replace("{user_info}", user_info) \
                        .replace("{history}", "\n".join([h["text"] for h in history]))

        return prompt