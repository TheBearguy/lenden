# class AssetValuation:
#     @staticmethod
#     def straight_line_depreciation(initial_cost, salvage_value, useful_life, years):
#         """
#         Calculates current value using the Straight-Line Method.
#         """
#         if useful_life == 0:
#             return salvage_value
#         annual_depreciation = (initial_cost - salvage_value) / useful_life
#         total_depreciation = annual_depreciation * years
#         current_value = initial_cost - total_depreciation
#         return max(round(current_value, 2), salvage_value)  # Never drops below salvage value

#     @staticmethod
#     def declining_balance_depreciation(initial_cost, salvage_value, depreciation_rate, years):
#         """
#         Calculates current value using the Declining Balance Method.
#         """
#         current_value = initial_cost * (1 - depreciation_rate) ** years
#         return max(round(current_value, 2), salvage_value)  # Never drops below salvage value

#     @staticmethod
#     def appreciation(initial_cost, appreciation_rate, years):
#         """
#         Calculates appreciated value for assets like real estate or collectibles.
#         """
#         return round(initial_cost * (1 + appreciation_rate) ** years, 2)

#     @staticmethod
#     def inflation_adjustment(value, inflation_rate, years):
#         """
#         Adjusts any calculated value for inflation.
#         """
#         return round(value * (1 + inflation_rate) ** years, 2)

#     @staticmethod
#     def calculate_salvage_value(original_cost, salvage_percentage):
#         """
#         Calculate salvage value as a percentage of the original cost.
#         """
#         return round(original_cost * salvage_percentage, 2)

#     @staticmethod
#     def calculate_useful_life(original_cost, salvage_value, annual_depreciation):
#         """
#         Calculate useful life based on original cost, salvage value, and annual depreciation.
#         """
#         if annual_depreciation == 0:
#             return float('inf')  # Infinite useful life if no depreciation
#         return round((original_cost - salvage_value) / annual_depreciation, 2)

#     @staticmethod
#     def calculate_straight_line_rate(useful_life):
#         """
#         Calculate the straight-line depreciation rate.
#         """
#         if useful_life == 0:
#             return 0
#         return round(100 / useful_life, 2)

# if __name__ == "__main__":
#     # Input parameters (customize these)
#     #!  THese values are to be fetched fromt he langflow agent, (which is risky coz it wornt be accurate)
#     initial_cost = 1000000       # Initial purchase price
#     salvage_percentage = 0.10     # Salvage value percentage (10%)
#     annual_depreciation = 30000   # Annual depreciation for useful life calculation
#     years = 10                    # Age of the asset

#     # Calculate parameters from workflow
#     salvage_value = AssetValuation.calculate_salvage_value(initial_cost, salvage_percentage)
#     useful_life = AssetValuation.calculate_useful_life(initial_cost, salvage_value, annual_depreciation)
    
#     # Calculate depreciation rates
#     straight_line_rate = AssetValuation.calculate_straight_line_rate(useful_life)
#     depreciation_rate = straight_line_rate / 100  # Convert to decimal for calculations
    
#     # Appreciation and inflation rates (assumed values)
#     appreciation_rate = 0.054   # 5.4% annual appreciation
#     inflation_rate = 0.06       # 6% annual inflation

#     # Calculate values using the methods defined in AssetValuation class
#     sl_value = AssetValuation.straight_line_depreciation(initial_cost, salvage_value, useful_life, years)
#     db_value = AssetValuation.declining_balance_depreciation(initial_cost, salvage_value, depreciation_rate, years)
#     appr_value = AssetValuation.appreciation(initial_cost, appreciation_rate, years)
    
#     # Adjust for inflation
#     sl_inflation_adjusted = AssetValuation.inflation_adjustment(sl_value, inflation_rate, years)
#     db_inflation_adjusted = AssetValuation.inflation_adjustment(db_value, inflation_rate, years)
#     appr_inflation_adjusted = AssetValuation.inflation_adjustment(appr_value, inflation_rate, years)

#     # Print results
#     print(f"Initial Value: ₹{initial_cost:,.2f}")
#     print(f"Age: {years} years\n")
    
#     print("Depreciation Methods:")
#     print(f"Straight-Line Method: ₹{sl_value:,.2f}")
#     print(f"Adjusted for Inflation: ₹{sl_inflation_adjusted:,.2f}\n")
    
#     print(f"Declining Balance Method: ₹{db_value:,.2f}")
#     print(f"Adjusted for Inflation: ₹{db_inflation_adjusted:,.2f}\n")
    
#     print("Appreciation Method:")
#     print(f"Appreciated Value: ₹{appr_value:,.2f}")
#     print(f"Adjusted for Inflation: ₹{appr_inflation_adjusted:,.2f}")

#!-----------------------------------------------------------------------------------------------

class AssetValuation:
    @staticmethod
    def straight_line_depreciation(initial_cost, salvage_value, useful_life, years):
        """
        Calculates current value using the Straight-Line Method.
        """
        if useful_life == 0:
            return salvage_value
        annual_depreciation = (initial_cost - salvage_value) / useful_life
        total_depreciation = annual_depreciation * years
        current_value = initial_cost - total_depreciation
        return max(round(current_value, 2), salvage_value)

    @staticmethod
    def declining_balance_depreciation(initial_cost, salvage_value, useful_life, years, factor=2):
        """
        Calculates current value using the Declining Balance Method with a depreciation factor.
        Default factor is 2 for double declining balance.
        """
        if useful_life == 0:
            return initial_cost
        depreciation_rate = factor / useful_life
        current_value = initial_cost
        for _ in range(years):
            current_value = max(current_value - current_value * depreciation_rate, salvage_value)
        return round(current_value, 2)

    @staticmethod
    def appreciation(initial_cost, appreciation_rate, years):
        """
        Calculates appreciated value for assets like real estate or collectibles.
        """
        return round(initial_cost * (1 + appreciation_rate) ** years, 2)

    @staticmethod
    def inflation_adjustment(value, inflation_rate, years):
        """
        Adjusts any calculated value for inflation.
        """
        return round(value * (1 + inflation_rate) ** years, 2)

    @staticmethod
    def calculate_salvage_value(original_cost, salvage_percentage):
        """
        Calculate salvage value as a percentage of the original cost.
        """
        return round(original_cost * salvage_percentage, 2)

    @staticmethod
    def calculate_useful_life(original_cost, salvage_value, annual_depreciation):
        """
        Calculate useful life based on original cost, salvage value, and annual depreciation.
        """
        if annual_depreciation == 0:
            return float('inf')  # Infinite useful life if no depreciation
        return round((original_cost - salvage_value) / annual_depreciation, 2)

    @staticmethod
    def calculate_straight_line_rate(useful_life):
        """
        Calculate the straight-line depreciation rate.
        """
        if useful_life == 0:
            return 0
        return round(100 / useful_life, 2)

def determine_valuation_method(product_name):
    """
    Determines if the product typically appreciates or depreciates based on keywords.
    """
    appreciating_keywords = ['art', 'real estate', 'antique', 'collectible', 'jewelry']
    depreciating_keywords = ['car', 'laptop', 'phone', 'equipment', 'furniture']
    
    product_lower = product_name.lower()
    for keyword in appreciating_keywords:
        if keyword in product_lower:
            return 'appreciate'
    for keyword in depreciating_keywords:
        if keyword in product_lower:
            return 'depreciate'
    return None  # Unknown type

if __name__ == "__main__":
    # User inputs
    product_name = input("Enter product name: ")
    years = int(input("Enter years used: "))
    
    valuation_method = determine_valuation_method(product_name)
    
    if valuation_method is None:
        valuation_method = input("Could not determine valuation method. Enter 'appreciate' or 'depreciate': ").lower()
    
    if valuation_method == 'depreciate':
        initial_cost = float(input("Enter initial cost of the product: "))
        salvage_percentage = float(input("Enter salvage value percentage (e.g., 0.1 for 10%): "))
        depreciation_method = input("Choose depreciation method (straight-line/declining): ").lower()
        
        salvage_value = AssetValuation.calculate_salvage_value(initial_cost, salvage_percentage)
        
        if depreciation_method == 'straight-line':
            annual_depreciation = float(input("Enter annual depreciation amount: "))
            useful_life = AssetValuation.calculate_useful_life(initial_cost, salvage_value, annual_depreciation)
            current_value = AssetValuation.straight_line_depreciation(
                initial_cost, salvage_value, useful_life, years
            )
        elif depreciation_method == 'declining':
            useful_life = float(input("Enter useful life of the product (years): "))
            factor = float(input("Enter declining balance factor (e.g., 2 for double declining): "))
            current_value = AssetValuation.declining_balance_depreciation(
                initial_cost, salvage_value, useful_life, years, factor
            )
        else:
            print("Invalid depreciation method selected.")
            exit()
        
    elif valuation_method == 'appreciate':
        initial_cost = float(input("Enter initial cost of the product: "))
        appreciation_rate = float(input("Enter annual appreciation rate (e.g., 0.05 for 5%): "))
        current_value = AssetValuation.appreciation(initial_cost, appreciation_rate, years)
    
    else:
        print("Invalid valuation method.")
        exit()
    
    # Inflation adjustment
    adjust_inflation = input("Adjust for inflation? (yes/no): ").lower()
    if adjust_inflation == 'yes':
        inflation_rate = float(input("Enter annual inflation rate (e.g., 0.03 for 3%): "))
        current_value = AssetValuation.inflation_adjustment(current_value, inflation_rate, years)
    
    print(f"\nCurrent Valuation for {product_name} after {years} years: ₹{current_value:,.2f}")