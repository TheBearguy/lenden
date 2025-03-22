from services.product_valuation import ProductValuation
from services.service_valuation import ServiceValuation

if __name__ == "__main__":
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
