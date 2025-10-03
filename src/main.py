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
            raise IndexError("Удаление с пустого стека")
        return self.items.pop()

    def is_empty(self):
        return (self.items == [])


numbers_stack = Stack()


def count_bracket(expr):
    """
            Вычисляет математическое выражение в обратной польской нотации со скобками,
            путем рекурсивного раскрытия скобок
            Поддерживает работу с int\float и операциями + \ - \ * \ ** \ // \ % \ /

            Args:
                expr (str): Математическое выражение без скобок в виде строки

            Returns:
                int | float: Результат вычисления выражения
    """
    global numbers_stack
    b_1 = -1
    b_2 = -1
    if "(" in expr and ")" in expr:
        for i in range(len(expr)):
            if expr[i] == "(":
                b_1 = i
            elif expr[i] == ")" and b_1 == -1:
                raise SyntaxError("Неправильно расставлены скобки")
            elif expr[i] == ")":
                b_2 = i
                result = str(count_bracket(expr[b_1 + 1:b_2]))
                return count_bracket(expr[:b_1] + result + expr[b_2 + 1:])
    elif "(" in expr or ")" in expr:
        raise SyntaxError("Неправильно расставлены скобки")
    else:
        return count_expr(expr)


def count_expr(expr):
    """
    Вычисляет математическое выражение в обратной польской нотации без скобок.
    Поддерживает работу с int\float и операциями + \ - \ * \ ** \ // \ % \ /

    Args:
        expr (str): Математическое выражение без скобок в виде строки

    Returns:
        int | float: Результат вычисления выражения
    """
    global numbers_stack
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
    global numbers_stack
    expr = input()

    try:
        result = count_bracket(expr)
        if not numbers_stack.items:
            print(result)
        else:
            raise SyntaxError("Лишние операнды")
        #print(f"Stack: {numbers_stack.items}")
    except (SyntaxError, IndexError, ZeroDivisionError, TypeError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
