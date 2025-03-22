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
        return max(round(current_value, 2), salvage_value)  # Never drops below salvage value

    @staticmethod
    def declining_balance_depreciation(initial_cost, salvage_value, depreciation_rate, years):
        """
        Calculates current value using the Declining Balance Method.
        """
        current_value = initial_cost * (1 - depreciation_rate) ** years
        return max(round(current_value, 2), salvage_value)  # Never drops below salvage value

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

# Example Usage
if __name__ == "__main__":
    # Input parameters (customize these)
    initial_cost = 1000000  # Initial purchase price
    salvage_value = 10000   # Residual value after useful life
    useful_life = 15        # Total expected lifespan in years
    depreciation_rate = 0.25 # 25% annual depreciation for declining balance
    appreciation_rate = 0.054 # 5.4% annual appreciation
    inflation_rate = 0.06   # 6% annual inflation
    years = 10              # Age of the asset

    # Calculate values
    sl_value = AssetValuation.straight_line_depreciation(initial_cost, salvage_value, useful_life, years)
    db_value = AssetValuation.declining_balance_depreciation(initial_cost, salvage_value, depreciation_rate, years)
    appr_value = AssetValuation.appreciation(initial_cost, appreciation_rate, years)
    
    # Adjust for inflation
    sl_inflation_adjusted = AssetValuation.inflation_adjustment(sl_value, inflation_rate, years)
    db_inflation_adjusted = AssetValuation.inflation_adjustment(db_value, inflation_rate, years)
    appr_inflation_adjusted = AssetValuation.inflation_adjustment(appr_value, inflation_rate, years)

    # Print results
    print(f"Initial Value: ₹{initial_cost:,.2f}")
    print(f"Age: {years} years\n")
    
    print("Depreciation Methods:")
    print(f"Straight-Line Method: ₹{sl_value:,.2f}")
    print(f"Adjusted for Inflation: ₹{sl_inflation_adjusted:,.2f}\n")
    
    print(f"Declining Balance Method: ₹{db_value:,.2f}")
    print(f"Adjusted for Inflation: ₹{db_inflation_adjusted:,.2f}\n")
    
    print("Appreciation Method:")
    print(f"Appreciated Value: ₹{appr_value:,.2f}")
    print(f"Adjusted for Inflation: ₹{appr_inflation_adjusted:,.2f}")
