from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage
from src.state import AgentState
from agents.research_agent import ResearchAgent


class SupervisorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.graph = self.build_graph()

    def supervisor_node(self, state: AgentState) -> dict:
        result = self.research_agent.research_agent_node(state)
        summary = result["research_output"]["summary"]
        return {"messages": [AIMessage(content=summary)]}

    def build_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node("supervisor", self.supervisor_node)
        builder.add_edge(START, "supervisor")
        builder.add_edge("supervisor", END)
        return builder.compile()
