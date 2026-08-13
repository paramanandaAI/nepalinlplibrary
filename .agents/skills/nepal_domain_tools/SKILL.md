---
name: nepal_domain_tools
description: AI agent tool-calling skill for querying Nepalese domain APIs and databases including NEPSE stock market quotes, weather/AQI, tourism landmarks, agricultural crop recommendations, legal case lookups, and real estate valuation.
---

# Nepalese Domain Tools Skill

This skill enables AI agents to query Nepalese domain APIs, lookup structured domain data, and execute Python tool calls across finance, meteorology, tourism, agriculture, jurisprudence, and real estate.

---

## 💻 Python Library Usage

All functions are implemented in [`linguistic_adaptation/.agents/skills/nepal_domain_tools/scripts/tools.py`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/scripts/tools.py) and exposed via [`linguistic_adaptation/.agents/skills/nepal_domain_tools/scripts/__init__.py`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/scripts/__init__.py):

```python
from .agents.skills.nepal_domain_tools.scripts import (
    get_nepse_quote,
    get_market_summary,
    get_nepal_weather_aqi,
    query_crop_recommendation,
    query_legal_cases,
    query_ciaa_reports,
    query_house_listings,
    predict_house_price,
    query_tourism_inventory,
)
```

---

## 🛠️ Tool Specifications & Schema References

1. **NEPSE Stock Market Tool**
   - **Functions:** `get_nepse_quote(symbol: str) -> Dict[str, Any]`, `get_market_summary() -> Dict[str, Any]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)

2. **Weather & Air Quality Index Tool**
   - **Function:** `get_nepal_weather_aqi(city: str) -> Dict[str, Any]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)

3. **Agriculture & Crop Recommendation Tool**
   - **Function:** `query_crop_recommendation(district: str) -> Dict[str, Any]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)

4. **Judiciary & Legal Case Lookup Tool**
   - **Functions:** `query_legal_cases(court_level: str, case_number: Optional[str]) -> Dict[str, Any]`, `query_ciaa_reports(fiscal_year: str) -> List[Dict[str, Any]]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)

5. **Real Estate & Valuation Tool**
   - **Functions:** `predict_house_price(location: str, bedrooms: int, area_sqft: int) -> Dict[str, Any]`, `query_house_listings(location: str) -> List[Dict[str, Any]]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)

6. **Tourism & Landmark Inventory Tool**
   - **Function:** `query_tourism_inventory(province: Optional[str], category: Optional[str]) -> List[Dict[str, Any]]`
   - **Schema:** [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json)
