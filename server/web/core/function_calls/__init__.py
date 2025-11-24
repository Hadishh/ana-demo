

from . import weather_api as weather_api
from . import knowledge_graph_search as knowledge_graph_api
from .executor import Executor

tool_map = {
    "function_registry": {**knowledge_graph_api.registry, **weather_api.registry}
}


functions_references = dict()
functions_references.update(weather_api.func_references)
functions_references.update(knowledge_graph_api.func_references)