import IGRA

# настройки
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Сложная фигура")

t = turtle.Turtle()
t.speed(3)
t.width(2)

# спираль
print("Шаг 1: Рисуем спираль")
t.color("cyan")
for i in range(20):
    t.forward(10 + i * 5)
    t.left(45)

#  возращение в центр
print("Шаг 2: Возврат в центр")
t.penup()
t.goto(0, 0)
t.setheading(0)
t.pendown()

# звезда
print("Шаг 3: Рисуем звезду")
t.color("yellow")
for i in range(5):
    t.forward(120)
    t.right(144)

# возращение в центр
t.penup()
t.goto(0, 0)
t.setheading(0)
t.pendown()

# шисти угольник
print("Шаг 5: Рисуем шестиугольник")
t.color("magenta")
t.penup()
t.goto(0, -150)
t.pendown()
for i in range(6):
    t.forward(150)
    t.left(60)

# рисуем лучь
print("Шаг 6: Рисуем лучи")
t.color("orange")
for i in range(12):
    t.penup()
    t.goto(0, 0)
    t.setheading(i * 30)
    t.pendown()
    t.forward(100)

#  ФИНАЛ
t.hideturtle()
print("Готово!")
turtle.done()