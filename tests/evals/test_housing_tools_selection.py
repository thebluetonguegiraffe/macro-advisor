import pytest
from langchain_core.messages import HumanMessage
from agents.supervisor_agent import SupervisorAgent


def invoke(query: str) -> dict:
    agent = SupervisorAgent()
    return agent.graph.invoke({"messages": [HumanMessage(content=query)]})


@pytest.fixture(scope="module")
def result_spain():
    return invoke("¿Es un buen momento para comprar una casa en España?")


@pytest.fixture(scope="module")
def result_germany():
    return invoke("Ist es ein guter Zeitpunkt, um ein Haus in Deutschland zu kaufen?")


def test_ine_housing_tool_called(result_spain):
    assert "get_ine_housing" in result_spain["called_tools"]


def test_ine_housing_no_news_fallback(result_spain):
    assert "search_macro_news" not in result_spain["called_tools"]


def test_eurostat_housing_tool_called(result_germany):
    assert "get_eurostat_housing" in result_germany["called_tools"]


def test_eurostat_housing_no_news_fallback(result_germany):
    assert "search_macro_news" not in result_germany["called_tools"]
