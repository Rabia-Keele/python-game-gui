#!/usr/bin/env python3
# Dodge the Blocks - Enhanced Version

import tkinter as tk
import random
import time
import os

WIDTH, HEIGHT = 500, 600
PLAYER_W, PLAYER_H = 50, 20
BLOCK_W, BLOCK_H = 40, 20
SPAWN_EVERY_MS = 900
TICK_MS = 16  # ~60 FPS

HIGHSCORE_FILE = "highscore.txt"

# ---------- Block Class ----------
class Block:
    COLORS = ["#444", "#f00", "#0f0"]  # normal, fast, bonus
    SPEEDS = [3, 6, 4]
    POINTS = [1, 1, 5]

    def __init__(self, canvas):
        self.type = random.randint(0, 2)
        self.speed = self.SPEEDS[self.type]
        self.points = self.POINTS[self.type]
        self.canvas = canvas
        self.x = random.randint(0, WIDTH - BLOCK_W)
        self.y = -BLOCK_H
        self.id = canvas.create_rectangle(
            self.x, self.y, self.x + BLOCK_W, self.y + BLOCK_H,
            outline="", fill=self.COLORS[self.type]
        )

    def step(self):
        self.y += self.speed
        self.canvas.move(self.id, 0, self.speed)

    def offscreen(self):
        return self.y > HEIGHT + BLOCK_H

    def bbox(self):
        return self.canvas.bbox(self.id)

# ---------- Game Class ----------
class Game:
    def __init__(self, root):
        self.root = root
        root.title("Dodge the Blocks")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#f5f5f5", highlightthickness=0)
        self.canvas.pack()

        # Info Text
        self.info = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Arial", 12))

        # Player
        self.player = self.canvas.create_rectangle(
            WIDTH//2-PLAYER_W//2, HEIGHT-60, WIDTH//2+PLAYER_W//2, HEIGHT-60+PLAYER_H,
            outline="", fill="#2d6cdf"
        )

        self.dx = 0
        self.blocks = []
        self.running = True
        self.score = 0
        self.best = self.load_highscore()
        self.last_spawn_t = time.time()

        # Controls
        root.bind("<KeyPress-Left>", lambda e: self.set_dx(-6))
        root.bind("<KeyPress-Right>", lambda e: self.set_dx(6))
        root.bind("<KeyRelease-Left>", lambda e: self.stop_dx(-6))
        root.bind("<KeyRelease-Right>", lambda e: self.stop_dx(6))
        root.bind("<space>", self.try_restart)

        self.loop()

    # ---------- Player Controls ----------
    def set_dx(self, v):
        self.dx = v
    def stop_dx(self, v):
        if self.dx == v:
            self.dx = 0

    # ---------- Restart ----------
    def try_restart(self, _evt=None):
        if not self.running:
            self.reset()

    def reset(self):
        for b in self.blocks:
            self.canvas.delete(b.id)
        self.blocks.clear()
        self.canvas.coords(self.player, WIDTH//2-PLAYER_W//2, HEIGHT-60, WIDTH//2+PLAYER_W//2, HEIGHT-60+PLAYER_H)
        self.dx = 0
        self.running = True
        self.score = 0
        self.last_spawn_t = time.time()
        self.canvas.itemconfig(self.info, text="")

    # ---------- Spawn & Move ----------
    def spawn_block(self):
        self.blocks.append(Block(self.canvas))

    def move_player(self):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        nx1 = max(0, min(WIDTH-PLAYER_W, x1 + self.dx))
        self.canvas.coords(self.player, nx1, y1, nx1+PLAYER_W, y2)

    # ---------- Collision ----------
    def intersects(self, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

    def check_collision(self):
        pbox = self.canvas.bbox(self.player)
        for b in self.blocks:
            if self.intersects(pbox, b.bbox()):
                if b.type == 2:  # Bonus block
                    self.score += b.points
                    self.canvas.delete(b.id)
                    self.blocks.remove(b)
                else:
                    return True
        return False

    # ---------- Highscore ----------
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        return 0

    def save_highscore(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.best))

    # ---------- Main Loop ----------
    def loop(self):
        if self.running:
            # spawn blocks
            now = time.time()
            if (now - self.last_spawn_t) * 1000 >= SPAWN_EVERY_MS:
                self.spawn_block()
                self.last_spawn_t = now

            # update blocks
            for b in list(self.blocks):
                b.step()
                if b.offscreen():
                    self.canvas.delete(b.id)
                    self.blocks.remove(b)
                    self.score += b.points

            # move player
            self.move_player()

            # collision
            if self.check_collision():
                self.running = False
                self.best = max(self.best, self.score)
                self.save_highscore()
                self.canvas.itemconfig(self.info, text=f"Game Over • Score {self.score} • Best {self.best}\nPress SPACE to restart")

        # HUD
        if self.running:
            self.canvas.itemconfig(self.info, text=f"Score: {self.score} • Best: {self.best}")

        self.root.after(TICK_MS, self.loop)

# ---------- Main ----------
def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
