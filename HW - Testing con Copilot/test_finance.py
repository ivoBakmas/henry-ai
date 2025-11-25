import pytest

from finance import (
    calculate_compound_interest,
    calculate_annuity_payment,
    calculate_internal_rate_of_return,
)


def test_compound_interest():
    principal = 1000.0
    rate = 0.05
    periods = 2
    expected = principal * ((1 + rate) ** periods)
    assert calculate_compound_interest(principal, rate, periods) == pytest.approx(expected)


def test_annuity_zero_rate():
    principal = 1200.0
    rate = 0.0
    periods = 12
    # With zero rate, payment is principal / periods
    assert calculate_annuity_payment(principal, rate, periods) == pytest.approx(principal / periods)


def test_annuity_non_zero_rate():
    principal = 1000.0
    rate = 0.05
    periods = 2
    expected = principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
    assert calculate_annuity_payment(principal, rate, periods) == pytest.approx(expected)


def test_internal_rate_of_return_npv_zero():
    cash_flows = [-100.0, 60.0, 60.0]
    irr = calculate_internal_rate_of_return(cash_flows, iterations=1000)
    # Returned IRR should make NPV approximately zero
    npv = sum(cf / (1 + irr) ** i for i, cf in enumerate(cash_flows))
    assert isinstance(irr, float)
    assert npv == pytest.approx(0.0, abs=1e-6)


def test_internal_rate_of_return_derivative_zero():
    # Construct cash flows that make the derivative sum zero immediately
    # Two contiguous zero cash flows (after the initial investment) cause
    # the derivative calculation (which multiplies by the index) to be zero.
    cash_flows = [-100.0, 0.0, 0.0]
    irr = calculate_internal_rate_of_return(cash_flows, iterations=10)
    # When derivative == 0 the function breaks and returns the current guess (initial 0.1)
    assert isinstance(irr, float)
    assert irr == pytest.approx(0.1)


if __name__ == "__main__":
    pytest.main([__file__])
