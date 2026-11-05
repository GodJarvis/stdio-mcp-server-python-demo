from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, ConfigDict, Field


class DiscountResult(BaseModel):
    """Structured discount calculation result returned to MCP clients."""

    model_config = ConfigDict(extra="forbid")

    currency: str = Field(description="ISO 4217 three-letter currency code.")
    original_unit_price: float
    discount_percent: float
    discount_amount_per_unit: float
    final_unit_price: float
    quantity: int
    total_original_amount: float
    total_discount_amount: float
    total_payable: float


def calculate_discount_value(
    original_price: float,
    discount_percent: float,
    quantity: int = 1,
    currency: str = "CNY",
    precision: int = 2,
) -> DiscountResult:
    """Calculate a discount using ROUND_HALF_UP and per-unit rounding first."""

    price = Decimal(str(original_price))
    percent = Decimal(str(discount_percent))
    quantizer = Decimal(1).scaleb(-precision)

    final_unit_price = (price * (Decimal(1) - percent / Decimal(100))).quantize(
        quantizer,
        rounding=ROUND_HALF_UP,
    )
    discount_per_unit = (price - final_unit_price).quantize(quantizer, rounding=ROUND_HALF_UP)
    total_original = (price * quantity).quantize(quantizer, rounding=ROUND_HALF_UP)
    total_payable = (final_unit_price * quantity).quantize(quantizer, rounding=ROUND_HALF_UP)
    total_discount = (total_original - total_payable).quantize(quantizer, rounding=ROUND_HALF_UP)

    return DiscountResult(
        currency=currency,
        original_unit_price=float(price.quantize(quantizer, rounding=ROUND_HALF_UP)),
        discount_percent=float(percent),
        discount_amount_per_unit=float(discount_per_unit),
        final_unit_price=float(final_unit_price),
        quantity=quantity,
        total_original_amount=float(total_original),
        total_discount_amount=float(total_discount),
        total_payable=float(total_payable),
    )

