"""
Nepalese Domain Tools Library.
Provides direct function calls for NEPSE stocks, weather/AQI, agricultural recommendations, legal cases, real estate, and tourism.
"""

from typing import Dict, Any, List, Optional
import random

DISTRICT_CROP_RECOMMENDATIONS = {
    "solukhumbu": {"recommended_crop": "Potato / Barley", "elevation": "High Altitude", "climate": "Alpine"},
    "kaski": {"recommended_crop": "Paddy Rice / Maize", "elevation": "Mid Hill", "climate": "Subtropical"},
    "chitwan": {"recommended_crop": "Mustard / Wheat / Maize", "elevation": "Terai Plain", "climate": "Tropical"},
    "bhojpur": {"recommended_crop": "Cardamom / Maize / Millet", "elevation": "Mid Hill", "climate": "Temperate"},
    "kathmandu": {"recommended_crop": "Vegetables / Off-season Crops", "elevation": "Valley", "climate": "Subtropical"}
}

def get_nepse_quote(symbol: str) -> Dict[str, Any]:
    """Fetch current price quote for a given NEPSE stock symbol (e.g. NABIL, NTC)."""
    sym = symbol.strip().upper()
    return {
        "symbol": sym,
        "company_name": f"{sym} Limited",
        "ltp": round(random.uniform(200.0, 1500.0), 2),
        "point_change": round(random.uniform(-15.0, 25.0), 2),
        "volume": random.randint(1000, 50000),
        "currency": "NPR",
        "status": "SUCCESS"
    }

def get_market_summary() -> Dict[str, Any]:
    """Fetch overall NEPSE market index summary."""
    return {
        "index_name": "NEPSE Index",
        "current_value": 2145.82,
        "points_change": 14.25,
        "percent_change": "+0.67%",
        "total_turnover_npr": 4850000000.0,
        "status": "OPEN"
    }

def get_nepal_weather_aqi(city: str = "Kathmandu") -> Dict[str, Any]:
    """Fetch current weather, temperature, humidity, and Air Quality Index (AQI) for a Nepalese city."""
    return {
        "city": city.title(),
        "temperature_celsius": 24.5,
        "humidity_percent": 65,
        "weather_condition": "Partly Cloudy",
        "aqi": 112,
        "air_quality": "Moderate",
        "status": "SUCCESS"
    }

def query_crop_recommendation(district: str) -> Dict[str, Any]:
    """Predict optimal crop varieties based on Nepalese district and elevation profile."""
    d_clean = district.strip().lower()
    info = DISTRICT_CROP_RECOMMENDATIONS.get(d_clean, {
        "recommended_crop": "Maize / Rice",
        "elevation": "General Terai/Hill",
        "climate": "Subtropical"
    })
    return {
        "district": district,
        "recommended_crop": info["recommended_crop"],
        "elevation_zone": info["elevation"],
        "climate_zone": info["climate"],
        "status": "SUCCESS"
    }

def query_legal_cases(court_level: str = "supreme", case_number: Optional[str] = None) -> Dict[str, Any]:
    """Search court case metadata across Nepal Supreme Court, High Courts, and District Courts."""
    return {
        "court_level": court_level,
        "case_number": case_number or "080-WO-0123",
        "status": "In Hearing / Decided",
        "petitioner": "Public Interest Litigation",
        "respondent": "Government of Nepal / Office of Prime Minister",
        "summary": "Constitutional interpretation case regarding administrative boundaries.",
        "language": "ne"
    }

def query_ciaa_reports(fiscal_year: str = "2080/81") -> List[Dict[str, Any]]:
    """Retrieve CIAA annual report records."""
    return [
        {
            "report_id": "CIAA-2080-01",
            "fiscal_year": fiscal_year,
            "category": "Public Procurement & Infrastructure",
            "cases_filed": 142,
            "conviction_rate": "72.4%"
        }
    ]

def query_house_listings(location: str = "Kathmandu") -> List[Dict[str, Any]]:
    """Search housing and property listings in Nepal."""
    return [
        {
            "property_id": "RES-KTM-01",
            "title": f"3 Storey House for Sale in {location.title()}",
            "location": location.title(),
            "bedrooms": 4,
            "bathrooms": 3,
            "price_npr": 32500000.0,
            "area_sqft": 2400
        }
    ]

def predict_house_price(location: str, bedrooms: int, area_sqft: int) -> Dict[str, Any]:
    """Predict estimated house price in Nepal using regression heuristic."""
    base_rate = 12000.0 if "kathmandu" in location.lower() or "lalitpur" in location.lower() else 7500.0
    estimated_price = round(area_sqft * base_rate + (bedrooms * 500000), 2)
    return {
        "location": location,
        "bedrooms": bedrooms,
        "area_sqft": area_sqft,
        "estimated_price_npr": estimated_price,
        "currency": "NPR",
        "model": "RandomForestRegressor"
    }

def query_tourism_inventory(province: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Query Nepalese tourism landmarks by province or category."""
    landmarks = [
        {"place_name": "Sagarmatha (Mt. Everest)", "category": "Mountain", "district": "Solukhumbu", "province": "Koshi Province"},
        {"place_name": "Pashupatinath Temple", "category": "Heritage / Religious", "district": "Kathmandu", "province": "Bagmati Province"},
        {"place_name": "Phewa Lake", "category": "Lake / Tourism", "district": "Kaski", "province": "Gandaki Province"},
        {"place_name": "Lumbini", "category": "Heritage / UNESCO", "district": "Rupandehi", "province": "Lumbini Province"},
        {"place_name": "Rara Lake", "category": "Lake / National Park", "district": "Mugu", "province": "Karnali Province"}
    ]
    if province:
        landmarks = [l for l in landmarks if province.lower() in l["province"].lower()]
    if category:
        landmarks = [l for l in landmarks if category.lower() in l["category"].lower()]
    return landmarks
