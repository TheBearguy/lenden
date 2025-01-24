class ProductValuation:
    def __init__(self, original_value, years_used,  depreciation_rate, uniqueness_score, preciousness_score, market_trend_factor):
        # To Initialize the product valuation model
        # Annual depreciation rate -> probably in the range of (0% to 10%) so numeric value = (0 to 1)
        # Score for uniqueness -> in the range of (0 to 10), numeric value  (o to 1)
        # preciousness score -> Same as above
        # market demand factor ->  if > 1: high demand, <1 low demand
        self.original_value=original_value
        self.years_used=years_used
        self.depreciation_rate=depreciation_rate
        self.uniqueness_score=uniqueness_score
        self.preciousness_score=preciousness_score
        self.market_trend_factor=market_trend_factor

   # Making a separate function for this bcoz i might hve to add some other computation or steps here:
    def calculate_depreciation(self):
        # Formula credit -> gpt
        return self.original_value * (1 - self.depreciation_rate) ** self.years_used


    def calculate_uniqueness_premium(self, base_value):
        return base_value * (1 + self.uniqueness_score * 0.5)  # Premium up to 50% based on uniqueness


    def calculate_preciousness_premium(self, base_value):
        return base_value * ( 1 + self.preciousness_score * 0.3) # Premium up to 30% based on preciousness


    def apply_market_trend(self,  base_value):
        return base_value * self.market_trend_factor

    def get_current_valuation(self):
        # Just returns the final numeric output -> final evaluation of the product:
        depreciated_value = self.calculate_depreciation()
        with_uniqueness = self.calculate_uniqueness_premium(depreciated_value)
        with_preciousness = self.calculate_preciousness_premium(with_uniqueness)
        final_value = self.apply_market_trend(with_preciousness)
        return round(final_value, 2)


if __name__ == "__main__":
    original_value =1000
    years_used = 10
    depreciation_rate = 0.1 # 10% depreciation rate
    uniqueness_score = 0.8 # 80% uniqueness
    preciousness_score = 0.6 # 60% preciousness
    market_trend_factor = 1.2 # 20% higher than demand

    valuation_model = ProductValuation(
        original_value,
        years_used,
        depreciation_rate,
        uniqueness_score,
        preciousness_score,
        market_trend_factor
    )

    current_value = valuation_model.get_current_valuation()
    print(f"The current valuation of the product is: ${current_value}")
