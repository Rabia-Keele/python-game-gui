import tkinter as tk
import random

# CONFIG
WIDTH, HEIGHT = 480, 700
PLAYER_W, PLAYER_H = 60, 20
BLOCK_W, BLOCK_H = 50, 20
SPAWN_INTERVAL = 1000  # ms
MOVE_SPEED = 7

COLORS = {
    "bg_top": "#081C24",
    "bg_bottom": "#133B5C",
    "player": "#00FFC6",
    "text": "#FFFFFF",
    "accent": "#FFD700",
}

class DodgeBlocks:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Dodge the Blocks Deluxe")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.minsize(400, 550)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.state = "menu"
        self.score = 0
        self.best_score = 0
        self.blocks = []
        self.keys = set()

        self.width = WIDTH
        self.height = HEIGHT

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.root.bind("<Configure>", self.on_resize)

        self.draw_menu()

    # MENU SCREEN
    def draw_menu(self):
        self.canvas.delete("all")
        self.draw_background_gradient()
        self.canvas.create_text(self.width/2, self.height/3,
                                text="🚀 DODGE THE BLOCKS 🚀",
                                fill=COLORS["accent"],
                                font=("Helvetica", 28, "bold"))
        self.canvas.create_text(self.width/2, self.height/2,
                                text="← → to move\nSPACE to start",
                                fill=COLORS["text"],
                                font=("Helvetica", 14),
                                justify="center")

    # RESIZE
    def on_resize(self, event):
        self.width, self.height = event.width, event.height
        if self.state == "menu":
            self.draw_menu()

    # SCALE FONT
    def scale_font(self, base_size):
        return max(8, int(base_size * self.width / WIDTH))

    # START GAME
    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.blocks.clear()
        self.canvas.delete("all")
        self.draw_background_gradient()

        # PLAYER
        self.player = self.canvas.create_rectangle(self.width/2-PLAYER_W/2, self.height-80,
                                                   self.width/2+PLAYER_W/2, self.height-60,
                                                   fill=COLORS["player"], outline="")

        # SCORE TEXT
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Score: {self.score}",
                                                  fill=COLORS["text"],
                                                  font=("Helvetica", 14, "bold"))
        self.best_text = self.canvas.create_text(10, 35, anchor="nw",
                                                 text=f"Best: {self.best_score}",
                                                 fill=COLORS["accent"],
                                                 font=("Helvetica", 12, "bold"))

        self.spawn_block()
        self.update_game()

    # BACKGROUND
    def draw_background_gradient(self):
        self.canvas.delete("bg")
        steps = 80
        for i in range(steps):
            color = self._interpolate_color(COLORS["bg_top"], COLORS["bg_bottom"], i/steps)
            y1 = i*(self.height/steps)
            y2 = (i+1)*(self.height/steps)
            self.canvas.create_rectangle(0, y1, self.width, y2, outline="", fill=color, tags="bg")

    def _interpolate_color(self, c1, c2, t):
        def hex_to_rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
        def rgb_to_hex(r): return f"#{r[0]:02x}{r[1]:02x}{r[2]:02x}"
        r1,g1,b1 = hex_to_rgb(c1[1:])
        r2,g2,b2 = hex_to_rgb(c2[1:])
        rgb = (int(r1 + (r2-r1)*t), int(g1+(g2-g1)*t), int(b1+(b2-b1)*t))
        return rgb_to_hex(rgb)

    # KEY HANDLERS
    def key_down(self, event):
        self.keys.add(event.keysym)
        if event.keysym == "space":
            if self.state in ("menu", "gameover"):
                self.start_game()

    def key_up(self, event):
        self.keys.discard(event.keysym)

    # GAME LOOP
    def update_game(self):
        if self.state != "playing":
            return
        self.move_player()
        self.move_blocks()
        self.check_collision()
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.root.after(20, self.update_game)

    # PLAYER
    def move_player(self):
        if "Left" in self.keys:
            self.canvas.move(self.player, -MOVE_SPEED, 0)
        if "Right" in self.keys:
            self.canvas.move(self.player, MOVE_SPEED, 0)
        x1,y1,x2,y2 = self.canvas.coords(self.player)
        if x1<0: self.canvas.move(self.player,-x1,0)
        if x2>self.width: self.canvas.move(self.player,self.width-x2,0)

    # BLOCKS
    def spawn_block(self):
        if self.state!="playing": return
        x = random.randint(0,self.width-BLOCK_W)
        color = random.choice(["#FF5C58","#FFB26B","#FFD93D","#00C2A8"])
        block = self.canvas.create_rectangle(x,-BLOCK_H, x+BLOCK_W,0, fill=color, outline="")
        speed = random.randint(3,6)
        self.blocks.append((block,speed))
        self.root.after(SPAWN_INTERVAL,self.spawn_block)

    def move_blocks(self):
        survived=[]
        for block,speed in self.blocks:
            self.canvas.move(block,0,speed)
            x1,y1,x2,y2 = self.canvas.coords(block)
            if y2<self.height:
                survived.append((block,speed))
            else:
                self.score+=1
                self.canvas.delete(block)
        self.blocks=survived

    # COLLISION
    def check_collision(self):
        px1,py1,px2,py2 = self.canvas.coords(self.player)
        for block,_ in self.blocks:
            bx1,by1,bx2,by2 = self.canvas.coords(block)
            if px1<bx2 and px2>bx1 and py1<by2 and py2>by1:
                self.flash_effect()
                self.end_game()
                return

    # GAME OVER
    def flash_effect(self):
        flash=self.canvas.create_rectangle(0,0,self.width,self.height, fill="white", outline="")
        self.root.update()
        self.root.after(80, lambda:self.canvas.delete(flash))

    def end_game(self):
        self.state="gameover"
        if self.score>self.best_score: self.best_score=self.score
        self.canvas.create_text(self.width/2,self.height/2,
                                text=f"💀 GAME OVER 💀\nScore: {self.score}\nPress SPACE to Restart",
                                fill="white",
                                font=("Helvetica",18,"bold"),
                                justify="center")
        self.canvas.itemconfig(self.best_text,text=f"Best: {self.best_score}")

if __name__=="__main__":
    root=tk.Tk()
    DodgeBlocks(root)
    root.mainloop()
