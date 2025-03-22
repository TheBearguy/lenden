import requests

class ProductValuation:
    def __init__(self, category, original_value, years_used, uniqueness_score, preciousness_score, market_trend_factor, additional_factors=None):
        self.original_value = original_value
        self.years_used = years_used
        self.uniqueness_score = uniqueness_score
        self.preciousness_score = preciousness_score
        self.market_trend_factor = market_trend_factor
        self.category = category
        self.additional_factors = additional_factors or {}
        self.model = joblib.load("depreciation_model.pkl")

    def predict_depreciation_rate(self):
        input_features = np.array([[self.uniqueness_score, self.preciousness_score, self.market_trend_factor, self.years_used]])
        return self.model.predict(input_features)[0]

    def calculate_valuation(self):
        depreciation_rate = self.predict_depreciation_rate()
        depreciated_value = self.original_value * (1 - depreciation_rate) ** self.years_used
        with_uniqueness = depreciated_value * (1 + self.uniqueness_score * 0.5)
        with_preciousness = with_uniqueness * (1 + self.preciousness_score * 0.3)
        with_market_trend = with_preciousness * self.market_trend_factor

        final_value = with_market_trend
        for factor, multiplier in self.additional_factors.items():
            final_value *= multiplier

        return round(final_value, 2)


class ServiceValuation:
    def __init__(self, category, base_rate, hours, expertise_level, demand_factor, additional_factors=None):
        self.base_rate = base_rate
        self.hours = hours
        self.expertise_level = expertise_level
        self.demand_factor = demand_factor
        self.category = category
        self.additional_factors = additional_factors or {}

    def calculate_valuation(self):
        base_value = self.base_rate * self.hours
        with_expertise = base_value * self.expertise_level
        with_demand = with_expertise * self.demand_factor

        final_value = with_demand
        for factor, multiplier in self.additional_factors.items():
            final_value *= multiplier

        return round(final_value, 2)


class Verification:
    @staticmethod
    def verify_product_valuation(product_value, market_value_range):
        return market_value_range[0] <= product_value <= market_value_range[1]

    @staticmethod
    def verify_service_valuation(service_value, industry_standard_rate):
        average_value = service_value / industry_standard_rate
        return 0.8 <= average_value <= 1.2


if __name__ == "__main__":
    # Example run
    product = ProductValuation(
        category="electronics",
        original_value=1000,
        years_used=5,
        uniqueness_score=0.7,
        preciousness_score=0.6,
        market_trend_factor=1.2,
        additional_factors={"brand_reputation": 1.1, "special_features": 1.05}
    )
    print("Predicted product valuation:", product.calculate_valuation())

    service = ServiceValuation(
        category="consulting",
        base_rate=100,
        hours=8,
        expertise_level=1.4,
        demand_factor=1.2,
        additional_factors={"certification_bonus": 1.1}
    )
    print("Predicted service valuation:", service.calculate_valuation())