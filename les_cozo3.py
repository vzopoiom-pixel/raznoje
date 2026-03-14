# Запрашиваем у пользователя количество правильных ответов
correct_answers = int(input("Введите количество правильных ответов (от 1 до 25): "))



# главное, чтобы число было в пределах от 1 до 25
if correct_answers < 1 or correct_answers > 25:
    print("Ошибка: число должно быть в диапазоне от 1 до 25.")

    
elif correct_answers >= 1 and correct_answers <= 5:
    print("Ужасний результат")
    
elif correct_answers >= 6 and correct_answers <= 10:
    print("Плохой результат")
    
elif correct_answers >= 11 and correct_answers <= 15:
    print("Средний результат")
    
elif correct_answers >= 16 and correct_answers <= 20:
    print("Хороший результат")
    
elif correct_answers >= 21 and correct_answers <= 25:
    print("Оличний результат")










    
