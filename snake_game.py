import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import struct
import math
import winsound

SAVE_FILE = "snake_save.json"
CONFIG_FILE = "snake_config.json"

def load_config():
    default = {"sound": True, "volume": 70, "resolution": "1920x1080",
               "fullscreen": False, "speed": 5}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            for k, v in default.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
    except:
        return default

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
    except:
        pass

def load_save():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_game(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except:
        pass

def delete_save():
    try:
        os.remove(SAVE_FILE)
    except:
        pass

def _make_wav(freq, duration_ms, volume):
    sample_rate = 8000
    num_samples = int(sample_rate * duration_ms / 1000)
    amplitude = int(volume * 32767 / 100)
    data = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        sample = int(amplitude * math.sin(2 * math.pi * freq * t))
        data.extend(struct.pack("<h", max(-32768, min(32767, sample))))
    wav = bytearray()
    wav.extend(b"RIFF")
    wav.extend(struct.pack("<I", 36 + len(data)))
    wav.extend(b"WAVE")
    wav.extend(b"fmt ")
    wav.extend(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
    wav.extend(b"data")
    wav.extend(struct.pack("<I", len(data)))
    wav.extend(data)
    return bytes(wav)

def play_sound(cfg, freq=880, duration=80):
    if not cfg.get("sound", True):
        return
    vol = cfg.get("volume", 70)
    if vol <= 0:
        return
    try:
        wav_data = _make_wav(freq, duration, vol)
        winsound.PlaySound(wav_data, winsound.SND_MEMORY | winsound.SND_ASYNC)
    except:
        pass

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, config, on_close):
        super().__init__(parent)
        self.config = config
        self.on_close = on_close
        self.title("设置")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")
        self.transient(parent)
        self.grab_set()
        w, h = 380, 480
        px = parent.winfo_x() + (parent.winfo_width() - w) // 2
        py = parent.winfo_y() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")
        tk.Label(self, text="⚙ 游戏设置", font=("微软雅黑", 16, "bold"),
                 fg="#e94560", bg="#1a1a2e").pack(pady=(14, 8))

        # 声音开关
        row1 = tk.Frame(self, bg="#1a1a2e")
        row1.pack(fill=tk.X, padx=30, pady=4)
        tk.Label(row1, text="🔊 游戏声音", font=("微软雅黑", 13),
                 fg="#ffffff", bg="#1a1a2e").pack(side=tk.LEFT)
        self.sound_var = tk.BooleanVar(value=self.config.get("sound", True))
        self.sound_btn = tk.Button(row1, text="开" if self.sound_var.get() else "关",
                                    font=("微软雅黑", 11),
                                    bg="#0f3460" if self.sound_var.get() else "#555555",
                                    fg="#ffffff", relief=tk.FLAT, cursor="hand2",
                                    command=self.toggle_sound, width=6, height=1)
        self.sound_btn.pack(side=tk.RIGHT)

        # 音量
        row2 = tk.Frame(self, bg="#1a1a2e")
        row2.pack(fill=tk.X, padx=30, pady=4)
        tk.Label(row2, text="🔉 音量", font=("微软雅黑", 13),
                 fg="#ffffff", bg="#1a1a2e").pack(side=tk.LEFT)
        vol_frame = tk.Frame(row2, bg="#1a1a2e")
        vol_frame.pack(side=tk.RIGHT)
        self.vol_label = tk.Label(vol_frame, text=str(self.config.get("volume", 70)),
                                   font=("微软雅黑", 10, "bold"),
                                   fg="#00ff88", bg="#1a1a2e", width=4)
        self.vol_label.pack(side=tk.RIGHT, padx=(4, 0))
        self.vol_var = tk.IntVar(value=self.config.get("volume", 70))
        self.vol_slider = tk.Scale(
            vol_frame, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.vol_var, length=120, showvalue=False,
            bg="#1a1a2e", fg="#00ff88", troughcolor="#16213e",
            activebackground="#1a508b", highlightthickness=0,
            command=lambda v: self._on_vol_change())
        self.vol_slider.pack(side=tk.RIGHT)

        test_frame = tk.Frame(self, bg="#1a1a2e")
        test_frame.pack(fill=tk.X, padx=30, pady=1)
        tk.Button(test_frame, text="🔔 试听", font=("微软雅黑", 10),
                  bg="#0f3460", fg="#ffffff", relief=tk.FLAT, cursor="hand2",
                  command=self.test_sound).pack(side=tk.RIGHT)

        # 分辨率
        row3 = tk.Frame(self, bg="#1a1a2e")
        row3.pack(fill=tk.X, padx=30, pady=4)
        tk.Label(row3, text="📺 分辨率", font=("微软雅黑", 13),
                 fg="#ffffff", bg="#1a1a2e").pack(side=tk.LEFT)
        self.res_var = tk.StringVar(value=self.config.get("resolution", "1920x1080"))
        res_opt = tk.OptionMenu(row3, self.res_var, "1920x1080", "1920x1440",
                                 command=lambda _: None)
        res_opt.config(font=("微软雅黑", 11), bg="#0f3460", fg="#ffffff", width=14,
                        relief=tk.FLAT)
        res_opt["menu"].config(bg="#16213e", fg="#ffffff", font=("微软雅黑", 11))
        res_opt.pack(side=tk.RIGHT)

        # 全屏/窗口
        row3b = tk.Frame(self, bg="#1a1a2e")
        row3b.pack(fill=tk.X, padx=30, pady=4)
        tk.Label(row3b, text="🖥 显示模式", font=("微软雅黑", 13),
                 fg="#ffffff", bg="#1a1a2e").pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value="全屏" if self.config.get("fullscreen", False) else "窗口")
        mode_opt = tk.OptionMenu(row3b, self.mode_var, "窗口", "全屏",
                                  command=lambda _: None)
        mode_opt.config(font=("微软雅黑", 11), bg="#0f3460", fg="#ffffff", width=8,
                         relief=tk.FLAT)
        mode_opt["menu"].config(bg="#16213e", fg="#ffffff", font=("微软雅黑", 11))
        mode_opt.pack(side=tk.RIGHT)

        # 速度
        row4 = tk.Frame(self, bg="#1a1a2e")
        row4.pack(fill=tk.X, padx=30, pady=4)
        tk.Label(row4, text="⚡ 游戏速度", font=("微软雅黑", 13),
                 fg="#ffffff", bg="#1a1a2e").pack(side=tk.LEFT)
        spd_frame = tk.Frame(row4, bg="#1a1a2e")
        spd_frame.pack(side=tk.RIGHT)
        speed_labels = {1: "🐢", 3: "🐇", 5: "🚀", 7: "⚡", 10: "💀"}
        self.speed_label = tk.Label(spd_frame,
            text=speed_labels.get(self.config.get("speed", 5), ""),
            font=("微软雅黑", 11), fg="#00ff88", bg="#1a1a2e")
        self.speed_label.pack(side=tk.RIGHT, padx=(4, 0))
        self.speed_var = tk.IntVar(value=self.config.get("speed", 5))
        self.speed_slider = tk.Scale(
            spd_frame, from_=1, to=10, orient=tk.HORIZONTAL,
            variable=self.speed_var, length=120, showvalue=False,
            bg="#1a1a2e", fg="#00ff88", troughcolor="#16213e",
            activebackground="#1a508b", highlightthickness=0,
            command=lambda v: self._on_speed_change())
        self.speed_slider.pack(side=tk.RIGHT)

        btn_frame = tk.Frame(self, bg="#1a1a2e")
        btn_frame.pack(pady=14)
        tk.Button(btn_frame, text="保存", font=("微软雅黑", 12, "bold"),
                  bg="#00ff88", fg="#1a1a2e", relief=tk.FLAT, cursor="hand2",
                  width=10, height=1, command=self.save_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", font=("微软雅黑", 12),
                  bg="#555555", fg="#ffffff", relief=tk.FLAT, cursor="hand2",
                  width=10, height=1, command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _on_vol_change(self):
        self.vol_label.config(text=str(self.vol_var.get()))
    def _on_speed_change(self):
        speed_labels = {1: "🐢", 3: "🐇", 5: "🚀", 7: "⚡", 10: "💀"}
        v = self.speed_var.get()
        closest = min(speed_labels.keys(), key=lambda k: abs(k - v))
        self.speed_label.config(text=speed_labels[closest])
    def toggle_sound(self):
        c = self.sound_var.get()
        self.sound_var.set(not c)
        self.sound_btn.config(text="开" if self.sound_var.get() else "关",
                               bg="#0f3460" if self.sound_var.get() else "#555555")
    def test_sound(self):
        play_sound({"sound": True, "volume": self.vol_var.get()}, 660, 120)
    def save_settings(self):
        self.config["sound"] = self.sound_var.get()
        self.config["volume"] = self.vol_var.get()
        self.config["resolution"] = self.res_var.get()
        self.config["fullscreen"] = (self.mode_var.get() == "全屏")
        self.config["speed"] = self.speed_var.get()
        save_config(self.config)
        self.destroy()
        self.on_close()

class MainMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.place(relwidth=1, relheight=1)
        tk.Label(self, text="🐍 贪 吃 蛇", font=("微软雅黑", 36, "bold"),
                 fg="#00ff88", bg="#1a1a2e").pack(pady=(50, 5))
        tk.Label(self, text="SNAKE GAME", font=("微软雅黑", 12),
                 fg="#e94560", bg="#1a1a2e").pack(pady=(0, 30))
        bs = {"font": ("微软雅黑", 16, "bold"), "width": 16, "height": 1,
              "relief": tk.FLAT, "cursor": "hand2", "bd": 0}
        self.btn_start = tk.Button(self, text="🎮  开始游戏", bg="#0f3460", fg="#ffffff",
                                    activebackground="#1a508b", activeforeground="#ffffff",
                                    command=self.start_game, **bs)
        self.btn_start.pack(pady=8)
        self._hover(self.btn_start, "#0f3460", "#1a508b")
        has_save = load_save() is not None
        self.btn_continue = tk.Button(self, text="▶  继续游戏",
                                       bg="#0f3460" if has_save else "#333333",
                                       fg="#ffffff" if has_save else "#666666",
                                       activebackground="#1a508b",
                                       activeforeground="#ffffff",
                                       state=tk.NORMAL if has_save else tk.DISABLED,
                                       command=self.continue_game, **bs)
        self.btn_continue.pack(pady=8)
        if has_save:
            self._hover(self.btn_continue, "#0f3460", "#1a508b")
        self.btn_settings = tk.Button(self, text="⚙  设置", bg="#0f3460", fg="#ffffff",
                                       activebackground="#1a508b", activeforeground="#ffffff",
                                       command=self.open_settings, **bs)
        self.btn_settings.pack(pady=8)
        self._hover(self.btn_settings, "#0f3460", "#1a508b")
        self.btn_exit = tk.Button(self, text="🚪  结束游戏", bg="#e94560", fg="#ffffff",
                                   activebackground="#ff6b81", activeforeground="#ffffff",
                                   command=self.exit_game, **bs)
        self.btn_exit.pack(pady=8)
        self._hover(self.btn_exit, "#e94560", "#ff6b81")
        tk.Label(self, text="方向键/WASD 移动 | 空格暂停 | +/- 调速 | F11 全屏 | ESC 返回",
                 font=("微软雅黑", 9), fg="#666666", bg="#1a1a2e").pack(side=tk.BOTTOM, pady=15)
    def _hover(self, btn, n, h):
        btn.bind("<Enter>", lambda e: btn.config(bg=h))
        btn.bind("<Leave>", lambda e: btn.config(bg=n))
    def start_game(self):
        delete_save()
        self.app.start_game()
    def continue_game(self):
        data = load_save()
        if data:
            self.app.start_game(load_data=data)
    def open_settings(self):
        SettingsDialog(self, self.app.config, self.app.on_config_changed)
    def exit_game(self):
        if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
            self.app.window.destroy()

class Countdown(tk.Frame):
    def __init__(self, parent, callback, config):
        super().__init__(parent, bg="#1a1a2e")
        self.callback = callback
        self.cfg = config
        self.place(relwidth=1, relheight=1)
        self.tkraise()
        self.label = tk.Label(self, text="", font=("微软雅黑", 80, "bold"),
                              fg="#00ff88", bg="#1a1a2e")
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.count = 3
        self._animate()
    def _animate(self):
        if self.count > 0:
            self.label.config(text=str(self.count))
            play_sound(self.cfg, 660, 150)
            self.count -= 1
            self.after(700, self._animate)
        else:
            self.label.config(text="GO!")
            play_sound(self.cfg, 880, 250)
            self.after(450, self._finish)
    def _finish(self):
        self.destroy()
        self.callback()

class GameScreen(tk.Frame):
    def __init__(self, parent, app, load_data=None):
        super().__init__(parent, bg="#1a1a2e")
        self.app = app
        self.config = app.config

        # 可用空间
        is_fs = self.config.get("fullscreen", False)
        res_str = self.config.get("resolution", "1920x1080")
        res_w, res_h = [int(x) for x in res_str.split("x")]
        if is_fs:
            avail_w = res_w
            avail_h = res_h - 40
        else:
            avail_w = res_w // 2
            avail_h = res_h // 2 - 40

        self.CELL_SIZE = max(20, avail_w // 54)
        self.COLS = avail_w // self.CELL_SIZE
        self.ROWS = avail_h // self.CELL_SIZE
        self.WIDTH = self.COLS * self.CELL_SIZE
        self.HEIGHT = self.ROWS * self.CELL_SIZE

        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT,
                                bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack()

        self.info_frame = tk.Frame(self, bg="#16213e", height=40)
        self.info_frame.pack(fill=tk.X)
        self.info_frame.pack_propagate(False)

        self.score_label = tk.Label(self.info_frame, text="得分: 0",
                                     font=("微软雅黑", 13, "bold"),
                                     fg="#e94560", bg="#16213e")
        self.score_label.pack(side=tk.LEFT, padx=15)

        self.speed_label = tk.Label(self.info_frame, text="速度: 5",
                                     font=("微软雅黑", 10),
                                     fg="#888888", bg="#16213e")
        self.speed_label.pack(side=tk.LEFT, padx=5)

        mode_text = "全屏" if is_fs else "窗口"
        self.hint_label = tk.Label(self.info_frame, text=f"{mode_text} | F11 切换",
                                    font=("微软雅黑", 9),
                                    fg="#666666", bg="#16213e")
        self.hint_label.pack(side=tk.RIGHT, padx=15)

        speed_delays = {1: 200, 2: 180, 3: 160, 4: 140, 5: 120,
                        6: 105, 7: 90, 8: 75, 9: 60, 10: 50}
        self.speed_level = self.config.get("speed", 5)
        self.base_speed = speed_delays.get(self.speed_level, 120)
        self.step_count = 0
        self.obstacles = []

        if load_data:
            self.snake = [tuple(s) for s in load_data["snake"]]
            self.direction = tuple(load_data["direction"])
            self.next_direction = tuple(load_data["direction"])
            self.food = tuple(load_data["food"])
            self.score = load_data["score"]
            self.speed = load_data.get("speed", self.base_speed)
            self.step_count = load_data.get("step_count", 0)
            self.obstacles = [tuple(o) for o in load_data.get("obstacles", [])]
        else:
            self.snake = [(self.COLS // 2, self.ROWS // 2)]
            self.direction = (1, 0)
            self.next_direction = (1, 0)
            self.food = None
            self.score = 0
            self.speed = self.base_speed

        self.game_over = False
        self.paused = False
        self.game_started = False
        self.countdown_active = True

        self.place(relwidth=1, relheight=1)

        if self.food is None:
            self.spawn_food()
        if not self.obstacles:
            self.spawn_obstacles()

        self.speed_label.config(text=f"速度: {self.speed_level}")
        self.draw()
        Countdown(self, self._after_countdown, self.config)

    def _after_countdown(self):
        self.countdown_active = False
        self.game_started = True
        self.game_loop()

    def spawn_food(self):
        while True:
            x = random.randint(0, self.COLS - 1)
            y = random.randint(0, self.ROWS - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                self.food = (x, y)
                break

    def spawn_obstacles(self):
        count = random.randint(1, 5)
        self.obstacles = []
        min_x, max_x = 2, self.COLS - 3
        min_y, max_y = 2, self.ROWS - 3
        zones = []
        cpz = max(2, (max_x - min_x + 1) // 3)
        rpz = max(2, (max_y - min_y + 1) // 2)
        for zx in range(3):
            for zy in range(2):
                zones.append((min_x + zx * cpz, min_x + (zx + 1) * cpz - 1,
                              min_y + zy * rpz, min_y + (zy + 1) * rpz - 1))
        random.shuffle(zones)
        chosen = zones[:count]
        used = set(self.snake)
        if self.food:
            used.add(self.food)
        for zx1, zx2, zy1, zy2 in chosen:
            for _ in range(50):
                x = random.randint(zx1, zx2)
                y = random.randint(zy1, zy2)
                if (x, y) not in used:
                    too_close = any(abs(x - ox) < 3 and abs(y - oy) < 3
                                    for ox, oy in self.obstacles)
                    if not too_close:
                        self.obstacles.append((x, y))
                        used.add((x, y))
                        break

    def on_key(self, event):
        key = event.keysym
        if key == "F11":
            self.app.toggle_fullscreen()
            return
        if key == "Escape":
            if not self.game_over:
                save_game({"snake": self.snake, "direction": self.direction,
                           "food": self.food, "score": self.score,
                           "speed": self.speed, "step_count": self.step_count,
                           "obstacles": self.obstacles})
            self.app.show_menu()
            return
        if self.countdown_active:
            return
        if not self.game_over:
            if key in ("Up", "w", "W") and self.direction != (0, 1):
                self.next_direction = (0, -1)
                play_sound(self.config, 440, 50)
            elif key in ("Down", "s", "S") and self.direction != (0, -1):
                self.next_direction = (0, 1)
                play_sound(self.config, 440, 50)
            elif key in ("Left", "a", "A") and self.direction != (1, 0):
                self.next_direction = (-1, 0)
                play_sound(self.config, 440, 50)
            elif key in ("Right", "d", "D") and self.direction != (-1, 0):
                self.next_direction = (1, 0)
                play_sound(self.config, 440, 50)
            elif key == "space":
                self.paused = not self.paused
            elif key in ("plus", "equal", "KP_Add"):
                if self.speed_level < 10:
                    self.speed_level += 1
                    sd = {1: 200, 2: 180, 3: 160, 4: 140, 5: 120,
                          6: 105, 7: 90, 8: 75, 9: 60, 10: 50}
                    self.base_speed = sd[self.speed_level]
                    self.speed = max(self.speed, self.base_speed)
                    self.speed_label.config(text=f"速度: {self.speed_level}")
            elif key in ("minus", "KP_Subtract"):
                if self.speed_level > 1:
                    self.speed_level -= 1
                    sd = {1: 200, 2: 180, 3: 160, 4: 140, 5: 120,
                          6: 105, 7: 90, 8: 75, 9: 60, 10: 50}
                    self.base_speed = sd[self.speed_level]
                    self.speed = max(self.speed, self.base_speed)
                    self.speed_label.config(text=f"速度: {self.speed_level}")
        if self.game_over and key == "r":
            self.restart()

    def move_snake(self):
        if self.paused or self.game_over or not self.game_started:
            return
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if not (0 <= new_head[0] < self.COLS and 0 <= new_head[1] < self.ROWS):
            self.end_game()
            return
        if new_head in self.snake or new_head in self.obstacles:
            self.end_game()
            return
        self.snake.insert(0, new_head)
        self.step_count += 1
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"得分: {self.score}")
            play_sound(self.config, 660, 60)
            self.spawn_food()
            min_s = max(25, self.base_speed // 3)
            self.speed = max(min_s, self.speed - 3)
        else:
            self.snake.pop()
            if self.step_count % 15 == 0 and self.speed > 30:
                self.speed = max(30, self.speed - 1)

    def draw(self):
        self.canvas.delete("all")
        for i in range(self.COLS):
            self.canvas.create_line(i * self.CELL_SIZE, 0,
                                     i * self.CELL_SIZE, self.HEIGHT, fill="#16213e")
        for i in range(self.ROWS):
            self.canvas.create_line(0, i * self.CELL_SIZE,
                                     self.WIDTH, i * self.CELL_SIZE, fill="#16213e")
        for i, (sx, sy) in enumerate(self.snake):
            x1, y1 = sx * self.CELL_SIZE + 2, sy * self.CELL_SIZE + 2
            x2, y2 = x1 + self.CELL_SIZE - 4, y1 + self.CELL_SIZE - 4
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                          fill="#0f3460" if i == 0 else "#00ff88", outline="")
        if self.food:
            fx, fy = self.food
            cx, cy = fx * self.CELL_SIZE + self.CELL_SIZE // 2, fy * self.CELL_SIZE + self.CELL_SIZE // 2
            r = self.CELL_SIZE // 2 - 3
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                     fill="#e94560", outline="")
        for ox, oy in self.obstacles:
            x1, y1 = ox * self.CELL_SIZE + 4, oy * self.CELL_SIZE + 4
            self.canvas.create_rectangle(x1, y1, x1 + self.CELL_SIZE - 8,
                                          y1 + self.CELL_SIZE - 8,
                                          fill="#8b4513", outline="#a0522d")
        if self.paused and not self.game_over:
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2,
                                     text="⏸ 暂停中", fill="#ffffff",
                                     font=("微软雅黑", 28, "bold"))

    def end_game(self):
        self.game_over = True
        play_sound(self.config, 330, 400)
        delete_save()

    def restart(self):
        self.snake = [(self.COLS // 2, self.ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.speed_level = self.config.get("speed", 5)
        sd = {1: 200, 2: 180, 3: 160, 4: 140, 5: 120,
              6: 105, 7: 90, 8: 75, 9: 60, 10: 50}
        self.base_speed = sd[self.speed_level]
        self.speed = self.base_speed
        self.step_count = 0
        self.obstacles = []
        self.food = None
        self.game_over = False
        self.paused = False
        self.game_started = True
        self.score_label.config(text="得分: 0")
        self.speed_label.config(text=f"速度: {self.speed_level}")
        delete_save()
        self.spawn_food()
        self.spawn_obstacles()
        self.draw()
        self.game_loop()

    def game_loop(self):
        if not self.game_over:
            self.move_snake()
            self.draw()
        if self.game_over:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="#1a1a2e")
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 - 25,
                                     text=f"游戏结束!\
最终得分: {self.score}",
                                     fill="#e94560", font=("微软雅黑", 22, "bold"),
                                     justify=tk.CENTER)
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 + 45,
                                     text="按 R 重新开始  |  ESC 返回菜单",
                                     fill="#00ff88", font=("微软雅黑", 12))
            return
        self.after(self.speed, self.game_loop)

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🐍 贪吃蛇")
        self.config = load_config()
        self._apply_display_mode()
        self.window.configure(bg="#1a1a2e")
        self.window.bind("<KeyPress>", self._global_key)
        self.current_frame = None
        self.show_menu()
        self.window.mainloop()

    def _apply_display_mode(self):
        fs = self.config.get("fullscreen", False)
        self.window.attributes("-fullscreen", fs)
        self.window.resizable(False, False)
        if not fs:
            res_str = self.config.get("resolution", "1920x1080")
            w, h = [int(x) for x in res_str.split("x")]
            w, h = w // 2, h // 2
            self.window.geometry(f"{w}x{h}")
            self.window.update_idletasks()
            sw = self.window.winfo_screenwidth()
            sh = self.window.winfo_screenheight()
            ww = self.window.winfo_width()
            wh = self.window.winfo_height()
            self.window.geometry(f"+{(sw - ww) // 2}+{(sh - wh) // 2}")

    def toggle_fullscreen(self):
        current = self.window.attributes("-fullscreen")
        self.window.attributes("-fullscreen", not current)
        self.config["fullscreen"] = not current
        save_config(self.config)
        if isinstance(self.current_frame, GameScreen):
            self.window.after(100, self.start_game, load_save())

    def _global_key(self, event):
        if event.keysym == "F11":
            self.toggle_fullscreen()
            return
        if isinstance(self.current_frame, GameScreen):
            self.current_frame.on_key(event)

    def show_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainMenu(self.window, self)

    def start_game(self, load_data=None):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = GameScreen(self.window, self, load_data)

    def on_config_changed(self):
        old_fs = self.config.get("fullscreen", False)
        self.config = load_config()
        new_fs = self.config.get("fullscreen", False)
        if old_fs != new_fs:
            self._apply_display_mode()
        if isinstance(self.current_frame, GameScreen):
            self.window.after(100, self.start_game, load_save())