# Задание 1
def corrector(string, width, symbol):
    return string.center(width, symbol)


# Тест задания 1
print(corrector("привет", 20, "*"))
print(corrector("Python", 15, "-"))
print(corrector("ok", 10, "+"))


# Задание 2  простой калькулятор
def calculator():
    title = corrector(" Калькулятор ", 30, "=")
    print(title)

    num1 = float(input("Введите первое число: "))
    operator = input("Введите операцию (+, -, *, /): ")
    num2 = float(input("Введите второе число: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            print("Ошибка: деление на ноль!")
            return
    else:
        print("Неизвестная операция!")
        return

    print(corrector(f" Результат: {result} ", 30, "-"))


calculator()