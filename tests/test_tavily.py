from src.tools.tavily import search_macro_news


def test_returns_results():
    result = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    assert "results" in result
    assert len(result["results"]) > 0


def test_result_structure():
    result = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    first = result["results"][0]
    assert "url" in first
    assert "title" in first
    assert "content" in first
    assert "score" in first


def test_result_count():
    result = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    assert len(result["results"]) <= 5


def test_results_are_relevant():
    result = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    contents = " ".join(r["content"] for r in result["results"]).lower()
    assert any(term in contents for term in ["ecb", "interest rate", "european central bank"])


def test_results_have_scores():
    result = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    assert all(isinstance(r["score"], float) for r in result["results"])
    assert all(r["score"] > 0 for r in result["results"])


def test_different_query_returns_different_results():
    result_ecb = search_macro_news.invoke({"query": "ECB interest rates 2025"})
    result_housing = search_macro_news.invoke({"query": "Spain housing market 2025"})
    urls_ecb = {r["url"] for r in result_ecb["results"]}
    urls_housing = {r["url"] for r in result_housing["results"]}
    assert urls_ecb != urls_housing
