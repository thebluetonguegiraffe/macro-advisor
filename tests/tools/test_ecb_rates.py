from src.tools.ecb.ecb_rates import get_ecb_rates


def test_ecb_rates_returns_three_series():
    result = get_ecb_rates.invoke({"last_n": 1})
    rate_names = {r["PROVIDER_FM_ID"] for r in result}
    assert len(rate_names) == 3
    assert any("Deposit" in n for n in rate_names)
    assert any("Marginal" in n for n in rate_names)
    assert any("Main refinancing" in n for n in rate_names)


def test_ecb_rates_current_values():
    result = get_ecb_rates.invoke({"last_n": 1})
    by_name = {r["PROVIDER_FM_ID"]: r["valor"] for r in result}
    deposit = next(v for k, v in by_name.items() if "Deposit" in k)
    marginal = next(v for k, v in by_name.items() if "Marginal" in k)
    mrr = next(v for k, v in by_name.items() if "Main" in k)
    assert deposit == 2.0
    assert marginal == 2.4
    assert mrr == 2.15


def test_ecb_rates_last_n():
    result = get_ecb_rates.invoke({"last_n": 5})
    periods = {r["period"] for r in result}
    assert len(periods) == 5


def test_ecb_rates_no_none_values():
    result = get_ecb_rates.invoke({"last_n": 12})
    assert all(r["valor"] is not None for r in result)
