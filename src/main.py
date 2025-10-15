class Stack:
    """
    Класс, реализующий стек, с основными методами.

    Основные методы:
    1. push - добавляет элемент в стек
    2. pop - удаляет элемент из стека
    3. is_empty - проверяет пустой ли стек
    """

    def __init__(self, *args):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("Недостаточно операндов")
        return self.items.pop()

    def is_empty(self):
        return (self.items == [])


numbers_stack = Stack()
bracket_indexes = Stack()


def count_bracket(expr, p):
    """
    Вычисляет математическое выражение в обратной польской нотации со скобками,
    путем рекурсивного раскрытия скобок
    Поддерживает работу с int | float и операциями + | - | * | ** | // | % | /

    Args:
        expr (str): Математическое выражение без скобок в виде строки
        p : Индекс, с которого начнем идти по строке

    Returns:
        int | float: Результат вычисления выражения
    """
    if "(" in expr and ")" in expr:
        for i in range(p, len(expr)):
            if expr[i] == "(":
                bracket_indexes.push(i)
            elif expr[i] == ")" and bracket_indexes.is_empty():
                raise SyntaxError("Неправильно расставлены скобки")
            elif expr[i] == ")":
                b_1 = bracket_indexes.pop()
                result = str(count_expr(expr[b_1 + 1:i]))
                return count_bracket(expr[:b_1] + result + expr[i + 1:], b_1)
    elif "(" in expr or ")" in expr:
        raise SyntaxError("Неправильно расставлены скобки")
    else:
        return count_expr(expr)


def count_expr(expr):
    """
    Вычисляет математическое выражение в обратной польской нотации без скобок.
    Поддерживает работу с int | float и операциями + | - | * | ** | // | % | /
    
    Args:
        expr (str): Математическое выражение без скобок в виде строки

    Returns:
        int | float: Результат вычисления выражения
    """
    tokens = expr.split()
    for token in tokens:
        if token.replace('.', '', 1).lstrip('+-').isdigit():
            if '.' in token:
                numbers_stack.push(float(token))
            else:
                numbers_stack.push(int(token))
        elif token == "+":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 + op2)
        elif token == "-":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 - op2)
        elif token == "*":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 * op2)
        elif token == "/":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            if op2 == 0:
                raise ZeroDivisionError("Деление на ноль")
            numbers_stack.push(op1 / op2)
        elif token == "//":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            if not (isinstance(op1, int) and isinstance(op2, int)):
                raise TypeError("// работает только с целыми")
            if op2 == 0:
                raise ZeroDivisionError("Деление на ноль")
            numbers_stack.push(op1 // op2)
        elif token == "%":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            if not (isinstance(op1, int) and isinstance(op2, int)):
                raise TypeError("% работает только с целыми")
            if op2 == 0:
                raise ZeroDivisionError("Деление на ноль")
            numbers_stack.push(op1 % op2)
        elif token == "**":
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 ** op2)
        else:
            raise SyntaxError(f"Неизвестный токен: {token}")
    return numbers_stack.pop()


def main() -> None:
    expr = input()

    try:
        result = count_bracket(expr, 0)
        if not numbers_stack.items:
            print(result)
        else:
            raise SyntaxError("Лишние операнды")
    except (SyntaxError, IndexError, ZeroDivisionError, TypeError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
