import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 500, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Смайлы 😊")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 22, bold=True)
font_big = pygame.font.SysFont("monospace", 28, bold=True)

# ── Цвета ──────────────────────────────────────────────────────────────────
BG       = (30,  30,  40)
YELLOW   = (255, 220,  0)
D_YELLOW = (200, 160,  0)
BLACK    = (0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (220,  40,  40)
PINK     = (255, 180, 200)
BLUE     = (50,  100, 255)
GREEN    = (50,  200,  80)
ORANGE   = (255, 150,  30)
PURPLE   = (160,  60, 220)
GREY     = (180, 180, 180)
BTN_N    = (60,  60,  80)
BTN_H    = (90,  90, 120)
BTN_A    = (100, 60, 180)

CX, CY, CR = WIDTH // 2, 210, 110

# ── Смайлы ──────────────────────────────────────────────────────────────────
# Каждый смайл: (название, цвет_лица, функция_рта, особые_черты)
SMILES = [
    "😊 Радость",
    "😢 Грусть",
    "😠 Злость",
    "😲 Удивление",
    "😎 Крутой",
    "😍 Влюблённый",
    "🤔 Задумчивый",
    "😴 Сонный",
]

current = 0
tick = 0

# ── Рисование смайлов ────────────────────────────────────────────────────────

def draw_face(surf, idx, cx, cy, r, t):
    # Тень
    pygame.draw.circle(surf, (0,0,0,80), (cx+6, cy+6), r)

    colors = [YELLOW, (150,200,255), (255,150,100),
              YELLOW, YELLOW, YELLOW, (255,230,100), (200,220,255)]
    face_color = colors[idx]

    pygame.draw.circle(surf, D_YELLOW if idx != 7 else (150,170,200), (cx, cy), r)
    pygame.draw.circle(surf, face_color, (cx, cy), r-4)

    if idx == 0:   draw_happy(surf, cx, cy, r, t)
    elif idx == 1: draw_sad(surf, cx, cy, r, t)
    elif idx == 2: draw_angry(surf, cx, cy, r, t)
    elif idx == 3: draw_surprised(surf, cx, cy, r, t)
    elif idx == 4: draw_cool(surf, cx, cy, r, t)
    elif idx == 5: draw_love(surf, cx, cy, r, t)
    elif idx == 6: draw_thinking(surf, cx, cy, r, t)
    elif idx == 7: draw_sleepy(surf, cx, cy, r, t)

def draw_happy(surf, cx, cy, r, t):
    # Глаза — дуги (закрытые от радости)
    for ox in (-r//3, r//3):
        pygame.draw.arc(surf, BLACK,
                        (cx+ox-14, cy-r//3-10, 28, 20),
                        math.pi*0.1, math.pi*0.9, 4)
    # Щёчки
    pygame.draw.circle(surf, PINK, (cx - r//2, cy + r//8), 18)
    pygame.draw.circle(surf, PINK, (cx + r//2, cy + r//8), 18)
    # Рот — улыбка
    pygame.draw.arc(surf, BLACK,
                    (cx - r//2, cy - r//8, r, r//2),
                    math.pi*1.1, math.pi*1.9, 5)

def draw_sad(surf, cx, cy, r, t):
    # Глаза
    for ox in (-r//3, r//3):
        pygame.draw.circle(surf, BLACK, (cx+ox, cy-r//4), 10)
        pygame.draw.circle(surf, WHITE, (cx+ox+3, cy-r//4-3), 4)
    # Брови грустные
    for ox, sign in [(-r//3, 1), (r//3, -1)]:
        pygame.draw.line(surf, BLACK,
                         (cx+ox-15, cy-r//2+sign*8),
                         (cx+ox+15, cy-r//2-sign*8), 4)
    # Рот — грусть
    pygame.draw.arc(surf, BLACK,
                    (cx - r//2, cy + r//6, r, r//2),
                    math.pi*0.1, math.pi*0.9, 5)
    # Слеза
    drop_y = cy - r//4 + 15 + int(10 * abs(math.sin(t * 0.05)))
    pygame.draw.ellipse(surf, BLUE, (cx - r//3 - 5, drop_y, 10, 14))

def draw_angry(surf, cx, cy, r, t):
    # Глаза
    for ox in (-r//3, r//3):
        pygame.draw.circle(surf, BLACK, (cx+ox, cy-r//4), 11)
        pygame.draw.circle(surf, RED,   (cx+ox, cy-r//4), 7)
        pygame.draw.circle(surf, BLACK, (cx+ox, cy-r//4), 4)
    # Брови сердитые — V-форма
    pygame.draw.line(surf, BLACK,
                     (cx - r//2, cy - r//2),
                     (cx - r//6, cy - r//3), 6)
    pygame.draw.line(surf, BLACK,
                     (cx + r//6, cy - r//3),
                     (cx + r//2, cy - r//2), 6)
    # Рот злой
    pts = [(cx - r//3, cy + r//4),
           (cx - r//6, cy + r//6),
           (cx,        cy + r//4),
           (cx + r//6, cy + r//6),
           (cx + r//3, cy + r//4)]
    pygame.draw.lines(surf, BLACK, False, pts, 5)
    # Пар из ноздрей
    shake = int(3 * math.sin(t * 0.3))
    pygame.draw.circle(surf, RED, (cx - 12 + shake, cy + 5), 6)
    pygame.draw.circle(surf, RED, (cx + 12 - shake, cy + 5), 6)

def draw_surprised(surf, cx, cy, r, t):
    # Глаза большие
    for ox in (-r//3, r//3):
        pygame.draw.circle(surf, WHITE, (cx+ox, cy-r//4), 16)
        pygame.draw.circle(surf, BLACK, (cx+ox, cy-r//4), 10)
        pygame.draw.circle(surf, WHITE, (cx+ox+4, cy-r//4-4), 4)
    # Брови вверх
    for ox in (-r//3, r//3):
        pygame.draw.arc(surf, BLACK,
                        (cx+ox-15, cy-r//2-10, 30, 20),
                        math.pi*0.2, math.pi*0.8, 4)
    # Рот — O
    bob = int(4 * math.sin(t * 0.08))
    pygame.draw.ellipse(surf, BLACK, (cx-20, cy+r//8+bob, 40, 35))
    pygame.draw.ellipse(surf, (80,40,10), (cx-15, cy+r//8+5+bob, 30, 25))

def draw_cool(surf, cx, cy, r, t):
    # Очки-прямоугольники
    for ox in (-r//3, r//3):
        pygame.draw.rect(surf, BLACK, (cx+ox-20, cy-r//3-10, 38, 26), border_radius=6)
        pygame.draw.rect(surf, (20,20,60), (cx+ox-18, cy-r//3-8, 34, 22), border_radius=5)
        pygame.draw.circle(surf, WHITE, (cx+ox+4, cy-r//3), 5)
    # Перемычка очков
    pygame.draw.line(surf, BLACK, (cx-r//3+18, cy-r//3), (cx+r//3-18, cy-r//3), 3)
    # Улыбка набок
    pygame.draw.arc(surf, BLACK,
                    (cx - r//2 + 10, cy - r//8, r - 10, r//2),
                    math.pi*1.2, math.pi*1.85, 5)

def draw_love(surf, cx, cy, r, t):
    # Глаза-сердечки
    for ox in (-r//3, r//3):
        _draw_heart(surf, cx+ox, cy-r//4, 14, RED)
    # Щёчки
    pygame.draw.circle(surf, PINK, (cx - r//2, cy + r//8), 20)
    pygame.draw.circle(surf, PINK, (cx + r//2, cy + r//8), 20)
    # Улыбка
    pygame.draw.arc(surf, BLACK,
                    (cx - r//2, cy - r//8, r, r//2),
                    math.pi*1.1, math.pi*1.9, 5)
    # Летящие сердечки
    for i, (hx, hy, hr) in enumerate([
        (cx + r - 20, cy - r + int(10*math.sin(t*0.07+i)), 10),
        (cx - r + 10, cy - r + 20 + int(8*math.sin(t*0.05)), 7),
    ]):
        _draw_heart(surf, hx, hy, hr, RED)

def _draw_heart(surf, cx, cy, size, color):
    pts = []
    for a in range(360):
        rad = math.radians(a)
        x = size * (16 * math.sin(rad)**3)
        y = -size * (13*math.cos(rad) - 5*math.cos(2*rad)
                     - 2*math.cos(3*rad) - math.cos(4*rad))
        pts.append((cx + x//6, cy + y//6))
    if len(pts) >= 3:
        pygame.draw.polygon(surf, color, pts)

def draw_thinking(surf, cx, cy, r, t):
    # Один глаз прищурен
    pygame.draw.circle(surf, BLACK, (cx - r//3, cy - r//4), 10)
    pygame.draw.circle(surf, WHITE, (cx - r//3 + 3, cy - r//4 - 3), 4)
    pygame.draw.arc(surf, BLACK,
                    (cx + r//3 - 14, cy - r//3 - 6, 28, 16),
                    math.pi*0.1, math.pi*0.9, 4)
    # Бровь думающая
    pygame.draw.line(surf, BLACK,
                     (cx - r//2, cy - r//2 + 5),
                     (cx - r//6, cy - r//2 - 5), 4)
    pygame.draw.line(surf, BLACK,
                     (cx + r//6, cy - r//2 - 5),
                     (cx + r//2, cy - r//2 + 5), 4)
    # Рука у подбородка
    pygame.draw.circle(surf, YELLOW, (cx + r - 10, cy + r//2), 22)
    # Рот нейтральный
    pygame.draw.line(surf, BLACK, (cx-20, cy+r//3), (cx+20, cy+r//3), 4)
    # Пузырьки мысли
    for i, (bx, by, br) in enumerate([
        (cx + r + 20, cy - r//2 + int(5*math.sin(t*0.04+i)), 8),
        (cx + r + 38, cy - r + 5 + int(5*math.sin(t*0.04+1)), 12),
        (cx + r + 60, cy - r - 15 + int(5*math.sin(t*0.04+2)), 18),
    ]):
        pygame.draw.circle(surf, WHITE, (bx, by), br)
        pygame.draw.circle(surf, GREY,  (bx, by), br, 2)
    # Облачко мысли
    cloud_x, cloud_y = cx + r + 75, cy - r - 20
    for dx, dy, cr2 in [(-20,10,18),(0,0,22),(20,10,18),(10,22,15),(-10,22,15)]:
        pygame.draw.circle(surf, WHITE, (cloud_x+dx, cloud_y+dy), cr2)
        pygame.draw.circle(surf, GREY,  (cloud_x+dx, cloud_y+dy), cr2, 2)
    q = font.render("?", True, PURPLE)
    surf.blit(q, (cloud_x - 8, cloud_y - 5))

def draw_sleepy(surf, cx, cy, r, t):
    # Закрытые глаза — линии
    for ox in (-r//3, r//3):
        pygame.draw.line(surf, BLACK,
                         (cx+ox-14, cy-r//4),
                         (cx+ox+14, cy-r//4), 5)
        # Ресницы
        for lx in range(-10, 15, 8):
            pygame.draw.line(surf, BLACK,
                             (cx+ox+lx, cy-r//4),
                             (cx+ox+lx-3, cy-r//4-8), 3)
    # Рот зевающий / нейтральный
    yawn = int(15 * abs(math.sin(t * 0.02)))
    pygame.draw.ellipse(surf, BLACK, (cx-20, cy+r//6, 40, 20+yawn))
    # Буква Z
    zs = [(cx+r-20, cy - r//3 + int(8*math.sin(t*0.05))),
          (cx+r+5,  cy - r//2 + int(6*math.sin(t*0.05+1))),
          (cx+r+25, cy - r    + int(5*math.sin(t*0.05+2)))]
    sizes = [18, 24, 32]
    for (zx, zy), sz in zip(zs, sizes):
        s = int(sz * abs(math.sin(t * 0.02 + sz)))
        if s < 4: continue
        col = (*BLUE[:3],)
        pygame.draw.line(surf, col, (zx, zy),         (zx+s, zy),     3)
        pygame.draw.line(surf, col, (zx+s, zy),       (zx, zy+s),     3)
        pygame.draw.line(surf, col, (zx, zy+s),       (zx+s, zy+s),   3)

# ── Кнопки ───────────────────────────────────────────────────────────────────

BTN_W, BTN_H_SIZE = 160, 46
btn_prev = pygame.Rect(WIDTH//2 - BTN_W - 20, HEIGHT - 80, BTN_W, BTN_H_SIZE)
btn_next = pygame.Rect(WIDTH//2 + 20,          HEIGHT - 80, BTN_W, BTN_H_SIZE)

def draw_button(surf, rect, text, hovered, active=False):
    color = BTN_A if active else (BTN_H if hovered else BTN_N)
    pygame.draw.rect(surf, color, rect, border_radius=12)
    pygame.draw.rect(surf, WHITE, rect, 2, border_radius=12)
    label = font_big.render(text, True, WHITE)
    surf.blit(label, (rect.centerx - label.get_width()//2,
                      rect.centery - label.get_height()//2))

# ── Основной цикл ─────────────────────────────────────────────────────────────

prev_pressed = False
next_pressed = False

while True:
    tick += 1
    mx, my = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_LEFT, pygame.K_a):
                current = (current - 1) % len(SMILES)
            if e.key in (pygame.K_RIGHT, pygame.K_d):
                current = (current + 1) % len(SMILES)
        if e.type == pygame.MOUSEBUTTONDOWN:
            if btn_prev.collidepoint(mx, my):
                current = (current - 1) % len(SMILES)
            if btn_next.collidepoint(mx, my):
                current = (current + 1) % len(SMILES)

    # Фон
    screen.fill(BG)

    # Заголовок
    title = font_big.render(SMILES[current], True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

    # Счётчик
    counter = font.render(f"{current+1} / {len(SMILES)}", True, GREY)
    screen.blit(counter, (WIDTH//2 - counter.get_width()//2, 60))

    # Смайл
    draw_face(screen, current, CX, CY, CR, tick)

    # Точки-индикаторы
    for i in range(len(SMILES)):
        col = WHITE if i == current else GREY
        r2  = 7 if i == current else 4
        pygame.draw.circle(screen, col, (WIDTH//2 - (len(SMILES)-1)*12 + i*24, HEIGHT-110), r2)

    # Кнопки
    draw_button(screen, btn_prev, "◀  Назад",
                btn_prev.collidepoint(mx, my),
                mouse_pressed and btn_prev.collidepoint(mx, my))
    draw_button(screen, btn_next, "Вперёд  ▶",
                btn_next.collidepoint(mx, my),
                mouse_pressed and btn_next.collidepoint(mx, my))

    # Подсказка
    hint = font.render("← → или кнопки для переключения", True, (100,100,120))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 25))

    pygame.display.flip()
    clock.tick(60)
