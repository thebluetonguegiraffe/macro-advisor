import pytest
from langchain_core.messages import HumanMessage
from agents.supervisor_agent import SupervisorAgent


def invoke(query: str) -> dict:
    agent = SupervisorAgent()
    return agent.graph.invoke({"messages": [HumanMessage(content=query)]})


@pytest.fixture(scope="module")
def result_economy_spain():
    return invoke("¿Cómo va la economía española?")


def test_economy_spain_calls_gdp(result_economy_spain):
    assert "get_ecb_gdp" in result_economy_spain["called_tools"]


def test_economy_spain_calls_cpi(result_economy_spain):
    assert "get_ecb_cpi" in result_economy_spain["called_tools"]


def test_economy_spain_calls_employment(result_economy_spain):
    assert "get_ine_employment" in result_economy_spain["called_tools"]


def test_economy_spain_calls_housing(result_economy_spain):
    assert "get_ine_housing" in result_economy_spain["called_tools"]


def test_economy_spain_no_news_fallback(result_economy_spain):
    assert "search_macro_news" not in result_economy_spain["called_tools"]
