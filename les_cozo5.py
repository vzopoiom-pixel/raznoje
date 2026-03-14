# главная строка
string = "ttttuuuurrrrttttlllleeee"

# первый способ : Используем set для удаления лишних символов
result1 = ''.join(set(string))
print("Способ 1:", result1)

#второй способ : Используем цикл для удаления повторений
result2 = ""
for char in string:
    if char not in result2:
        result2 += char
print("Способ 2:", result2)
