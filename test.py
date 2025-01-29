import requests
import json
import streamlit as st
import re
import os
from dotenv import load_dotenv
load_dotenv()
def extract_values(response_text):
    # Extract numerical values using regex
    try:
        data = json.loads(response_text)
        text = data.get("text", "")

        # Regex to find the required values
        market_trend_factor = re.search(r'"market_trend_factor"\s*:\s*([\d.]+)', text)
        uniqueness_score = re.search(r'"uniqueness_score"\s*:\s*([\d.]+)', text)
        preciousness_score = re.search(r'"preciousness_score"\s*:\s*([\d.]+)', text)

        # Extract and convert to float if found, else None
        return {
            "market_trend_factor": float(market_trend_factor.group(1)) if market_trend_factor else None,
            "uniqueness_score": float(uniqueness_score.group(1)) if uniqueness_score else None,
            "preciousness_score": float(preciousness_score.group(1)) if preciousness_score else None
        }

    except json.JSONDecodeError:
        return "Invalid JSON"


def run_flow():
    API_KEY=os.environ.get("API_KEY")
    URL="https://payload.vextapp.com/hook/JRTTX71X3M/catch/hello_ji" #last endpoint should be a unique identifier, its used for message history
    headers={
        "Content-type": "application/json",
        "ApiKey": f"Api-key {API_KEY}"
    }
    data={"payload": "Iphone 12 that has been used roughly for 3 years. It has some scratches on its screen.It has a storage of 128 gb", "brand": "Apple", "category": "Mobiles and Electronics", "product_name": "Iphone 12", "original_value": "$500"}

    response = requests.post(URL, headers=headers, json=data)
    extract_values(response.text)
    print(response.text )
    print()
    print(extract_values(response.text))
    # return extract_values(response.text)
    return response.text


def main():
    st.title("Chat Interface")

    # message = st.text_area("Message", placeholder="The Prompt is hard")

    if st.button("Run FLow"):
        # if not message.strip():
            # st.error("Please enter a message")
            # return

        try:
            with st.spinner("Running Flow..."):
                response = run_flow()
            # response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.text(response)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
