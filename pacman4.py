import pygame
import sys
import math
import random

# ── Константы ──────────────────────────────────────────────────────────────
CELL   = 32
COLS   = 19
ROWS   = 21
WIDTH  = COLS * CELL          # 608
PANEL  = 50
HEIGHT = ROWS * CELL + PANEL  # 722
FPS    = 60

# Цвета
BLACK   = (0,   0,   0)
YELLOW  = (0,   210,  60)
DKYELLOW= (0,   150,  40)
BLUE    = (20,  20, 200)
LBLUE   = (100, 140, 255)
WHITE   = (255, 255, 255)
RED     = (220,  30,  30)
PINK    = (255, 150, 180)
CYAN    = (0,   220, 220)
ORANGE  = (255, 160,  30)
DARK    = (180,  0,   0)
GREY    = (120, 120, 120)
WALL_C  = (255, 140,  0)
WALL_HL = (255, 200, 80)
DOT_C   = (255, 210, 130)
POW_C   = (255, 255, 200)
FRIGHT  = (20,  20, 180)

# ── Лабиринт 21×19 ─────────────────────────────────────────────────────────
# 1=стена  0=точка  2=пусто  3=энергизатор  4=дверь дома призраков
RAW = [
    "1111111111111111111",
    "1000000001000000001",
    "1011101101101110101",
    "1000000000000000001",
    "1011010111101101101",
    "1000010000001000001",
    "1111010111101011111",
    "2220100000001002222",
    "1111014444410111111",
    "0000002422200000000",
    "1111014444410111111",
    "2222002000002002222",
    "1111010111101011111",
    "1000010000001000001",
    "1011010111101101101",
    "1000100010001000001",
    "1011011111111011101",
    "1000000001000000001",
    "1011111101101111101",
    "1000000000000000001",
    "1111111111111111111",
]

ENERGIZERS = {(2,1),(2,17),(17,1),(17,17)}

def build_grid():
    g = []
    for r, row in enumerate(RAW):
        line = []
        for c, ch in enumerate(row):
            if (r, c) in ENERGIZERS:
                line.append(3)
            else:
                line.append(int(ch))
        g.append(line)
    return g

def is_wall(grid, col, row):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return True
    return grid[row][col] == 1

def cell_px(col, row):
    return col * CELL + CELL // 2, row * CELL + CELL // 2 + PANEL

# ── Pac-Man ─────────────────────────────────────────────────────────────────

class Pacman:
    SPEED = 3

    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.x, self.y = cell_px(col, row)
        self.dx = 0
        self.dy = 0
        self.want_dx = 1   # сразу вправо при старте
        self.want_dy = 0
        self.mouth   = 5
        self.mdir    = 1
        self.alive   = True
        self.die_t   = 0

    def set_dir(self, dx, dy):
        self.want_dx = dx
        self.want_dy = dy

    def update(self, grid):
        if not self.alive:
            self.die_t += 1
            return

        cx, cy = cell_px(self.col, self.row)
        on_cx = abs(self.x - cx) < self.SPEED
        on_cy = abs(self.y - cy) < self.SPEED

        if on_cx and on_cy:
            self.x, self.y = cx, cy

            # Попытка сменить направление
            nc = self.col + self.want_dx
            nr = self.row + self.want_dy
            if not is_wall(grid, nc, nr):
                self.dx = self.want_dx
                self.dy = self.want_dy

            # Шаг к следующему тайлу
            nc = self.col + self.dx
            nr = self.row + self.dy
            if not is_wall(grid, nc, nr):
                self.col = nc
                self.row = nr

        # Плавное движение к центру целевого тайла
        tx, ty = cell_px(self.col, self.row)
        def mv(pos, t):
            d = t - pos
            if abs(d) <= self.SPEED: return t
            return pos + self.SPEED * (1 if d > 0 else -1)
        self.x = mv(self.x, tx)
        self.y = mv(self.y, ty)

        # Тоннель
        if self.col < 0:
            self.col = COLS - 1
            self.x = cell_px(self.col, self.row)[0]
        if self.col >= COLS:
            self.col = 0
            self.x = cell_px(self.col, self.row)[0]

        # Анимация рта
        self.mouth += 3 * self.mdir
        if self.mouth >= 40: self.mdir = -1
        if self.mouth <= 2:  self.mdir =  1

    def eat(self, grid):
        v = grid[self.row][self.col]
        if v in (0, 3):
            grid[self.row][self.col] = 2
            return v
        return None

    def draw(self, surf):
        x, y = int(self.x), int(self.y)
        R = CELL // 2 - 3

        if not self.alive:
            frac = min(self.die_t / 40, 1.0)
            gap  = int(frac * 180)
            if gap < 180:
                pts = [(x, y)]
                for a in range(gap, 360 - gap + 1, 4):
                    rad = math.radians(a)
                    pts.append((x + R*math.cos(rad), y + R*math.sin(rad)))
                if len(pts) >= 3:
                    pygame.draw.polygon(surf, YELLOW, pts)
            return

        dir_angle = {(1,0):0, (-1,0):180, (0,-1):90, (0,1):270, (0,0):0}
        base = dir_angle.get((self.dx, self.dy), 0)
        a0 = base + self.mouth
        a1 = base + 360 - self.mouth
        pts = [(x, y)]
        for i in range(37):
            a = math.radians(a0 + (a1 - a0) * i / 36)
            pts.append((x + R*math.cos(a), y + R*math.sin(a)))
        if len(pts) >= 3:
            pygame.draw.polygon(surf, YELLOW, pts)

# ── Призрак ─────────────────────────────────────────────────────────────────

GHOST_COLORS = [RED, PINK, CYAN, ORANGE]

class Ghost:
    SPEED  = 2
    FTICKS = FPS * 7

    def __init__(self, col, row, color, idx):
        self.col = col
        self.row = row
        self.x, self.y = cell_px(col, row)
        self.dx = random.choice([-1, 1])
        self.dy = 0
        self.color  = color
        self.idx    = idx
        self.fright = 0
        self.eaten  = False

    def frighten(self):
        self.fright = self.FTICKS
        self.eaten  = False

    def _can(self, grid, dc, dr):
        nc, nr = self.col + dc, self.row + dr
        if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS: return False
        v = grid[nr][nc]
        if v == 1: return False
        if v == 4 and self.eaten: return False
        return True

    def update(self, grid, pac_col, pac_row):
        if self.fright > 0:
            self.fright -= 1

        cx, cy = cell_px(self.col, self.row)
        on_cx = abs(self.x - cx) < self.SPEED
        on_cy = abs(self.y - cy) < self.SPEED

        if on_cx and on_cy:
            self.x, self.y = cx, cy
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            no_back = [d for d in dirs if d != (-self.dx, -self.dy) and self._can(grid, *d)]
            if not no_back:
                no_back = [d for d in dirs if self._can(grid, *d)]
            if no_back:
                if not self.fright and not self.eaten and random.random() < 0.6:
                    no_back.sort(key=lambda d:
                        (self.col+d[0]-pac_col)**2 + (self.row+d[1]-pac_row)**2)
                else:
                    random.shuffle(no_back)
                self.dx, self.dy = no_back[0]

            if self._can(grid, self.dx, self.dy):
                self.col += self.dx
                self.row += self.dy

        tx, ty = cell_px(self.col, self.row)
        def mv(pos, t):
            d = t - pos
            if abs(d) <= self.SPEED: return t
            return pos + self.SPEED * (1 if d > 0 else -1)
        self.x = mv(self.x, tx)
        self.y = mv(self.y, ty)

        if self.col < 0:
            self.col = COLS-1
            self.x = cell_px(self.col, self.row)[0]
        if self.col >= COLS:
            self.col = 0
            self.x = cell_px(self.col, self.row)[0]

    def draw(self, surf, tick):
        x, y = int(self.x), int(self.y)
        R = CELL//2 - 2

        if self.eaten:
            for ox in (-5, 5):
                pygame.draw.circle(surf, WHITE, (x+ox, y-3), 4)
                pygame.draw.circle(surf, BLUE,  (x+ox, y-3), 2)
            return

        col = self.color
        if self.fright > 0:
            blink = self.fright < FPS*2 and (tick//8)%2 == 0
            col = WHITE if blink else FRIGHT

        pygame.draw.ellipse(surf, col, (x-R, y-R, R*2, R*2))
        pygame.draw.rect(surf, col, (x-R, y, R*2, R))

        teeth = 4
        w = R*2 // teeth
        for i in range(teeth):
            bx = x - R + i * w
            pts = [(bx, y+R), (bx+w//2, y+R-5), (bx+w, y+R)]
            pygame.draw.polygon(surf, DARK, pts)

        if self.fright == 0:
            for ox in (-4, 4):
                pygame.draw.circle(surf, WHITE, (x+ox, y-3), 4)
                pygame.draw.circle(surf, BLUE,  (x+ox+self.dx, y-3+self.dy), 2)
        else:
            pygame.draw.line(surf, WHITE, (x-5, y+1), (x-2, y+4), 2)
            pygame.draw.line(surf, WHITE, (x-2, y+4), (x+2, y+1), 2)
            pygame.draw.line(surf, WHITE, (x+2, y+1), (x+5, y+4), 2)

# ── Игра ─────────────────────────────────────────────────────────────────────

class Game:
    PAC_START   = (9, 15)
    GHOST_START = [(8,9),(9,9),(10,9),(9,10)]

    def __init__(self):
        pygame.init()
        self.screen   = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PAC-MAN")
        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_big = pygame.font.SysFont("monospace", 44, bold=True)
        self.reset()

    def reset(self):
        self.grid      = build_grid()
        self.pac       = Pacman(*self.PAC_START)
        self.ghosts    = [Ghost(c, r, GHOST_COLORS[i], i)
                          for i,(c,r) in enumerate(self.GHOST_START)]
        self.score     = 0
        self.lives     = 3
        self.dots_left = sum(1 for row in self.grid for v in row if v in (0,3))
        self.state     = "playing"
        self.tick      = 0
        self.pause_t   = 0

    def _respawn(self):
        if self.lives <= 0:
            self.state = "gameover"; return
        self.pac = Pacman(*self.PAC_START)
        for g in self.ghosts:
            c, r = self.GHOST_START[g.idx]
            g.col, g.row = c, r
            g.x, g.y = cell_px(c, r)
            g.dx, g.dy = 1, 0
            g.fright = 0
            g.eaten  = False
        self.state = "playing"

    def handle_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if self.state in ("win","gameover"):
                    if e.key == pygame.K_SPACE: self.reset()
                    return
                if self.state == "dead":
                    if self.pause_t <= 0: self._respawn()
                    return
                k = e.key
                if   k in (pygame.K_LEFT,  pygame.K_a): self.pac.set_dir(-1, 0)
                elif k in (pygame.K_RIGHT, pygame.K_d): self.pac.set_dir( 1, 0)
                elif k in (pygame.K_UP,    pygame.K_w): self.pac.set_dir( 0,-1)
                elif k in (pygame.K_DOWN,  pygame.K_s): self.pac.set_dir( 0, 1)

    def update(self):
        if self.state != "playing":
            if self.pause_t > 0: self.pause_t -= 1
            return

        self.tick += 1
        self.pac.update(self.grid)

        v = self.pac.eat(self.grid)
        if v == 0:
            self.score += 10;  self.dots_left -= 1
        elif v == 3:
            self.score += 50;  self.dots_left -= 1
            for g in self.ghosts: g.frighten()

        if self.dots_left <= 0:
            self.state = "win"; return

        for g in self.ghosts:
            g.update(self.grid, self.pac.col, self.pac.row)

        for g in self.ghosts:
            dist = math.hypot(self.pac.x - g.x, self.pac.y - g.y)
            if dist < CELL - 6:
                if g.fright and not g.eaten:
                    g.eaten = True; self.score += 200
                elif not g.eaten and self.pac.alive:
                    self.pac.alive = False
                    self.lives    -= 1
                    self.state     = "dead"
                    self.pause_t   = FPS * 2
                    return

    def draw_maze(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL
                y = row * CELL + PANEL
                v = self.grid[row][col]
                if v == 1:
                    r = pygame.Rect(x+1, y+1, CELL-2, CELL-2)
                    pygame.draw.rect(self.screen, WALL_C,  r, border_radius=5)
                    pygame.draw.rect(self.screen, WALL_HL, r, 1, border_radius=5)
                elif v == 0:
                    pygame.draw.circle(self.screen, DOT_C,
                                       (x+CELL//2, y+CELL//2), 3)
                elif v == 3:
                    pulse = 6 + int(3*math.sin(self.tick * 0.08))
                    pygame.draw.circle(self.screen, POW_C,
                                       (x+CELL//2, y+CELL//2), pulse)
                    pygame.draw.circle(self.screen, YELLOW,
                                       (x+CELL//2, y+CELL//2), pulse-3)
                elif v == 4:
                    pygame.draw.rect(self.screen, (80,80,160),
                                     (x, y+CELL//2-2, CELL, 4))

    def draw_hud(self):
        self.screen.fill(BLACK, (0, 0, WIDTH, PANEL))
        pygame.draw.line(self.screen, WALL_C, (0, PANEL-2), (WIDTH, PANEL-2), 2)
        sc = self.font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(sc, (10, 14))
        lbl = self.font.render("LIVES:", True, GREY)
        self.screen.blit(lbl, (WIDTH-170, 14))
        for i in range(self.lives):
            pygame.draw.circle(self.screen, YELLOW,   (WIDTH-50+i*0-i*26, 25), 10)
            pygame.draw.circle(self.screen, DKYELLOW, (WIDTH-50+i*0-i*26, 25), 10, 2)

    def draw_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        if self.state == "dead":
            overlay.fill((0,0,0,120))
            self.screen.blit(overlay, (0,0))
            msg = "ОЙ!" if self.pause_t > 0 else "Нажми любую клавишу"
            s = self.font_big.render(msg, True, RED)
            self.screen.blit(s, (WIDTH//2-s.get_width()//2, HEIGHT//2-25))
        elif self.state in ("win", "gameover"):
            overlay.fill((0,0,0,160))
            self.screen.blit(overlay, (0,0))
            if self.state == "win":
                s1 = self.font_big.render("ПОБЕДА!", True, YELLOW)
            else:
                s1 = self.font_big.render("GAME OVER", True, RED)
            s2 = self.font.render(f"Счёт: {self.score}     [SPACE] — заново", True, WHITE)
            self.screen.blit(s1, (WIDTH//2-s1.get_width()//2, HEIGHT//2-40))
            self.screen.blit(s2, (WIDTH//2-s2.get_width()//2, HEIGHT//2+20))

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.screen.fill(DARK)
            self.draw_maze()
            self.draw_hud()
            for g in self.ghosts:
                g.draw(self.screen, self.tick)
            self.pac.draw(self.screen)
            self.draw_overlay()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()
