import requests
import json
import re

def extract_values(response_text):
    # Extract numerical values using regex
    depreciation_rate = re.search(r'"depreciation_rate":\s*([\d.]+)', response_text)
    uniqueness_score = re.search(r'"uniqueness_score":\s*([\d.]+)', response_text)
    preciousness_score = re.search(r'"preciousness_score":\s*([\d.]+)', response_text)
    market_trend_factor = re.search(r'"market_trend_factor":\s*([\d.]+)', response_text)

    # Extract additional factors as a dictionary
    additional_factors_match = re.search(r'"additional_factors":\s*(\{.*?\})', response_text, re.DOTALL)
    additional_factors = {}

    if additional_factors_match:
        try:
            additional_factors = json.loads(additional_factors_match.group(1))
        except json.JSONDecodeError:
            additional_factors = {}

    # Convert extracted values to float
    return {
        "depreciation_rate": float(depreciation_rate.group(1)) if depreciation_rate else None,
        "uniqueness_score": float(uniqueness_score.group(1)) if uniqueness_score else None,
        "preciousness_score": float(preciousness_score.group(1)) if preciousness_score else None,
        "market_trend_factor": float(market_trend_factor.group(1)) if market_trend_factor else None,
        "additional_factors": additional_factors
    }


API_KEY="TyOClZgK.IIxy9fH02MZuLr1rsperO6FB9a8zzf0H"
URL="https://payload.vextapp.com/hook/JRTTX71X3M/catch/hello_ji" #last endpoint should be a unique identifier, its used for message history
headers={
    "Content-type": "application/json",
    "ApiKey": f"Api-key {API_KEY}"
}
data={"payload": "Iphone 12 that has been used roughly for 3 years. It has some scratches on its screen.It has a storage of 128 gb", "brand": "Apple", "categorY": "Mobiles and Electronics", "product_name": "Iphone 12", "original_value": "$500"}

response = requests.post(URL, headers=headers, json=data)
extract_values(response.text)
print(response.text )
print()
print(extract_values(response.text))
