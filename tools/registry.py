import time


class ToolRegistry:
    """
    Central registry for all tools available
    to the agent orchestration system.
    """

    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool):
        """Register a tool with a unique name."""

        if not callable(tool):
            raise TypeError(
                f"Tool '{name}' must be callable."
            )

        if name in self.tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self.tools[name] = tool

    def get(self, name: str):
        """Retrieve a registered tool by name."""

        return self.tools.get(name)

    def list_tools(self):
        """Return the names of registered tools."""

        return list(self.tools.keys())

    def execute(self, name: str, *args, **kwargs):
        """Execute a tool and record its execution details."""

        start_time = time.perf_counter()
        tool = self.get(name)

        if tool is None:
            return None, {
                "tool": name,
                "success": False,
                "latency": time.perf_counter() - start_time,
                "input": args,
                "kwargs": kwargs,
                "error": f"Tool '{name}' is not registered."
            }

        try:
            result = tool(*args, **kwargs)

            return result, {
                "tool": name,
                "success": True,
                "latency": time.perf_counter() - start_time,
                "input": args,
                "kwargs": kwargs,
                "output": result
            }

        except Exception as error:
            return None, {
                "tool": name,
                "success": False,
                "latency": time.perf_counter() - start_time,
                "input": args,
                "kwargs": kwargs,
                "error": str(error)
            }
