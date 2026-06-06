from src.tools.ecb.ecb_rates import get_ecb_rates
from src.tools.ecb.ecb_cpi import get_ecb_cpi
from src.tools.ecb.ecb_gdp import get_ecb_gdp
from src.tools.eurostat.eurostat_employment import get_eurostat_employment
from src.tools.eurostat.eurostat_housing import get_eurostat_housing
from src.tools.ine.ine_employment import get_ine_employment
from src.tools.ine.ine_housing import get_ine_housing
from src.tools.tavily import search_macro_news

all_tools = [
    get_eurostat_housing,
    get_eurostat_employment,
    get_ecb_rates,
    get_ecb_cpi,
    get_ecb_gdp,
    get_ine_employment,
    get_ine_housing,
    search_macro_news,
]
