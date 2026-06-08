import os
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, ToolMessage
from langsmith import traceable

from src.state import AgentState
from src.tools import all_tools, search_macro_news

from src.prompts import load_prompt


class ResearchAgent:
    def __init__(self):
        llm = init_chat_model(
            model=os.getenv("MODEL"),
            model_provider="openai",
            api_key=os.getenv("OPENAI_GH_TOKEN"),
            base_url="https://models.github.ai/inference",
            temperature=0,
        )
        structured_tools = [t for t in all_tools if t.name != "search_macro_news"]
        self.llm_with_tools = llm.bind_tools(structured_tools)

        self.llm_with_fallback = llm.bind_tools([search_macro_news])

        self.tools_by_name = {t.name: t for t in all_tools}
        self.system_prompt = load_prompt("research-agent-base")

    @traceable(name="research_agent_node")
    def research_agent_node(self, state: AgentState) -> dict:
        messages = list(state.get("messages", []))

        response, called_tools = self._run_tool_loop(messages, self.llm_with_tools)

        if not called_tools:
            called_tools.append("search_macro_news")
            response, _ = self._run_tool_loop(messages, self.llm_with_fallback)

        return {"research_output": {"summary": response.content, "called_tools": called_tools}}

    def _run_tool_loop(self, messages: list, llm) -> tuple:
        messages = [SystemMessage(content=self.system_prompt)] + list(messages)
        called_tools = []

        while True:
            response = llm.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            for tool_call in response.tool_calls:
                tool = self.tools_by_name[tool_call["name"]]
                try:
                    result = tool.invoke(tool_call["args"])
                    called_tools.append(tool_call["name"])
                    messages.append(
                        ToolMessage(
                            content=str(result),
                            tool_call_id=tool_call["id"],
                        )
                    )

                except Exception:
                    # compulsory fallback if any tool fails, to avoid leaving the agent hanging
                    # without a response
                    messages.append(
                        ToolMessage(
                            content="No data available for these parameters.",
                            tool_call_id=tool_call["id"],
                        )
                    )

        return response, called_tools
