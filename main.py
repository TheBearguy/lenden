class ProductValuation:
    def __init__(self, category, original_value, years_used,  depreciation_rate, uniqueness_score, preciousness_score, market_trend_factor, additional_factors=None):
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
        self.category=category
        self.additional_factors=additional_factors

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


    # This method only works when we have a definite API
    @staticmethod
    def fetch_market_trend(category):
        # Fetch market trend factor dynamically for the given category.
        # Fetch either via API or via tool
        # :param category: (str) Product category to fetch trends for.
        # :return: (dict) Market trend data.
        try:
            response = requests.get(f"https://api.example.com/market-trends/{category}")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {"trend_factor": 1.0}  # Default trend factor


    def apply_additional_factors(self, base_value):
        # Adjust the value based on additional (user-defined + LLM + tool) factors.
        # Each factor should be provided as a multiplier in the dictionary.
        adjusted_value = base_value
        for factor, multiplier in self.additional_factors.items():
            adjusted_value *= multiplier
        return adjusted_value


    def get_current_valuation(self):
        # Just returns the final numeric output -> final evaluation of the product:
        depreciated_value = self.calculate_depreciation()
        with_uniqueness = self.calculate_uniqueness_premium(depreciated_value)
        with_preciousness = self.calculate_preciousness_premium(with_uniqueness)
        with_market_trend = self.apply_market_trend(with_preciousness)
        final_value = self.apply_additional_factors(with_market_trend)
        return round(final_value, 2)




class ServiceValuation:
    def __init__(self,category, base_rate, hours, expertise_level, demand_factor, additional_factors=None):
        # Initialise the service valutation model.
        # base_rate = hourly rate
        # expertise_level = Multiplier based on expertise_level, example -> 1.0 for junior (easy) tasks, 1.5 for senior(complex),
        # demand_factor = market demand factor, >1 for high demand, <1 for low demand.
        # additional_factors = Dictionary of other factors as defined by (user, LLM, tool)
        # Note : all this arguments are coming from previous steps / actions
        self.base_rate = base_rate
        self.hours = hours
        self.expertise_level = expertise_level
        self.demand_factor = demand_factor
        self.category = category
        self.additional_factors = additional_factors or {}


    def calculate_base_value(self):
        return self.base_rate * self.hours

    def apply_expertise_level(self, base_value):
        # Adjust the value based on the expertise level.
        return base_value * self.expertise_level

    def apply_demand_factor(self, base_value):
        # Adjust the value based on market demand.
        return base_value * self.demand_factor

    @staticmethod
    def fetch_market_trend(category):
        """
        Fetch market trend factor dynamically for the given category.

        :param category: (str) Service category to fetch trends for.
        :return: (dict) Market trend data.
        """
        try:
            response = requests.get(f"https://api.example.com/service-trends/{category}")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {"trend_factor": 1.0}  # Default trend factor


    def apply_additional_factors(self, base_value):
        # Adjust the value based on additional user-defined factors.
        # Each factor should be provided as a multiplier in the dictionary.
        adjusted_value = base_value
        for factor, multiplier in self.additional_factors.items():
            adjusted_value *= multiplier
        return adjusted_value

    def get_current_valuation(self):
        # Compute the final valuation of the service.
        base_value = self.calculate_base_value()
        with_expertise = self.apply_expertise_level(base_value)
        with_demand = self.apply_demand_factor(with_expertise)
        final_value = self.apply_additional_factors(with_demand)
        return round(final_value, 2)




class Verification:
    @staticmethod
    def verify_product_valuation(product_value, market_value_range):
        # Verify if the product valuation falls within an acceptable market value range.
        # product_value: (float) Valuation of the product.
        # market_value_range: (tuple) Acceptable range of market value (min, max).
        # :return: (bool) True if within range, False otherwise.
        return market_value_range[0] <= product_value <= market_value_range[1]
        # the exact way to verify may vary depending on whether i manage to get the market_value_range as an array of low and high values.


    @staticmethod
    def verify_service_valuation(service_value, industry_standard_rate):
        #  Verify if the service valuation is aligned with industry standards.
        # service_value: (float) Valuation of the service.
        # industry_standard_rate: (float) Average hourly rate for the service.
        # :return: (bool) True if valuation aligns with standards, False otherwise.
        average_value = service_value / industry_standard_rate
        return 0.8 <= average_value <= 1.2
        # variance -> should not be large

if __name__ == "__main__":
    # Product Valuation Example
    original_value = 1000  # Original price in dollars
    years_used = 10  # Years used
    depreciation_rate = 0.1  # 10% depreciation per year
    uniqueness_score = 0.8  # 80% uniqueness
    preciousness_score = 0.6  # 60% preciousness
    market_trend_factor = 1.2  # 20% higher demand
    additional_factors = {
        "brand_reputation": 1.1,  # 10% premium for brand reputation
        "special_features": 1.05  # 5% premium for additional features
    }

    product_valuation = ProductValuation(
        original_value,
        years_used,
        depreciation_rate,
        uniqueness_score,
        preciousness_score,
        market_trend_factor,
        additional_factors
    )

    product_value = product_valuation.get_current_valuation()
    print(f"The current valuation of the product is: ${product_value}")

    # Service Valuation Example
    base_rate = 50  # Hourly rate in dollars
    hours = 10  # Number of hours worked
    expertise_level = 1.5  # Senior level
    demand_factor = 1.2  # High demand
    additional_factors_service = {
        "specialization": 1.1,  # 10% premium for specialization
        "customer_ratings": 1.05  # 5% premium for high ratings
    }

    service_valuation = ServiceValuation(
        base_rate,
        hours,
        expertise_level,
        demand_factor,
        additional_factors_service
    )

    service_value = service_valuation.get_current_valuation()
    print(f"The current valuation of the service is: ${service_value}")

    # Verification Examples
    market_value_range = (800, 1200)  # Acceptable range for product valuation
    print(f"Product valuation verified: {Verification.verify_product_valuation(product_value, market_value_range)}")

    industry_standard_rate = 55  # Average hourly rate for service
    print(f"Service valuation verified: {Verification.verify_service_valuation(service_value, industry_standard_rate)}")
