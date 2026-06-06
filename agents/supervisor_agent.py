from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage
from src.state import AgentState
from agents.research_agent import ResearchAgent

SINGLE_WORD_GREETINGS = ["hola", "hello", "hi", "hey", "buenas"]

MULTI_WORD_GREETINGS = [
    "buenos días", "buenas tardes", "buenas noches",
    "qué tal", "que tal", "cómo estás", "como estas",
    "good morning", "good afternoon", "good evening",
]

GREETING_RESPONSE = (
    "¡Hola! Soy Macro Advisor, tu asistente de contexto macroeconómico. "
    "Pregúntame sobre tipos de interés, inflación, empleo, vivienda "
    "o cualquier decisión financiera personal. ¿En qué puedo ayudarte?"
)


class SupervisorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.graph = self.build_graph()

    def _get_last_user_message(self, state: AgentState) -> str | None:
        for msg in reversed(state.get("messages", [])):
            if isinstance(msg, HumanMessage):
                return msg.content
        return None

    def router_node(self, state: AgentState) -> dict:
        last_message = self._get_last_user_message(state)
        text = last_message.strip().lower() if last_message else ""
        words = text.split()

        is_greeting = (
            len(text) < 50
            and any(kw in words for kw in SINGLE_WORD_GREETINGS)
            or any(kw in text for kw in MULTI_WORD_GREETINGS)
        )

        return {"intent": "greeting" if is_greeting else "research"}

    def greeting_node(self, state: AgentState) -> dict:
        return {"messages": [AIMessage(content=GREETING_RESPONSE)]}

    def route_intent(self, state: AgentState) -> str:
        return state.get("intent", "research")

    def research_node(self, state: AgentState) -> dict:
        result = self.research_agent.research_agent_node(state)
        summary = result["research_output"]["summary"]
        called_tools = result["research_output"]["called_tools"]
        return {
            "messages": [AIMessage(content=summary)],
            "called_tools": called_tools,
        }

    def build_graph(self):
        builder = StateGraph(AgentState)
        builder.add_node("router", self.router_node)
        builder.add_node("greeting", self.greeting_node)
        builder.add_node("research", self.research_node)

        builder.add_edge(START, "router")
        builder.add_conditional_edges("router", self.route_intent, {
            "greeting": "greeting",
            "research": "research",
        })
        builder.add_edge("greeting", END)
        builder.add_edge("research", END)

        return builder.compile()
