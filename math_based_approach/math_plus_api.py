import requests
from datetime import datetime

class AssetValuationUsingAPIs:
    def __init__(self):
        self.category_db = {
            'electronics': {'depreciation_rate': 0.25, 'salvage': 0.15, 'method': 'declining'},
            'vehicles': {'depreciation_rate': 0.18, 'salvage': 0.20, 'method': 'straight-line'},
            'real_estate': {'appreciation_rate': 0.05, 'method': 'appreciation'},
            'collectibles': {'appreciation_rate': 0.07, 'method': 'appreciation'},
            'furniture': {'depreciation_rate': 0.15, 'salvage': 0.10, 'method': 'straight-line'}
        }
        
    def categorize_product(self, product_name):
        """Improved categorization using keyword matching and external API"""
        try:
            # Try to get category from local database
            product_lower = product_name.lower()
            for category, keywords in {
                'electronics': ['phone', 'laptop', 'tablet', 'camera'],
                'vehicles': ['car', 'bike', 'motorcycle', 'scooter'],
                'real_estate': ['house', 'apartment', 'land', 'property'],
                'collectibles': ['art', 'antique', 'coin', 'stamp'],
                'furniture': ['chair', 'table', 'sofa', 'cabinet']
            }.items():
                if any(kw in product_lower for kw in keywords):
                    return category
            
            # Fallback to ML-based categorization (placeholder)
            return 'general'
        except Exception as e:
            print(f"Error in categorization: {e}")
            return 'general'

#! API Expected
    def get_market_price(self, product_name):
        """Get current market price using eBay BROWSE API (placeholder)"""
        try:
            # Replace with actual API call
            return None  # Simulated failure
        except:
            return None

    def calculate_valuation(self, product_name, years_used):
        """Main valuation calculator"""
        # Get product category
        category = self.categorize_product(product_name)
        
        # Try to get current market price
        market_price = self.get_market_price(product_name)
        if market_price:
            return market_price  # Most accurate if available
        
        # If market price unavailable, use category-based calculation
        category_data = self.category_db.get(category, {})
        
        if category_data.get('method') == 'appreciation':
            return self.calculate_appreciation(category_data, years_used)
        else:
            return self.calculate_depreciation(category_data, years_used)

    def calculate_depreciation(self, category_data, years_used):
        """Handle depreciation calculations"""
        initial_price = self.get_initial_price()
        salvage = initial_price * category_data.get('salvage', 0.1)
        
        if category_data.get('method') == 'straight-line':
            useful_life = 1 / category_data.get('depreciation_rate', 0.2)
            return max(initial_price - (initial_price - salvage)/useful_life * years_used, salvage)
        else:
            rate = category_data.get('depreciation_rate', 0.2)
            current_value = initial_price * (1 - rate) ** years_used
            return max(current_value, salvage)

    def calculate_appreciation(self, category_data, years_used):
        """Handle appreciation calculations"""
        initial_price = self.get_initial_price()
        rate = category_data.get('appreciation_rate', 0.05)
        return initial_price * (1 + rate) ** years_used

    def get_initial_price(self):
        """Get initial price from user"""
        while True:
            try:
                return float(input("Enter the original purchase price: "))
            except ValueError:
                print("Please enter a valid number")

#! API EXPECTED
    def get_inflation_adjusted(self, value, years_used):
        """Get inflation adjustment from historical data"""
        try:
            inflation_data = requests.get("https://api.inflationdata.com").json()
            # Process inflation data based on years_used
            return value * (1 + inflation_data['average_rate']) ** years_used
        except:
            return value  # Return unadjusted if API fails

if __name__ == "__main__":
    valuator = EnhancedAssetValuation()
    
    product_name = input("Enter product name: ")
    years_used = int(input("Enter years used: "))
    
    base_value = valuator.calculate_valuation(product_name, years_used)
    final_value = valuator.get_inflation_adjusted(base_value, years_used)
    
    print(f"\nEstimated current value for {product_name}:")
    print(f"Base valuation: ${base_value:,.2f}")
    print(f"Inflation-adjusted value: ${final_value:,.2f}")