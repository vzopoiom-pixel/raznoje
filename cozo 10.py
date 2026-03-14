import turtle

# Задаём размеры прямоугольника
width = 100
height = 150

# Настраиваем 
t = turtle.Turtle()

# Рисуем прямоугольник 
t.forward(width)
t.left(90)
t.forward(height)
t.left(90)
t.forward(width)
t.left(90)
t.forward(height)
t.left(90)

# Оставляем окно открытым
turtle.done()
