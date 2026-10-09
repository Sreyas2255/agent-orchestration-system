from tools.registry import ToolRegistry
from tools.web_search import web_search


def create_tool_registry() -> ToolRegistry:
    """
    Create and configure the central tool registry.
    """

    registry = ToolRegistry()

    registry.register(
        "web_search",
        web_search
    )

    return registry


registry = create_tool_registry()
