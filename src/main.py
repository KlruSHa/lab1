class Stack:   # Обычная реализация стека
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
    """
    Вспомогательная функция, которая скидывает в стек операнд

    Args:
        token (str): Операнд

    Returns:
        str: Пустая строка
    """
    if "." in token and len(token) != 1: # Кладем в стек вещ. число и проверяем, что это не просто точка
        numbers_stack.push(float(token))
        token = ""
        return token
    elif token.isdigit(): # Кладем в стек целое число
        numbers_stack.push(int(token))
        token = ""
        return token
    elif "." in token and len(token) == 1: # Вызываем ошибку т.к не можем положить просто точку в стек
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
    if "(" in expr and ")" in expr:  # Проверяем есть ли скобки
        for i in range(p, len(expr)):
            if expr[i] == "(":
                bracket_indexes.push(i)
            elif expr[i] == ")" and bracket_indexes.is_empty(): # Если встретили закрыв. скобку, но откр. не было, то это ошибка
                raise SyntaxError("Неправильно расставлены скобки")
            elif expr[i] == ")":
                b_1 = bracket_indexes.pop()
                result = str(count_expr(expr[b_1 + 1:i]))  # Считаем выражение в скобке
                if float(result) < 0: # Проверяем на отрицательность результат т.к унарные минусы у нас оператор и обрабатываются по другому
                    return count_bracket(expr[:b_1] + " " + result[1:] + "~" + expr[i + 1:], b_1) # Рекурсивно вызываем, уже с результатом посчитанной скобки
                else:
                    return count_bracket(expr[:b_1] + " " + result + " " + expr[i + 1:], b_1)
    elif "(" in expr or ")" in expr: # Если какой-то один вид скобок, то это ошибка
        raise SyntaxError("Неправильно расставлены скобки")
    else:
        return count_expr(expr)  # Если скобок в выражении нет, то вызываем ф-ию, которая считает такие выражения


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
    for i in range(len(expr)): # Идем по символам и обрабатываем
        if expr[i].isdigit(): # Если встретили число, то добавляем его к текущему токену
            token += expr[i]
        elif expr[i] == "+": # Если встретили оператор, то
            token = token_flush(token) # Скидываем текущий токен в стек и очищаем токен
            op2 = numbers_stack.pop() # Достаем из стека нужные нам операнды
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 + op2) # Выполняем встретившийся нам оператор с операндами, которые мы достали
        elif expr[i] == "-":
            token = token_flush(token)
            op2 = numbers_stack.pop()
            op1 = numbers_stack.pop()
            numbers_stack.push(op1 - op2)
        elif expr[i] == ".": # Если встретили точку, то
            if "." not in token: # Проверяем, что она первая в токене
                token += "."
            else:
                raise SyntaxError(f"Неизвестный токен - {token + expr[i]}") # Иначе ошибка и неверный токен
        elif expr[i] == "~":
            token = token_flush(token)
            op1 = numbers_stack.pop()
            op1 *= -1
            numbers_stack.push(op1)
        elif expr[i] == "/": # Если встретили оператор, который может трактоваться по разному (/ //), то
            if not forward:
                token = token_flush(token)
                if i + 2 <= len(expr): # Сначала проверяем, что можем посмотреть следующий символ, возможно он //
                    if expr[i + 1] == '/': # Если след. символ оказался /, то выполняем //
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        if not (isinstance(op1, int) and isinstance(op2, int)):
                            raise TypeError("// работает только с целыми")
                        if op2 == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        numbers_stack.push(op1 // op2)
                        forward = 1
                    else: # Идем сюда, если след. символ был не / и выполняем обычный /
                        op2 = numbers_stack.pop()
                        op1 = numbers_stack.pop()
                        if op2 == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        numbers_stack.push(op1 / op2)
                else: # Идем сюда, если не можем проверить след. символ и выполняем обычный /
                    op2 = numbers_stack.pop()
                    op1 = numbers_stack.pop()
                    if op2 == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    numbers_stack.push(op1 / op2)
            else:
                forward = 0
        elif expr[i] == "*": # Аналогично / //
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
    token_flush(token) # Обрабатываем токен, если он стоит последним, например (7)
    return numbers_stack.pop()


def main() -> None:
    expr = input("Введите выражение в RPN: ")  # Ввод выражения

    try:
        result = count_bracket(expr, 0)
        if numbers_stack.is_empty():
            print(f"Результат вычислений: {result}")
        else:
            raise SyntaxError("Лишние операнды")
    except (SyntaxError, IndexError, ZeroDivisionError, TypeError, RecursionError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
