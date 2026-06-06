import os

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, ToolMessage
from src.state import AgentState
from src.tools import all_tools, search_macro_news

RESEARCH_SYSTEM_PROMPT = (
    "You are a macroeconomic research agent. "
    "Answer only with a sentence."
    "NEVER answer from memory — ALWAYS use the available tools "
    "to fetch up-to-date data before responding. "
    "If the question is about an economic indicator (inflation, unemployment, interest rates, "
    "GDP, housing), you MUST call the corresponding tool."
)


class ResearchAgent:
    def __init__(self):
        llm = init_chat_model(
            model="openai/gpt-4o",
            model_provider="openai",
            api_key=os.getenv("GITHUB_TOKEN"),
            base_url="https://models.github.ai/inference",
        )
        structured_tools = [t for t in all_tools if t.name != "search_macro_news"]
        self.llm_with_tools = llm.bind_tools(structured_tools)

        self.llm_with_fallback = llm.bind_tools([search_macro_news])

        self.tools_by_name = {t.name: t for t in all_tools}

    def research_agent_node(self, state: AgentState) -> dict:
        messages = list(state.get("messages", []))

        response, tool_was_called = self._run_tool_loop(messages, self.llm_with_tools)

        if not tool_was_called:
            response, _ = self._run_tool_loop(messages, self.llm_with_fallback)

        return {
            "research_output": {
                "summary": response.content,
            }
        }

    def _run_tool_loop(self, messages: list, llm) -> tuple:
        messages = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + list(messages)
        tool_was_called = False

        while True:
            response = llm.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            tool_was_called = True
            for tool_call in response.tool_calls:
                tool = self.tools_by_name[tool_call["name"]]
                result = tool.invoke(tool_call["args"])
                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

        return response, tool_was_called
