import turtle

def draw_star(side_length):
    """Рисует пятиконечную звезду с заданной длиной стороны"""
    screen = turtle.Screen()          #  сначала создает окно
    screen.title("Звезда")
    screen.bgcolor("black")           #  чёрный фон

    t = turtle.Turtle()
    t.speed(5)
    t.color("gold", "yellow")
    t.begin_fill()

    for _ in range(5):
        t.forward(side_length)
        t.right(144)

    t.end_fill()
    t.hideturtle()

#  Ввод ДО открытия окна — в терминале
# лучше ввести длину 25 например
side = int(input("Введите длину стороны звезды: "))
draw_star(side)
turtle.done()