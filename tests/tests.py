import pytest
from main import count_expr, count_bracket


@pytest.mark.parametrize("expr, expected", [
    ("10 5 + 2 *", 30),
])
def test_count_expr(expr, expected):
    assert count_expr(expr) == expected


def test_count_expr_zero_division():
    with pytest.raises(ZeroDivisionError):
        count_expr("10 0 /")
    with pytest.raises(ZeroDivisionError):
        count_expr("10 0 %")


def test_count_expr_insufficient_operands():
    with pytest.raises(IndexError, match="Удаление с пустого стека"):
        count_expr("10 +")


@pytest.mark.parametrize("expr, expected", [
    ("(10 5 +)", 15),
    ("(5)", 5)
])
def test_count_bracket_valid_expressions(expr, expected):
    assert count_bracket(expr) == expected


@pytest.mark.parametrize("expr", [
    "((10 5 +)",
    "(10 5 +))",
    "10 5) + (",
])
def test_count_bracket_syntax_error(expr):
    with pytest.raises(SyntaxError, match="Неправильно расставлены скобки"):
        count_bracket(expr)
