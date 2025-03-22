import requests
import os
from datetime import datetime

class AssetValuationUsingAPIs:
    def __init__(self):
        # Enhanced category configuration
        self.category_db = {
            'electronics': {
                'depreciation_rate': 0.25, 
                'salvage': 0.15, 
                'method': 'declining',
                'ebay_category': '9355'  # Electronics category ID
            },
            'vehicles': {
                'depreciation_rate': 0.18,
                'salvage': 0.20,
                'method': 'straight-line',
                'ebay_category': '6001'  # Vehicles category ID
            },
            'real_estate': {
                'appreciation_rate': 0.05, 
                'method': 'appreciation'
            },
            'collectibles': {
                'appreciation_rate': 0.07,
                'method': 'appreciation',
                'ebay_category': '1'  # Collectibles category ID
            },
            'furniture': {
                'depreciation_rate': 0.15,
                'salvage': 0.10,
                'method': 'straight-line',
                'ebay_category': '11700'  # Home & Garden category ID
            }
        }
        
        # API configuration
        self.ebay_api_endpoint = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self.oauth_endpoint = "https://api.ebay.com/identity/v1/oauth2/token"
        self.inflation_api = "https://www.statbureau.org/get-data-json"
        
        # Security configuration
        self.client_id = os.getenv('EBAY_CLIENT_ID')
        self.client_secret = os.getenv('EBAY_CLIENT_SECRET')
        self.oauth_token = None
        self.marketplace_id = 'EBAY-US'  # Configurable marketplace

    def categorize_product(self, product_name):
        """Enhanced product categorization with fallback logic"""
        try:
            category_map = {
                'electronics': ['phone', 'laptop', 'tablet', 'camera'],
                'vehicles': ['car', 'bike', 'motorcycle', 'scooter'],
                'real_estate': ['house', 'apartment', 'land', 'property'],
                'collectibles': ['art', 'antique', 'coin', 'stamp'],
                'furniture': ['chair', 'table', 'sofa', 'cabinet']
            }
            
            product_lower = product_name.lower()
            for category, keywords in category_map.items():
                if any(kw in product_lower for kw in keywords):
                    return category
            return 'general'
        except Exception as e:
            print(f"Categorization error: {str(e)}")
            return 'general'

    def _get_oauth_token(self):
        """Secure OAuth2 token retrieval with error handling"""
        try:
            auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = {
                'grant_type': 'client_credentials',
                'scope': 'https://api.ebay.com/oauth/api_scope'
            }
            
            response = requests.post(
                self.oauth_endpoint,
                auth=auth,
                headers=headers,
                data=data
            )
            response.raise_for_status()
            self.oauth_token = response.json()['access_token']
            return True
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False

    def get_market_price(self, product_name, category):
        """Enhanced eBay price fetching with category-specific search"""
        try:
            if not self.oauth_token and not self._get_oauth_token():
                return None

            headers = {
                'Authorization': f'Bearer {self.oauth_token}',
                'X-EBAY-C-MARKETPLACE-ID': self.marketplace_id
            }

            params = {
                'q': product_name,
                'filter': 'conditions:USED',
                'limit': '10',  # Get more samples for better accuracy
                'sort': 'price',
                'category_ids': self.category_db.get(category, {}).get('ebay_category', '')
            }

            response = requests.get(
                self.ebay_api_endpoint,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            items = response.json().get('itemSummaries', [])
            if not items:
                return None

            # Advanced price analysis
            prices = []
            for item in items:
                if item.get('price') and item.get('condition') == 'USED':
                    try:
                        price = float(item['price']['value'])
                        if price > 0:  # Filter invalid prices
                            prices.append(price)
                    except (ValueError, KeyError):
                        continue
            
            if len(prices) < 3:  # Require minimum 3 valid prices
                return None

            # Calculate trimmed mean (ignore extremes)
            prices.sort()
            trimmed = prices[1:-1]
            return round(sum(trimmed) / len(trimmed), 2)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                self.oauth_token = None
                return self.get_market_price(product_name, category)
            print(f"API Error: {e.response.text}")
            return None
        except Exception as e:
            print(f"Price check failed: {str(e)}")
            return None

    def calculate_valuation(self, product_name, years_used):
        """Hybrid valuation system with fallback logic"""
        try:
            category = self.categorize_product(product_name)
            market_price = self.get_market_price(product_name, category)
            
            if market_price:
                return self._apply_condition_adjustment(market_price, years_used, category)
            
            return self._calculate_theoretical_value(category, years_used)
            
        except Exception as e:
            print(f"Valuation error: {str(e)}")
            return None

    def _apply_condition_adjustment(self, base_price, years_used, category):
        """Apply condition-based adjustment to market price"""
        adjustment_factors = {
            'electronics': 0.85 ** years_used,
            'vehicles': 0.90 ** years_used,
            'furniture': 0.95 ** years_used,
            'general': 0.90 ** years_used
        }
        factor = adjustment_factors.get(category, 0.9 ** years_used)
        return max(base_price * factor, base_price * 0.2)  # Never drop below 20% of market

    def _calculate_theoretical_value(self, category, years_used):
        """Calculate value using depreciation/appreciation models"""
        category_data = self.category_db.get(category, {})
        initial_price = self._get_validated_input("Enter original purchase price: ", float)
        
        if category_data.get('method') == 'appreciation':
            rate = category_data.get('appreciation_rate', 0.05)
            return initial_price * (1 + rate) ** years_used
        else:
            salvage = initial_price * category_data.get('salvage', 0.1)
            rate = category_data.get('depreciation_rate', 0.2)
            
            if category_data.get('method') == 'straight-line':
                useful_life = 1 / rate if rate else float('inf')
                depreciation = (initial_price - salvage) / useful_life * years_used
                return max(initial_price - depreciation, salvage)
            else:  # Declining balance
                current_value = initial_price * (1 - rate) ** years_used
                return max(current_value, salvage)


    def get_inflation_adjusted(self, value, years_used):
        """Accurate inflation adjustment using StatBureau API"""
        try:
            current_year = datetime.now().year
            params = {
                'country': 'united-states',
                'start': current_year - years_used,
                'end': current_year,
                'format': 'true',
                'interval': 'year'
            }
            
            response = requests.get(
                self.inflation_api,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            
            inflation_data = response.json()
            
            if not isinstance(inflation_data, list) or len(inflation_data) == 0:
                print("No valid inflation data available")
                return value
                
            cumulative_factor = 1.0
            for rate in inflation_data:
                try:
                    # Convert percentage to decimal and calculate cumulative effect
                    cumulative_factor *= (1 + float(rate)/100
                except (ValueError, TypeError):
                    continue  # Skip invalid entries
                    
            return round(value * cumulative_factor, 2)
            
        except requests.exceptions.HTTPError as e:
            print(f"Inflation API Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Inflation API connection failed: {str(e)}")
        except Exception as e:
            print(f"Inflation calculation error: {str(e)}")
            
        return value  # Fallback to original value


    def _get_validated_input(self, prompt, data_type):
        """Universal input validation with retry logic"""
        while True:
            try:
                value = data_type(input(prompt))
                if data_type == int and value < 0:
                    raise ValueError("Negative values not allowed")
                return value
            except ValueError:
                print(f"Invalid input. Please enter a valid {data_type.__name__}")

if __name__ == "__main__":
    valuator = AssetValuationUsingAPIs()
    
    product_name = input("Product name: ").strip()
    years_used = valuator._get_validated_input("Years used: ", int)
    
    base_value = valuator.calculate_valuation(product_name, years_used)
    if base_value:
        final_value = valuator.get_inflation_adjusted(base_value, years_used)
        print(f"\nValuation for {product_name} ({years_used} years):")
        print(f"Current estimated value: ${base_value:,.2f}")
        print(f"Inflation-adjusted value: ${final_value:,.2f}")
    else:
        print("Could not determine valuation for this item")