from typing import Annotated, Any
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    intent: str | None
    research_output: dict[str, Any] | None
    # Memory hooks — vacíos en Phase 1, se activan en Phase 2
    user_context: dict[str, Any] | None
    knowledge_context: dict[str, Any] | None
