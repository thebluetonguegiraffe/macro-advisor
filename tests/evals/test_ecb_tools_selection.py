import pytest
from langchain_core.messages import HumanMessage
from agents.supervisor_agent import SupervisorAgent


def invoke(query: str) -> dict:
    agent = SupervisorAgent()
    return agent.graph.invoke({"messages": [HumanMessage(content=query)]})


@pytest.fixture(scope="module")
def result_gdp_spain():
    return invoke("¿Cómo va el PIB español?")


@pytest.fixture(scope="module")
def result_gdp_germany():
    return invoke("¿Is German economy growing this year?")


@pytest.fixture(scope="module")
def result_cpi_spain():
    return invoke("¿Está subiendo el coste de la vida en España?")


@pytest.fixture(scope="module")
def result_cpi_germany():
    return invoke("How much has inflation increased in Germany this year?")


@pytest.fixture(scope="module")
def result_rates_mortgage():
    return invoke("¿Es un buen momento para pedir una hipoteca?")


@pytest.fixture(scope="module")
def result_rates_outlook():
    return invoke("¿Cuándo van a bajar los tipos de interés?")


# --- GDP ---


def test_gdp_spain_tool_called(result_gdp_spain):
    assert "get_ecb_gdp" in result_gdp_spain["called_tools"]


def test_gdp_spain_no_news_fallback(result_gdp_spain):
    assert "search_macro_news" not in result_gdp_spain["called_tools"]


def test_gdp_germany_tool_called(result_gdp_germany):
    assert "get_ecb_gdp" in result_gdp_germany["called_tools"]


def test_gdp_germany_no_news_fallback(result_gdp_germany):
    assert "search_macro_news" not in result_gdp_germany["called_tools"]


# --- CPI ---


def test_cpi_spain_tool_called(result_cpi_spain):
    assert "get_ecb_cpi" in result_cpi_spain["called_tools"]


def test_cpi_spain_no_news_fallback(result_cpi_spain):
    assert "search_macro_news" not in result_cpi_spain["called_tools"]


def test_cpi_germany_tool_called(result_cpi_germany):
    assert "get_ecb_cpi" in result_cpi_germany["called_tools"]


def test_cpi_germany_no_news_fallback(result_cpi_germany):
    assert "search_macro_news" not in result_cpi_germany["called_tools"]


# --- Rates ---


def test_rates_mortgage_tool_called(result_rates_mortgage):
    assert "get_ecb_rates" in result_rates_mortgage["called_tools"]


def test_rates_mortgage_no_news_fallback(result_rates_mortgage):
    assert "search_macro_news" not in result_rates_mortgage["called_tools"]


def test_rates_outlook_tool_called(result_rates_outlook):
    assert "get_ecb_rates" in result_rates_outlook["called_tools"]
