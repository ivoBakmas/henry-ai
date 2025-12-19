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


def test_compound_interest_zero_principal():
    assert calculate_compound_interest(0.0, 0.05, 10) == pytest.approx(0.0)


def test_compound_interest_zero_periods():
    principal = 500.0
    assert calculate_compound_interest(principal, 0.07, 0) == pytest.approx(principal)


def test_compound_interest_negative_rate():
    principal = 1000.0
    rate = -0.05
    periods = 2
    expected = principal * ((1 + rate) ** periods)
    assert calculate_compound_interest(principal, rate, periods) == pytest.approx(expected)


def test_annuity_payment_one_period():
    principal = 1000.0
    rate = 0.05
    periods = 1
    expected = principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
    assert calculate_annuity_payment(principal, rate, periods) == pytest.approx(expected)


def test_annuity_payment_small_rate():
    principal = 1000.0
    rate = 1e-8
    periods = 10
    expected = principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
    assert calculate_annuity_payment(principal, rate, periods) == pytest.approx(expected, rel=1e-9)


def test_annuity_payment_large_periods():
    principal = 1000.0
    rate = 0.05
    periods = 360
    expected = principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
    assert calculate_annuity_payment(principal, rate, periods) == pytest.approx(expected, rel=1e-12)


def test_irr_single_period():
    cash_flows = [-100.0, 110.0]
    irr = calculate_internal_rate_of_return(cash_flows, iterations=100)
    # Exact solution is 0.1 for this simple case
    assert irr == pytest.approx(0.1, abs=1e-8)


def test_irr_all_zero_cashflows():
    cash_flows = [0.0, 0.0, 0.0]
    # NPV is zero and derivative is zero; function should break and return the initial guess
    irr = calculate_internal_rate_of_return(cash_flows, iterations=10)
    assert irr == pytest.approx(0.1)


def test_irr_single_period_high_return():
    cash_flows = [-100.0, 120.0]
    irr = calculate_internal_rate_of_return(cash_flows, iterations=100)
    # Exact solution is 0.2
    assert irr == pytest.approx(0.2, abs=1e-8)


def test_irr_zero_solution():
    # -100 + 0 + 100/(1+irr)^2 = 0 has irr == 0
    cash_flows = [-100.0, 0.0, 100.0]
    irr = calculate_internal_rate_of_return(cash_flows, iterations=100)
    assert irr == pytest.approx(0.0, abs=1e-6)


if __name__ == "__main__":
    pytest.main([__file__])
