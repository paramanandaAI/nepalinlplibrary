"""
Skill Call Synthesizer Library.
Generates structured single-turn and multi-turn agent tool-calling datasets in Nepali and English
conforming to the project canonical data schema.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional

class SkillCallSynthesizer:
    """Synthesizer for Nepali domain agent tool calling training dialogues."""

    TEMPLATES = {
        "get_nepse_quote": [
            ("आज {symbol} को सेयर मूल्य कति छ?", {"symbol": "{symbol}"}),
            ("Can you check the current stock price for {symbol} on NEPSE?", {"symbol": "{symbol}"}),
            ("{symbol} को बजार भाउ कति पुग्यो?", {"symbol": "{symbol}"})
        ],
        "get_nepal_weather_aqi": [
            ("{city}को आजको मौसम र वायु प्रदूषण (AQI) कस्तो छ?", {"city": "{city}"}),
            ("What is the current weather and air quality index in {city}?", {"city": "{city}"}),
            ("{city}को हावापानी कस्तो छ अहिले?", {"city": "{city}"})
        ],
        "query_crop_recommendation": [
            ("{district} जिल्लामा कुन बाली लगाउन उपयुक्त हुन्छ?", {"district": "{district}"}),
            ("Which crops are recommended for farming in {district} district?", {"district": "{district}"}),
            ("{district}को हावापानीमा कुन खेती राम्रो फस्टाउँछ?", {"district": "{district}"})
        ],
        "predict_house_price": [
            ("{location}मा {bedrooms} कोठा भएको {area_sqft} वर्गफुटको घरको अनुमानित मूल्य कति पर्ला?", 
             {"location": "{location}", "bedrooms": "{bedrooms}", "area_sqft": "{area_sqft}"}),
            ("Estimate the house price in {location} with {bedrooms} bedrooms and {area_sqft} sqft.", 
             {"location": "{location}", "bedrooms": "{bedrooms}", "area_sqft": "{area_sqft}"})
        ]
    }

    SYMBOLS = ["NABIL", "NTC", "NIFRA", "GBIME", "SHIVM", "HDL", "CHCL"]
    CITIES = ["Kathmandu", "Pokhara", "Biratnagar", "Lalitpur", "Chitwan", "Bhaktapur", "Dharan"]
    DISTRICTS = ["Solukhumbu", "Kaski", "Chitwan", "Bhojpur", "Kathmandu", "Mustang", "Jhapa"]

    @classmethod
    def generate_single_turn(cls, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Generate a single-turn tool-calling conversation item."""
        if not tool_name or tool_name not in cls.TEMPLATES:
            tool_name = random.choice(list(cls.TEMPLATES.keys()))

        template_text, param_template = random.choice(cls.TEMPLATES[tool_name])
        
        symbol = random.choice(cls.SYMBOLS)
        city = random.choice(cls.CITIES)
        district = random.choice(cls.DISTRICTS)
        bedrooms = random.randint(2, 6)
        area_sqft = random.randint(1000, 4500)
        location = random.choice(cls.CITIES)

        user_query = template_text.format(
            symbol=symbol, city=city, district=district,
            bedrooms=bedrooms, area_sqft=area_sqft, location=location
        )

        arguments = {}
        for k, v in param_template.items():
            val = v.format(
                symbol=symbol, city=city, district=district,
                bedrooms=bedrooms, area_sqft=area_sqft, location=location
            )
            if k in ["bedrooms", "area_sqft"]:
                arguments[k] = int(val)
            else:
                arguments[k] = val

        return {
            "instruction": user_query,
            "tool_calls": [
                {
                    "name": tool_name,
                    "arguments": arguments
                }
            ],
            "language": "ne" if any('\u0900' <= c <= '\u097f' for c in user_query) else "en"
        }

    @classmethod
    def generate_dataset(cls, num_samples: int = 10) -> List[Dict[str, Any]]:
        """Generate a batch of synthetic tool call conversations."""
        return [cls.generate_single_turn() for _ in range(num_samples)]
