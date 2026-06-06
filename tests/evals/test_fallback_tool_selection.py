import pytest
from langchain_core.messages import HumanMessage
from agents.supervisor_agent import SupervisorAgent


def invoke(query: str) -> dict:
    agent = SupervisorAgent()
    return agent.graph.invoke({"messages": [HumanMessage(content=query)]})


@pytest.fixture(scope="module")
def result_trade_war():
    return invoke("What is happening with the trade war between the US and Europe?")


def test_trade_war_falls_back_to_news(result_trade_war):
    assert "search_macro_news" in result_trade_war["called_tools"]


# def test_trade_war_no_structured_tools(result_trade_war):
#     structured = {
#         "get_ecb_rates",
#         "get_ecb_cpi",
#         "get_ecb_gdp",
#         "get_ine_housing",
#         "get_ine_employment",
#         "get_eurostat_housing",
#         "get_eurostat_employment",
#     }
#     assert not structured.intersection(set(result_trade_war["called_tools"]))
