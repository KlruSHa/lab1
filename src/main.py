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


def token_flush(token):
    if "." in token and len(token) != 1:
        numbers_stack.push(float(token))
        token = ""
        return token
    elif token.isdigit():
        numbers_stack.push(int(token))
        token = ""
        return token
    elif "." in token and len(token) == 1:
        raise SyntaxError(f"Неизвестный токен - {token}")
    else:
        return ""


def count_bracket(expr, p):
    """
    Вычисляет математическое выражение в обратной польской нотации со скобками,
    путем рекурсивного раскрытия скобок
    Поддерживает работу с int | float и операциями + | - | * | ** | // | % | / | ~ # (унарные - +)

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
                if float(result) < 0:
                    return count_bracket(expr[:b_1] + " " + result[1:] + "~" + expr[i + 1:], b_1)
                else:
                    return count_bracket(expr[:b_1] + " " + result + " " + expr[i + 1:], b_1)
    elif "(" in expr or ")" in expr:
        raise SyntaxError("Неправильно расставлены скобки")
    else:
        return count_expr(expr)


def count_expr(expr):
    """
    Вычисляет математическое выражение в обратной польской нотации без скобок.
    Поддерживает работу с int | float и операциями + | - | * | ** | // | % | / | ~ # (унарные - +)
    
    Args:
        expr (str): Математическое выражение без скобок в виде строки

    Returns:
        int | float: Результат вычисления выражения
    """
    token = ""
    forward = 0
    for i in range(len(expr)):
        if expr[i].isdigit():
            token += expr[i]
        elif expr[i] == "+":
            token = token_flush(token)
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 + op2)
        elif expr[i] == "-":
            token = token_flush(token)
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 - op2)
        elif expr[i] == ".":
            if "." not in token:
                token += "."
            else:
                raise SyntaxError(f"Неизвестный токен - {token + expr[i]}")
        elif expr[i] == "~":
            token = token_flush(token)
            op1 = numbers_stack.pop()
            op1 *= -1
            numbers_stack.push(op1)
        elif expr[i] == "/":
            if not forward:
                token = token_flush(token)
                if i + 2 <= len(expr):
                    if expr[i + 1] == '/':
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        if not (isinstance(op1, int) and isinstance(op2, int)):
                            raise TypeError("// работает только с целыми")
                        if op2 == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        numbers_stack.push(op1 // op2)
                        forward = 1
                    else:
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        if op2 == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        numbers_stack.push(op1 / op2)
                else:
                    op2 = numbers_stack.pop()
                    op1 = numbers_stack.pop()
                    if op2 == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    numbers_stack.push(op1 / op2)
            else:
                forward = 0
        elif expr[i] == "*":
            if not forward:
                token = token_flush(token)
                if i + 2 <= len(expr):
                    if expr[i + 1] == '*':
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        numbers_stack.push(op1 ** op2)
                        forward = 1
                    else:
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        numbers_stack.push(op1 * op2)
                else:
                    op2 = numbers_stack.pop()
                    op1 = numbers_stack.pop()
                    numbers_stack.push(op1 * op2)
            else:
                forward = 0
        elif expr[i] == "%":
            token = token_flush(token)
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            if not (isinstance(op1, int) and isinstance(op2, int)):
                raise TypeError("% работает только с целыми")
            if op2 == 0:
                raise ZeroDivisionError("Деление на ноль")
            numbers_stack.push(op1 % op2)
        elif expr[i] == " ":
            token = token_flush(token)
        elif expr[i] == "#":
            token = token_flush(token)
        else:
            raise SyntaxError(f"Неизвестный токен - {expr[i]}")
    token_flush(token)
    return numbers_stack.pop()


def main() -> None:
    expr = input("")

    try:
        result = count_bracket(expr, 0)
        if numbers_stack.is_empty():
            print(result)
        else:
            raise SyntaxError("Лишние операнды")
    except (SyntaxError, IndexError, ZeroDivisionError, TypeError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
