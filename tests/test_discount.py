from app.discount import calculate_discount_value


def test_calculate_discount_uses_per_unit_rounding() -> None:
    result = calculate_discount_value(199.9, 15, quantity=2)

    assert result.final_unit_price == 169.92
    assert result.total_discount_amount == 59.96
    assert result.total_payable == 339.84


def test_round_half_up_matches_money_expectation() -> None:
    result = calculate_discount_value(1.005, 0, precision=2)

    assert result.original_unit_price == 1.01

