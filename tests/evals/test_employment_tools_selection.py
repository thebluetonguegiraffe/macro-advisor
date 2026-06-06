# tests/evals/test_employment_tool_selection.py
import pytest
from langchain_core.messages import HumanMessage
from agents.supervisor_agent import SupervisorAgent


def invoke(query: str) -> dict:
    agent = SupervisorAgent()
    return agent.graph.invoke({"messages": [HumanMessage(content=query)]})


@pytest.fixture(scope="module")
def result_spain():
    return invoke("¿Cómo está el mercado laboral en España?")


@pytest.fixture(scope="module")
def result_germany():
    return invoke("Wie ist die Lage auf dem Arbeitsmarkt in Deutschland?")


def test_ine_employment_tool_called(result_spain):
    assert "get_ine_employment" in result_spain["called_tools"]


def test_ine_employment_no_news_fallback(result_spain):
    assert "search_macro_news" not in result_spain["called_tools"]


def test_eurostat_employment_tool_called(result_germany):
    assert "get_eurostat_employment" in result_germany["called_tools"]


def test_eurostat_employment_no_news_fallback(result_germany):
    assert "search_macro_news" not in result_germany["called_tools"]