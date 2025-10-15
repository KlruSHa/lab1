import pytest
from src.main import count_expr, count_bracket


@pytest.mark.parametrize("expr, expected", [
    ("5 10 3 + * 2 /", 32.5),
    ("100 50 25 - / 5 +", 9.0),
    ("7 4 3 + * 2 -", 47),
    ("2.5 1.5 0.5 * + 2 /", 1.625),
    ("10 3 % 2 * 10 2 / -", -3.0),
    ("-5 10 +", 5),
    ("10 -3 *", -30),
    ("4 -2 /", -2.0),
    ("2 3 ** 5 +", 13),
    ("10 3 // 2 *", 6),
    ("-2 3 **", -8),
    ("2 -3 **", 0.125),
])
def test_count_expr(expr, expected):
    assert count_expr(expr) == expected


def test_count_expr_zero_division():
    with pytest.raises(ZeroDivisionError):
        count_expr("10 0 /")
    with pytest.raises(ZeroDivisionError):
        count_expr("10 0 %")


def test_count_expr_insufficient_operands():
    with pytest.raises(IndexError, match="Недостаточно операндов"):
        count_expr("10 +")


@pytest.mark.parametrize("expr, expected", [
    ("( 20 5 /) (10 2 -) *", 32.0),
    ("((3 2 +) 4 *) 5 %", 0),
    ("10 (5 2 * (10 5 /) +) -", -2),
    ("(1 (2 (3 4 *) -) +)", -9),
    ("2 3 * (10 5 -) 2 / +", 8.5),
    ("(1.2 0.8 + (3 2 *) -) 2 / 0.5 +", -1.5),
    ("(3 2 ** 4 **)", 6561),
    ("100 (2 3 **) 10 / /", 125),
])
def test_count_bracket_valid_expressions(expr, expected):
    assert count_bracket(expr, 0) == expected


@pytest.mark.parametrize("expr", [
    "((10 5 +)",
    "(10 5 +))",
    "10 5) + (",
])
def test_count_bracket_syntax_error(expr):
    with pytest.raises(SyntaxError, match="Неправильно расставлены скобки"):
        count_bracket(expr, 0)
