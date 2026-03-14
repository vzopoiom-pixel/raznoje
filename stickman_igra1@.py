import pygame
import sys
import math
import random

pygame.init()

# ── Константы ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 900, 560
FPS = 60
GRAVITY = 0.55
JUMP_FORCE = -13
PLAYER_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Adventure")
clock = pygame.time.Clock()

font      = pygame.font.SysFont("monospace", 22, bold=True)
font_big  = pygame.font.SysFont("monospace", 48, bold=True)
font_med  = pygame.font.SysFont("monospace", 30, bold=True)

# ── Цвета ────────────────────────────────────────────────────────────────────
SKY_TOP    = (100, 180, 255)
SKY_BOT    = (200, 230, 255)
GROUND_C   = (80,  160,  60)
DIRT_C     = (140, 100,  60)
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
RED        = (220,  40,  40)
DARK_RED   = (160,  20,  20)
YELLOW     = (255, 220,  0)
GOLD       = (255, 180,  0)
ORANGE     = (255, 130,  20)
BLUE       = (50,  100, 255)
GREEN      = (50,  200,  80)
DARK_GREEN = (30,  130,  50)
PURPLE     = (150,  60, 220)
GREY       = (150, 150, 150)
DARK       = (30,   30,  40)
BROWN      = (120,  80,  40)
PLAT_C     = (80,  160,  60)
PLAT_TOP   = (120, 200,  80)

# ── Рисование человечка (stickman) ──────────────────────────────────────────

def draw_stickman(surf, x, y, color, scale=1.0, walk_t=0, facing=1,
                  is_dead=False, dead_angle=0, hat_color=None, enemy=False):
    """
    x, y — центр бёдер (pivot)
    walk_t — фаза анимации ходьбы
    facing — 1=вправо, -1=влево
    """
    s = scale
    # Анимация ног
    leg_swing = math.sin(walk_t * 0.25) * 25 * s
    arm_swing = math.sin(walk_t * 0.25 + math.pi) * 20 * s

    if is_dead:
        # Упавший человечек
        cx, cy = int(x), int(y)
        angle = dead_angle
        # Тело лёжа
        bx = int(cx + math.cos(math.radians(angle)) * 20 * s)
        by = int(cy + math.sin(math.radians(angle)) * 20 * s)
        pygame.draw.line(surf, color, (cx, cy), (bx, by), max(1, int(3*s)))
        # Голова
        hx = int(bx + math.cos(math.radians(angle)) * 12 * s)
        hy = int(by + math.sin(math.radians(angle)) * 12 * s)
        pygame.draw.circle(surf, color, (hx, hy), max(1, int(9*s)))
        # Руки-ноги врассыпную
        pygame.draw.line(surf, color, (cx, cy),
                         (int(cx - 15*s), int(cy - 10*s)), max(1, int(3*s)))
        pygame.draw.line(surf, color, (cx, cy),
                         (int(cx + 15*s), int(cy + 5*s)), max(1, int(3*s)))
        pygame.draw.line(surf, color, (cx, cy),
                         (int(cx - 10*s), int(cy + 15*s)), max(1, int(3*s)))
        pygame.draw.line(surf, color, (cx, cy),
                         (int(cx + 5*s), int(cy - 15*s)), max(1, int(3*s)))
        return

    ix, iy = int(x), int(y)
    lw = max(1, int(3 * s))

    # Ноги
    lleg_end = (int(ix - 8*s*facing), int(iy + 25*s + leg_swing*facing))
    rleg_end = (int(ix + 8*s*facing), int(iy + 25*s - leg_swing*facing))
    pygame.draw.line(surf, color, (ix, iy), lleg_end, lw)
    pygame.draw.line(surf, color, (ix, iy), rleg_end, lw)
    # Ступни
    pygame.draw.line(surf, color, lleg_end,
                     (lleg_end[0] + int(7*s*facing), lleg_end[1]), lw)
    pygame.draw.line(surf, color, rleg_end,
                     (rleg_end[0] + int(7*s*facing), rleg_end[1]), lw)

    # Тело
    body_top = (ix, int(iy - 25*s))
    pygame.draw.line(surf, color, (ix, iy), body_top, lw)

    # Руки
    larm = (int(ix - 18*s), int(iy - 10*s + arm_swing*0.5))
    rarm = (int(ix + 18*s), int(iy - 10*s - arm_swing*0.5))
    pygame.draw.line(surf, color, body_top, larm, lw)
    pygame.draw.line(surf, color, body_top, rarm, lw)

    # Голова
    head_c = (ix, int(iy - 35*s))
    pygame.draw.circle(surf, color, head_c, max(1, int(9*s)))

    # Глаза
    ex = int(3*s*facing)
    pygame.draw.circle(surf, BLACK if not enemy else RED,
                       (head_c[0]+ex, head_c[1]-2), max(1, int(2*s)))

    # Шляпа игрока
    if hat_color:
        hx, hy = head_c
        pygame.draw.rect(surf, hat_color,
                         (hx - int(10*s), hy - int(18*s),
                          int(20*s), int(10*s)), border_radius=2)
        pygame.draw.rect(surf, hat_color,
                         (hx - int(14*s), hy - int(9*s),
                          int(28*s), int(4*s)), border_radius=1)

    # Рожи врага
    if enemy:
        # Злые брови
        pygame.draw.line(surf, BLACK,
                         (head_c[0]+ex-4, head_c[1]-6),
                         (head_c[0]+ex+3, head_c[1]-4), lw)
        # Рот
        pygame.draw.arc(surf, BLACK,
                        (head_c[0]-6, head_c[1], 12, 8),
                        math.pi*0.1, math.pi*0.9, lw)

# ── Платформы ────────────────────────────────────────────────────────────────

class Platform:
    def __init__(self, x, y, w, h=18, moving=False, move_range=80, color=None):
        self.rect     = pygame.Rect(x, y, w, h)
        self.moving   = moving
        self.move_dir = 1
        self.move_range = move_range
        self.start_x  = x
        self.color    = color or PLAT_C

    def update(self):
        if self.moving:
            self.rect.x += self.move_dir * 1.5
            if abs(self.rect.x - self.start_x) > self.move_range:
                self.move_dir *= -1

    def draw(self, surf, cam_x):
        rx = self.rect.x - cam_x
        pygame.draw.rect(surf, self.color,
                         (rx, self.rect.y, self.rect.w, self.rect.h),
                         border_radius=6)
        pygame.draw.rect(surf, PLAT_TOP,
                         (rx, self.rect.y, self.rect.w, 5),
                         border_radius=6)
        # Трава
        for i in range(0, self.rect.w, 12):
            gx = rx + i + 4
            gy = self.rect.y
            pygame.draw.line(surf, DARK_GREEN,
                             (gx, gy), (gx - 3, gy - 6), 2)
            pygame.draw.line(surf, DARK_GREEN,
                             (gx, gy), (gx + 3, gy - 7), 2)

# ── Монета ───────────────────────────────────────────────────────────────────

class Coin:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.collected = False
        self.t = random.randint(0, 100)

    def update(self):
        self.t += 1

    def draw(self, surf, cam_x):
        if self.collected: return
        bob = math.sin(self.t * 0.1) * 4
        cx, cy = int(self.x - cam_x), int(self.y + bob)
        pygame.draw.circle(surf, GOLD, (cx, cy), 10)
        pygame.draw.circle(surf, YELLOW, (cx, cy), 7)
        s = font.render("$", True, ORANGE)
        surf.blit(s, (cx - s.get_width()//2, cy - s.get_height()//2))

# ── Враг ─────────────────────────────────────────────────────────────────────

class Enemy:
    SPEED = 1.5

    def __init__(self, x, y, patrol=120):
        self.x, self.y  = float(x), float(y)
        self.vy         = 0
        self.start_x    = x
        self.patrol     = patrol
        self.dir        = 1
        self.walk_t     = 0
        self.alive      = True
        self.die_t      = 0
        self.on_ground  = False

    def update(self, platforms):
        if not self.alive:
            self.die_t += 1
            return

        self.vy += GRAVITY
        self.x += self.dir * self.SPEED
        self.y += self.vy

        if abs(self.x - self.start_x) > self.patrol:
            self.dir *= -1

        # Колизия с платформами
        self.on_ground = False
        er = pygame.Rect(int(self.x)-14, int(self.y)-50, 28, 55)
        for p in platforms:
            if er.colliderect(p.rect) and self.vy >= 0:
                self.y = p.rect.top
                self.vy = 0
                self.on_ground = True

        self.walk_t += 1 if self.alive else 0

    def draw(self, surf, cam_x):
        if not self.alive:
            if self.die_t < 40:
                angle = self.die_t * 4
                draw_stickman(surf, self.x - cam_x, self.y,
                              RED, 1.0, 0, self.dir,
                              is_dead=True, dead_angle=angle)
            return
        draw_stickman(surf, self.x - cam_x, self.y,
                      RED, 1.0, self.walk_t, self.dir, enemy=True)

# ── Частицы ──────────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = random.randint(20, 40)
        self.color = color
        self.size  = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self, surf, cam_x):
        if self.life > 0:
            alpha = max(0, self.life * 6)
            r = max(1, self.size * self.life // 30)
            pygame.draw.circle(surf, self.color,
                               (int(self.x - cam_x), int(self.y)), r)

# ── Игрок ────────────────────────────────────────────────────────────────────

class Player:
    def __init__(self, x, y):
        self.x, self.y  = float(x), float(y)
        self.vx, self.vy = 0.0, 0.0
        self.on_ground  = False
        self.facing     = 1
        self.walk_t     = 0
        self.alive      = True
        self.die_t      = 0
        self.jumps_left = 2   # двойной прыжок

    def jump(self):
        if self.jumps_left > 0:
            self.vy = JUMP_FORCE
            self.jumps_left -= 1

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if self.alive:
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.vx = -PLAYER_SPEED; self.facing = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx =  PLAYER_SPEED; self.facing =  1

        self.vy += GRAVITY
        self.x  += self.vx
        self.y  += self.vy

        # Пол уровня
        if self.y > HEIGHT + 100:
            self.alive = False

        self.on_ground = False
        pr = pygame.Rect(int(self.x)-14, int(self.y)-55, 28, 60)
        for p in platforms:
            if pr.colliderect(p.rect):
                if self.vy >= 0 and self.y - 55 < p.rect.top + 10:
                    self.y = p.rect.top
                    self.vy = 0
                    self.on_ground = True
                    self.jumps_left = 2

        if self.vx != 0 and self.on_ground:
            self.walk_t += 1
        elif not self.on_ground:
            self.walk_t += 0.5

        if not self.alive:
            self.die_t += 1

    def draw(self, surf, cam_x):
        sx = self.x - cam_x
        if not self.alive:
            if self.die_t < 50:
                angle = 90 + self.die_t * 3
                draw_stickman(surf, sx, self.y, BLACK, 1.1, 0,
                              self.facing, is_dead=True, dead_angle=angle)
            return
        draw_stickman(surf, sx, self.y, BLACK, 1.1,
                      self.walk_t, self.facing, hat_color=BLUE)

# ── Уровни ───────────────────────────────────────────────────────────────────

def make_level(num):
    platforms = []
    coins     = []
    enemies   = []

    # Земля (несколько секций)
    gw = 220
    for i in range(18):
        platforms.append(Platform(i * gw, HEIGHT - 40, gw + 4, 40, color=GROUND_C))

    if num == 1:
        data = [
            (300, 400, 140), (500, 320, 120), (700, 260, 100),
            (900, 340, 160, True), (1100, 280, 120),
            (1300, 200, 100), (1500, 310, 140, True),
            (1700, 240, 120), (1900, 170, 100),
            (200, 300, 100), (400, 220, 80),
        ]
        enemy_data = [
            (500, HEIGHT-100, 100), (900, HEIGHT-100, 80),
            (1300, HEIGHT-100, 120), (1700, HEIGHT-100, 90),
        ]
        coin_data = [
            (350, 370), (520, 290), (720, 230), (950, 310),
            (1150, 250), (1350, 170), (1550, 280),
            (1750, 210), (1950, 140),
            (250, 270), (450, 190),
        ]
    else:
        data = [
            (250, 380, 100, True, 60), (450, 300, 80), (620, 350, 120, True),
            (800, 260, 90), (1000, 200, 80), (1200, 280, 140, True, 100),
            (1400, 200, 80), (1600, 140, 80), (1800, 220, 120, True),
            (2000, 160, 80), (150, 320, 80),
        ]
        enemy_data = [
            (450, HEIGHT-100, 80), (800, HEIGHT-100, 60),
            (1200, HEIGHT-100, 100), (1600, HEIGHT-100, 70),
            (2000, HEIGHT-100, 90),
        ]
        coin_data = [
            (280, 350), (470, 270), (650, 320), (820, 230),
            (1020, 170), (1230, 250), (1420, 170), (1620, 110),
            (1820, 190), (2020, 130), (180, 290),
        ]

    for d in data:
        moving = len(d) > 3 and d[3]
        mr = d[4] if len(d) > 4 else 80
        platforms.append(Platform(d[0], d[1], d[2],
                                  moving=moving, move_range=mr))
    for ex, ey, ep in enemy_data:
        enemies.append(Enemy(ex, ey, ep))
    for cx, cy in coin_data:
        coins.append(Coin(cx, cy))

    return platforms, coins, enemies

# ── Главный класс игры ───────────────────────────────────────────────────────

class Game:
    def __init__(self):
        self.level   = 1
        self.score   = 0
        self.tick    = 0
        self.state   = "menu"   # menu / playing / dead / win / next_level
        self.particles = []
        self.cam_x   = 0
        self._load_level()

    def _load_level(self):
        self.platforms, self.coins, self.enemies = make_level(self.level)
        self.player    = Player(100, HEIGHT - 120)
        self.cam_x     = 0
        self.particles = []
        self.state     = "playing"
        self.msg_t     = 0
        self.total_coins = len(self.coins)

    def spawn_particles(self, x, y, color, n=12):
        for _ in range(n):
            self.particles.append(Particle(x, y, color))

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if e.key == pygame.K_SPACE:
                        self.state = "playing"
                elif self.state == "playing":
                    if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.player.jump()
                elif self.state in ("dead", "win", "next_level"):
                    if e.key == pygame.K_SPACE:
                        if self.state == "dead":
                            self.score = 0
                            self.level = 1
                            self._load_level()
                        elif self.state == "next_level":
                            self.level += 1
                            self._load_level()
                        elif self.state == "win":
                            self.score = 0
                            self.level = 1
                            self._load_level()

    def update(self):
        self.tick += 1
        if self.state != "playing":
            self.msg_t += 1
            return

        for p in self.platforms:
            p.update()

        self.player.update(self.platforms)

        # Камера
        target_cam = self.player.x - WIDTH // 3
        self.cam_x += (target_cam - self.cam_x) * 0.1

        # Монеты
        pr = pygame.Rect(int(self.player.x)-14, int(self.player.y)-55, 28, 60)
        for c in self.coins:
            if not c.collected:
                cr = pygame.Rect(int(c.x)-10, int(c.y)-10, 20, 20)
                if pr.colliderect(cr):
                    c.collected = True
                    self.score += 10
                    self.spawn_particles(c.x, c.y, GOLD)
            c.update()

        # Враги
        for en in self.enemies:
            en.update(self.platforms)
            if not en.alive: continue
            er = pygame.Rect(int(en.x)-14, int(en.y)-50, 28, 55)
            if pr.colliderect(er) and self.player.alive:
                # Прыжок на голову?
                if self.player.vy > 1 and self.player.y < en.y - 20:
                    en.alive = False
                    self.player.vy = JUMP_FORCE * 0.7
                    self.score += 25
                    self.spawn_particles(en.x, en.y, RED, 16)
                else:
                    self.player.alive = False
                    self.spawn_particles(self.player.x, self.player.y, BLUE, 20)

        # Частицы
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # Смерть
        if not self.player.alive and self.player.die_t > 50:
            self.state = "dead"
            self.msg_t = 0

        # Все монеты собраны?
        if all(c.collected for c in self.coins) and self.player.alive:
            if self.level < 2:
                self.state = "next_level"
            else:
                self.state = "win"
            self.msg_t = 0

    def draw_bg(self):
        # ── Красивый закатный градиент неба ──
        sky_colors = [
            (255, 100,  50),   # горизонт — оранжево-красный
            (255, 160,  80),   # тёплый оранжевый
            (255, 200, 120),   # жёлто-оранжевый
            (180, 120, 220),   # фиолетовый
            ( 80,  60, 160),   # тёмно-синий
            ( 30,  20,  80),   # ночной синий (верх)
        ]
        band = HEIGHT // (len(sky_colors) - 1)
        for y in range(HEIGHT):
            seg = min(y // band, len(sky_colors) - 2)
            t   = (y - seg * band) / band
            c1, c2 = sky_colors[seg], sky_colors[seg + 1]
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # ── Солнце / закатный диск ──
        sun_x = WIDTH * 3 // 4
        sun_y = HEIGHT // 2 - 20
        for ring in range(40, 0, -5):
            alpha = ring * 3
            col = (min(255, 255), min(255, 200 - ring*2), max(0, 50 - ring*2))
            pygame.draw.circle(screen, col, (sun_x, sun_y), ring)
        pygame.draw.circle(screen, (255, 255, 180), (sun_x, sun_y), 28)
        # Лучи солнца
        for a in range(0, 360, 30):
            rad = math.radians(a + self.tick * 0.3)
            x1 = sun_x + int(math.cos(rad) * 35)
            y1 = sun_y + int(math.sin(rad) * 35)
            x2 = sun_x + int(math.cos(rad) * 55)
            y2 = sun_y + int(math.sin(rad) * 55)
            pygame.draw.line(screen, (255, 220, 100), (x1, y1), (x2, y2), 2)

        # ── Звёзды (вверху) ──
        random.seed(42)
        for _ in range(60):
            sx = random.randint(0, WIDTH)
            sy = random.randint(0, HEIGHT // 3)
            blink = int(180 + 75 * math.sin(self.tick * 0.05 + sx))
            pygame.draw.circle(screen, (blink, blink, blink), (sx, sy), 1)
        random.seed()

        # ── Дальние горы (слой 1, медленный параллакс) ──
        W_TILE = 600
        for i in range(-1, WIDTH // W_TILE + 3):
            ox = int((i * W_TILE - self.cam_x * 0.12) % (W_TILE * 8)) - W_TILE
            pts = []
            peaks = [(0, 180),(80, 80),(160, 130),(240, 60),
                     (320, 110),(400, 50),(480, 100),(560, 140),(600, 180)]
            for px, py in peaks:
                pts.append((ox + px, HEIGHT - py))
            pts.append((ox + 600, HEIGHT))
            pts.append((ox, HEIGHT))
            pygame.draw.polygon(screen, (100, 60, 120), pts)
            # Снежные шапки
            for px, py in peaks[1:-1]:
                if py < 100:
                    cap = [(ox+px-18, HEIGHT-py+12),(ox+px, HEIGHT-py-5),(ox+px+18, HEIGHT-py+12)]
                    pygame.draw.polygon(screen, (230, 220, 240), cap)

        # ── Средние горы (слой 2) ──
        W2 = 500
        for i in range(-1, WIDTH // W2 + 3):
            ox = int((i * W2 - self.cam_x * 0.25) % (W2 * 7)) - W2
            pts = []
            shape = [(0,120),(70,50),(140,90),(210,30),(280,70),(360,20),(430,60),(500,120)]
            for px, py in shape:
                pts.append((ox+px, HEIGHT - py))
            pts.append((ox+500, HEIGHT)); pts.append((ox, HEIGHT))
            pygame.draw.polygon(screen, (60, 80, 100), pts)

        # ── Лес на заднем плане (параллакс 0.4) ──
        tree_spacing = 45
        tree_count   = WIDTH // tree_spacing + 6
        for i in range(tree_count):
            tx = int((i * tree_spacing - self.cam_x * 0.4) % (tree_spacing * (tree_count + 4)))
            ty = HEIGHT - 90
            h  = 55 + (i * 17 % 30)
            # Ствол
            pygame.draw.rect(screen, (60, 35, 15), (tx - 4, ty, 8, 35))
            # Крона (3 треугольника)
            for layer, (lh, lw) in enumerate([(h, 28), (h+18, 22), (h+32, 16)]):
                tri = [(tx, ty - lh), (tx - lw, ty - lh + 28), (tx + lw, ty - lh + 28)]
                col = (20 + layer*10, 80 + layer*15, 20 + layer*8)
                pygame.draw.polygon(screen, col, tri)

        # ── Облака (параллакс 0.15, объёмные) ──
        cloud_data = [
            (0,   80, 1.2), (350, 55, 0.9), (700, 95, 1.4),
            (150, 120, 0.7),(520, 70, 1.1), (900, 105, 0.8),
            (1100, 60, 1.3),(1400, 90, 1.0),(1700, 50, 1.5),
        ]
        for cx0, cy0, sc in cloud_data:
            cx = int((cx0 - self.cam_x * 0.15) % (WIDTH * 2.5))
            # Несколько эллипсов = пышное облако
            for ox, oy, ow, oh in [
                (0,  10, int(90*sc), int(35*sc)),
                (-int(28*sc), 20, int(65*sc), int(30*sc)),
                ( int(28*sc), 20, int(65*sc), int(30*sc)),
                (-int(10*sc),  0, int(50*sc), int(25*sc)),
            ]:
                col = (255, 240, 220) if cy0 > 80 else (255, 255, 255)
                pygame.draw.ellipse(screen, col, (cx+ox, cy0+oy, ow, oh))

        # ── Отражение заката на земле (туман у горизонта) ──
        fog = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
        for fy in range(60):
            a = int(80 * (1 - fy / 60))
            pygame.draw.line(fog, (255, 140, 60, a), (0, fy), (WIDTH, fy))
        screen.blit(fog, (0, HEIGHT - 120))

    def draw_hud(self):
        # Панель
        pygame.draw.rect(screen, (0,0,0,120), (0, 0, WIDTH, 48))
        pygame.draw.line(screen, GOLD, (0, 48), (WIDTH, 48), 2)

        sc = font.render(f"СЧЁТ: {self.score}", True, YELLOW)
        screen.blit(sc, (20, 12))

        lv = font.render(f"УРОВЕНЬ: {self.level}/2", True, WHITE)
        screen.blit(lv, (WIDTH//2 - lv.get_width()//2, 12))

        collected = sum(1 for c in self.coins if c.collected)
        cn = font.render(f"🪙 {collected}/{self.total_coins}", True, GOLD)
        screen.blit(cn, (WIDTH - cn.get_width() - 20, 12))

        # Подсказка управления
        hint = pygame.font.SysFont("monospace", 14).render(
            "← → или A D  |  SPACE / W / ↑ — прыжок (двойной!)", True, GREY)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 22))

    def draw_overlay(self, text_lines, sub="SPACE — продолжить"):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        screen.blit(ov, (0, 0))
        total = len(text_lines)
        for i, (txt, col, fnt) in enumerate(text_lines):
            s = fnt.render(txt, True, col)
            y = HEIGHT//2 - (total * 55)//2 + i * 60
            screen.blit(s, (WIDTH//2 - s.get_width()//2, y))
        if self.msg_t > 40:
            sub_s = font.render(sub, True, WHITE)
            screen.blit(sub_s, (WIDTH//2 - sub_s.get_width()//2, HEIGHT//2 + 80))

    def run(self):
        while True:
            self.handle_events()
            self.update()

            # ── Отрисовка ──
            self.draw_bg()

            for p in self.platforms:
                p.draw(screen, self.cam_x)

            for c in self.coins:
                c.draw(screen, self.cam_x)

            for en in self.enemies:
                en.draw(screen, self.cam_x)

            for pt in self.particles:
                pt.draw(screen, self.cam_x)

            self.player.draw(screen, self.cam_x)

            self.draw_hud()

            # Оверлеи
            if self.state == "menu":
                self.draw_overlay([
                    ("STICKMAN",       YELLOW, font_big),
                    ("ADVENTURE",      WHITE,  font_big),
                    ("Собери все монеты!", GOLD, font_med),
                    ("Прыгни на врага — убьёшь его!", GREY, font),
                ], "SPACE — начать")

            elif self.state == "dead":
                self.draw_overlay([
                    ("ТЫ ПОГИБ", RED,    font_big),
                    (f"Счёт: {self.score}", YELLOW, font_med),
                ], "SPACE — заново")

            elif self.state == "next_level":
                self.draw_overlay([
                    ("УРОВЕНЬ ПРОЙДЕН!", YELLOW, font_big),
                    (f"Счёт: {self.score}", GOLD,   font_med),
                    ("Следующий уровень сложнее!", WHITE, font),
                ])

            elif self.state == "win":
                self.draw_overlay([
                    ("ПОБЕДА! 🎉",      YELLOW, font_big),
                    (f"Финальный счёт: {self.score}", GOLD, font_med),
                    ("Ты собрал все монеты!", WHITE, font),
                ], "SPACE — заново")

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    Game().run()
