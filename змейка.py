
import tkinter as tk
from random import choice, randint, random
import math
import time
from collections import deque

# Генерация уникальной цветовой палитры
colors = ["#" + ''.join([choice('0123456789ABCDEF') for j in range(6)]) for _ in range(200)]

class EffectApple:
    """Класс для специальных яблок с эффектами"""
    EFFECT_TYPES = {
        'speed': {
            'name': 'Ускорение',
            'color': '#00FF00',
            'glow_color': '#88FF88',
            'duration': 10,
            'icon': '⚡',
            'description': 'Увеличивает скорость в 1.5 раза'
        },
        'shield': {
            'name': 'Щит',
            'color': '#4488FF',
            'glow_color': '#88BBFF',
            'duration': 15,
            'icon': '🛡️',
            'description': 'Защищает от одного столкновения'
        },
        'magnet': {
            'name': 'Магнит',
            'color': '#FF44FF',
            'glow_color': '#FF88FF',
            'duration': 12,
            'icon': '🧲',
            'description': 'Притягивает яблоки в радиусе 200'
        },
        'invisibility': {
            'name': 'Невидимость',
            'color': '#888888',
            'glow_color': '#CCCCCC',
            'duration': 8,
            'icon': '👻',
            'description': 'Враги вас не видят'
        },
        'freeze': {
            'name': 'Заморозка',
            'color': '#88FFFF',
            'glow_color': '#CCFFFF',
            'duration': 6,
            'icon': '❄️',
            'description': 'Замедляет всех врагов на 50%'
        },
        'ghost': {
            'name': 'Призрак',
            'color': '#AA88FF',
            'glow_color': '#CCAAFF',
            'duration': 5,
            'icon': '👻',
            'description': 'Проходит сквозь стены'
        },
        'phase': {
            'name': 'Фаза',
            'color': '#FFFFFF',
            'glow_color': '#FFFFFF',
            'duration': 3,
            'icon': '🌀',
            'description': 'Неуязвимость и прохождение сквозь стены'
        }
    }
    
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.effect_data = self.EFFECT_TYPES[effect_type]
        self.size = 35
        self.pulse_phase = random() * 2 * math.pi
        
    def get_color(self):
        return self.effect_data['color']
    
    def get_glow_color(self):
        return self.effect_data['glow_color']

class PauseButton:
    """Кнопка паузы (отдельный Canvas) слева от мини-карты"""
    def __init__(self, parent, x, y, size=50):
        self.parent = parent
        self.size = size
        self.is_paused = False
        self.pause_callback = None
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg='#111111',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.canvas.place(x=x, y=y)
        
        self._draw_pause_icon()
        
        self.canvas.bind("<Button-1>", self._on_click)
    
    def _draw_pause_icon(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.size, self.size, 
                                     fill='#1a1a1a', outline='#555555', width=1)
        
        bar_width = 8
        bar_height = 24
        gap = 6
        
        x1_left = self.size//2 - gap - bar_width
        x2_left = self.size//2 - gap
        y1 = self.size//2 - bar_height//2
        y2 = self.size//2 + bar_height//2
        
        self.canvas.create_rectangle(x1_left, y1, x2_left, y2, 
                                     fill='#ffffff', outline='')
        
        x1_right = self.size//2 + gap
        x2_right = self.size//2 + gap + bar_width
        
        self.canvas.create_rectangle(x1_right, y1, x2_right, y2, 
                                     fill='#ffffff', outline='')
        
        self.canvas.create_text(self.size//2, self.size - 5, 
                                text="ПАУЗА", fill='#aaaaaa', 
                                font=("Arial", 2), anchor="s")
    
    def _draw_play_icon(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.size, self.size, 
                                     fill='#1a1a1a', outline='#555555', width=1)
        
        tri_size = 14
        cx = self.size//2 + 3
        cy = self.size//2 - 3
        
        self.canvas.create_polygon(
            cx - tri_size//2, cy - tri_size,
            cx - tri_size//2, cy + tri_size,
            cx + tri_size, cy,
            fill='#00ff00', outline=''
        )
        
        self.canvas.create_text(self.size//2, self.size - 5, 
                                text="ИГРАТЬ", fill='#aaaaaa', 
                                font=("Arial", 2), anchor="s")
    
    def _on_click(self, event):
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self._draw_play_icon()
        else:
            self._draw_pause_icon()
        
        if self.pause_callback:
            self.pause_callback(self.is_paused)
    
    def set_pause_callback(self, callback):
        self.pause_callback = callback
    
    def destroy(self):
        self.canvas.destroy()


class ReturnToMenuButton:
    """Кнопка возврата в главное меню (отдельный Canvas)"""
    def __init__(self, parent, x, y, size=50):
        self.parent = parent
        self.size = size
        self.click_callback = None
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size + 25,
            bg='#111111',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.canvas.place(x=x, y=y)
        
        self._draw_icon()
        
        self.canvas.bind("<Button-1>", self._on_click)
    
    def _draw_icon(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.size, self.size, 
                                     fill='#1a1a1a', outline='#555555', width=2)
        
        cx = self.size // 2
        cy = self.size // 2
        
        self.canvas.create_line(
            cx + 12, cy - 6,
            cx - 8, cy - 6,
            fill='#ffffff', width=3
        )
        
        self.canvas.create_line(
            cx - 8, cy - 6,
            cx - 8, cy + 8,
            fill='#ffffff', width=3
        )
        
        self.canvas.create_polygon(
            cx - 8, cy + 8,
            cx - 16, cy + 2,
            cx, cy + 2,
            fill='#ffffff', outline=''
        )
        
        self.canvas.create_text(
            self.size // 2, 
            self.size + 1, 
            text="меню", 
            fill='#aaaaaa', 
            font=("Arial", 2), 
            anchor="n"
        )
    
    def _on_click(self, event):
        if self.click_callback:
            self.click_callback()
    
    def set_click_callback(self, callback):
        self.click_callback = callback
    
    def destroy(self):
        self.canvas.destroy()


class JoystickWidget:
    """Виджет джойстика управления (отдельный Canvas)"""
    def __init__(self, parent, x, y, base_radius=120, thumb_radius=50):
        self.parent = parent
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.thumb_radius = thumb_radius
        self.max_offset = base_radius - thumb_radius - 10
        
        self.is_active = False
        self.thumb_offset_x = 0
        self.thumb_offset_y = 0
        self.last_angle = None
        
        self.direction_callback = None
        
        size = base_radius * 2 + 40
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            highlightthickness=0,
            bd=0,
            relief='flat',
            bg='black'
        )
        
        self.canvas.place(x=x - size//2, y=y - size//2)
        
        self._draw()
        
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
    
    def _draw(self):
        self.canvas.delete("all")
        cx = self.canvas.winfo_reqwidth() // 2
        cy = self.canvas.winfo_reqheight() // 2
        
        r = self.base_radius
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline="#808080",
            width=4,
            fill=""
        )
        
        thumb_x = cx + self.thumb_offset_x
        thumb_y = cy + self.thumb_offset_y
        tr = self.thumb_radius
        self.canvas.create_oval(
            thumb_x - tr, thumb_y - tr,
            thumb_x + tr, thumb_y + tr,
            fill="#808080",
            outline=""
        )
    
    def _on_press(self, event):
        self.is_active = True
        self._update_thumb(event.x, event.y)
    
    def _on_motion(self, event):
        if self.is_active:
            self._update_thumb(event.x, event.y)
    
    def _on_release(self, event):
        self.is_active = False
        self.thumb_offset_x = 0
        self.thumb_offset_y = 0
        self._draw()
        self.last_angle = None
        if self.direction_callback:
            self.direction_callback(0, 0, None)
    
    def _update_thumb(self, mouse_x, mouse_y):
        cx = self.canvas.winfo_reqwidth() // 2
        cy = self.canvas.winfo_reqheight() // 2
        
        dx = mouse_x - cx
        dy = mouse_y - cy
        distance = math.hypot(dx, dy)
        
        if distance > self.max_offset:
            angle = math.atan2(dy, dx)
            dx = math.cos(angle) * self.max_offset
            dy = math.sin(angle) * self.max_offset
            distance = self.max_offset
        
        self.thumb_offset_x = dx
        self.thumb_offset_y = dy
        self._draw()
        
        if self.direction_callback:
            if distance > 8:
                angle = math.degrees(math.atan2(dy, dx)) % 360
                self.last_angle = angle
                self.direction_callback(1, 0, angle)
            else:
                self.last_angle = None
                self.direction_callback(0, 0, None)
    
    def set_direction_callback(self, callback):
        self.direction_callback = callback
    
    def destroy(self):
        self.canvas.destroy()


class AccelerationButton:
    """Кнопка ускорения (отдельный Canvas)"""
    def __init__(self, parent, x, y, radius=60):
        self.parent = parent
        self.radius = radius
        self.is_pressed = False
        self.press_callback = None
        self.release_callback = None
        
        size = radius * 2 + 10
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            highlightthickness=0,
            bd=0,
            relief='flat',
            bg='black'
        )
        self.canvas.place(x=x - size//2, y=y - size//2)
        
        self._draw_normal()
        
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
    
    def _draw_normal(self):
        self.canvas.delete("all")
        cx = self.canvas.winfo_reqwidth() // 2
        cy = self.canvas.winfo_reqheight() // 2
        r = self.radius
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white", outline="")
        self.canvas.create_text(cx, cy, text="↑", font=("Helvetica", 20, "bold"), fill="black")
    
    def _draw_pressed(self):
        self.canvas.delete("all")
        cx = self.canvas.winfo_reqwidth() // 2
        cy = self.canvas.winfo_reqheight() // 2
        r = self.radius
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#cccccc", outline="")
        self.canvas.create_text(cx, cy, text="↑", font=("Helvetica", 20, "bold"), fill="black")
    
    def _on_press(self, event):
        self.is_pressed = True
        self._draw_pressed()
        if self.press_callback:
            self.press_callback()
    
    def _on_release(self, event):
        self.is_pressed = False
        self._draw_normal()
        if self.release_callback:
            self.release_callback()
    
    def set_callbacks(self, press_callback, release_callback):
        self.press_callback = press_callback
        self.release_callback = release_callback
    
    def destroy(self):
        self.canvas.destroy()


class MiniMap:
    """Мини-карта в углу экрана"""
    def __init__(self, parent, x, y, size=200, world_w=3000, world_h=3000):
        self.parent = parent
        self.x = x
        self.y = y
        self.size = size
        self.world_w = world_w
        self.world_h = world_h
        self.scale_x = size / world_w
        self.scale_y = size / world_h
        self._update_counter = 0
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg='#111111',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.canvas.place(x=x, y=y)
    
    def update(self, player_snake, snakes, apples, golden_apples, effect_apples, screen_w, screen_h, camera_x, camera_y, boss=None):
        self._update_counter += 1
        if self._update_counter % 3 != 0:
            return
            
        self.canvas.delete("all")
        
        # Рисуем границы карты на мини-карте
        self.canvas.create_rectangle(0, 0, self.size, self.size, 
                                    outline='#FF0000', width=2, fill='#111111')
        
        if len(apples) < 300:
            for apple_x, apple_y in apples[:100]:
                mx = apple_x * self.scale_x
                my = apple_y * self.scale_y
                self.canvas.create_oval(mx-1, my-1, mx+1, my+1, fill="#ff3333", outline="")
        
        for apple_x, apple_y in golden_apples:
            mx = apple_x * self.scale_x
            my = apple_y * self.scale_y
            self.canvas.create_oval(mx-3, my-3, mx+3, my+3, 
                                   fill="#FFD700", outline="#FFA500", width=1)
        
        for effect_apple in effect_apples:
            mx = effect_apple.x * self.scale_x
            my = effect_apple.y * self.scale_y
            self.canvas.create_oval(mx-3, my-3, mx+3, my+3, 
                                   fill=effect_apple.get_color(), 
                                   outline=effect_apple.get_glow_color(), width=2)
        
        if boss and boss.get('alive') and boss.get('position'):
            hx, hy = boss['position'][-1]
            mx = hx * self.scale_x
            my = hy * self.scale_y
            self.canvas.create_oval(mx-6, my-6, mx+6, my+6, 
                                   fill="#FF0000", outline="#FF6666", width=2)
        
        leader = None
        max_apples = -1
        for snake in snakes:
            if snake['alive'] and snake['eaten_apples'] > max_apples:
                max_apples = snake['eaten_apples']
                leader = snake
        
        for snake in snakes:
            if not snake['alive']:
                continue
            
            if snake.get('invisible', False) and snake['label'] != 'Игрок':
                continue
                
            color = "#00ffff" if snake['label'] == 'Игрок' else snake['color']
            if snake['position']:
                hx, hy = snake['position'][-1]
                mx = hx * self.scale_x
                my = hy * self.scale_y
                
                if snake == leader:
                    self.canvas.create_oval(mx-4, my-4, mx+4, my+4, 
                                           fill=color, outline="#FFD700", width=2)
                else:
                    self.canvas.create_oval(mx-2, my-2, mx+2, my+2, 
                                           fill=color, outline="white", width=0.5)
        
        vx1 = camera_x * self.scale_x
        vy1 = camera_y * self.scale_y
        vx2 = (camera_x + screen_w) * self.scale_x
        vy2 = (camera_y + screen_h) * self.scale_y
        self.canvas.create_rectangle(vx1, vy1, vx2, vy2, outline="white", width=1)
    
    def destroy(self):
        self.canvas.destroy()


class Leaderboard:
    """Таблица лидеров в левом верхнем углу"""
    def __init__(self, parent, x, y, width=220, height=400):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._update_counter = 0
        
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg='#0a0a0a',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.canvas.place(x=x, y=y)
        self._draw_background()
    
    def _draw_background(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                     fill='#0a0a0a', outline='#333333', width=1)
        self.canvas.create_text(self.width//2, 15, text="ТАБЛИЦА ЛИДЕРОВ", 
                                fill="#FFD700", font=("Arial", 2, "bold"), anchor="n")
    
    def update(self, snakes):
        self._update_counter += 1
        if self._update_counter % 5 != 0:
            return
            
        self.canvas.delete("all")
        self._draw_background()
        
        alive_snakes = [(s['label'], s['eaten_apples'], s['color']) 
                       for s in snakes if s['alive']]
        alive_snakes.sort(key=lambda x: x[1], reverse=True)
        
        self.canvas.create_text(25, 35, text="№", fill="#888888", font=("Arial", 3), anchor="w")
        self.canvas.create_text(55, 35, text="Игрок", fill="#888888", font=("Arial", 3), anchor="w")
        self.canvas.create_text(200, 35, text="Яблок", fill="#888888", font=("Arial", 3), anchor="e")
        
        self.canvas.create_line(10, 42, self.width-10, 42, fill="#333333")
        
        for i, (name, apples, color) in enumerate(alive_snakes[:15]):
            y = 50 + i * 22
            
            if i == 0:
                medal = "🥇"
            elif i == 1:
                medal = "🥈"
            elif i == 2:
                medal = "🥉"
            else:
                medal = f"{i+1}."
            
            self.canvas.create_text(20, y, text=medal, fill="white", font=("Arial", 3), anchor="w")
            
            self.canvas.create_oval(50, y-4, 58, y+4, fill=color, outline="")
            
            self.canvas.create_text(65, y, text=name, fill="white", font=("Arial", 4), anchor="w")
            
            self.canvas.create_text(200, y, text=str(apples), fill="#FFD700", font=("Arial", 4, "bold"), anchor="e")
            
            if name == 'Игрок':
                self.canvas.create_rectangle(10, y-10, self.width-10, y+10, 
                                             outline="#00ffff", width=1)
    
    def destroy(self):
        self.canvas.destroy()


class QuestSystem:
    """Система заданий для обычного режима"""
    def __init__(self):
        self.current_quest = None
        self.quest_progress = 0
        self.quest_target = 0
        self.quest_completed = False
        self.quest_reward_claimed = False
        
        self.quest_apples_eaten = 0
        self.quest_golden_apples_eaten = 0
        self.quest_boosts_used = 0
        self.quest_enemies_killed = 0
        self.quest_direction_changes = 0
        self.quest_distance_traveled = 0
        self.quest_survival_time = 0
        self.quest_was_leader = False
        
        self.last_direction = None
        self.last_position = None
        
        self.quest_bosses_killed = 0
        self.quest_effect_apples_eaten = 0
        self.quest_skin_changes = 0
        
        self.quest_pool = [
            {
                'id': 'eat_apples',
                'icon': '🍎',
                'name': 'Съешьте \nяблок',
                'target': 200,
                'reward': 5,
                'get_progress': lambda: self.quest_apples_eaten
            },
            {
                'id': 'eat_golden',
                'icon': '👑',
                'name': 'Съешьте золотых\n яблок',
                'target': 3,
                'reward': 8,
                'get_progress': lambda: self.quest_golden_apples_eaten
            },
            {
                'id': 'use_boost',
                'icon': '💨',
                'name': 'Используйте\n ускорение',
                'target': 10,
                'reward': 3,
                'get_progress': lambda: self.quest_boosts_used
            },
            {
                'id': 'kill_enemies',
                'icon': '⚔️',
                'name': 'Уничтожьте врагов',
                'target': 2,
                'reward': 10,
                'get_progress': lambda: self.quest_enemies_killed
            }, 
            {
                'id': 'become_leader',
                'icon': '🏆',
                'name': 'Станьте лидером',
                'target': 1,
                'reward': 7,
                'get_progress': lambda: 1 if self.quest_was_leader else 0
            },
            {
                'id': 'change_direction',
                'icon': '🔄',
                'name': 'Поменяйте\n направление',
                'target': 50,
                'reward': 4,
                'get_progress': lambda: self.quest_direction_changes
            },
            {
                'id': 'survive_time',
                'icon': '⏱️',
                'name': 'Продержитесь\n секунд',
                'target': 120,
                'reward': 6,
                'get_progress': lambda: int(self.quest_survival_time)
            },
            {
                'id': 'travel_distance',
                'icon': '🗺️',
                'name': 'Проползите\n расстояние',
                'target': 3000,
                'reward': 5,
                'get_progress': lambda: int(self.quest_distance_traveled)
            },
            {
                'id': 'kill_bosses',
                'icon': '🐉',
                'name': 'Победите боссов',
                'target': 2,
                'reward': 20,
                'get_progress': lambda: self.quest_bosses_killed
            },
            {
                'id': 'eat_effect_apples',
                'icon': '✨',
                'name': 'Съешьте\n магических яблок',
                'target': 10,
                'reward': 12,
                'get_progress': lambda: self.quest_effect_apples_eaten
            }
        ]
        
        self.select_random_quest()
    
    def select_random_quest(self):
        self.current_quest = choice(self.quest_pool)
        self.quest_target = self.current_quest['target']
        self.quest_progress = 0
        self.quest_completed = False
        self.quest_reward_claimed = False
        
        self.quest_apples_eaten = 0
        self.quest_golden_apples_eaten = 0
        self.quest_boosts_used = 0
        self.quest_enemies_killed = 0
        self.quest_direction_changes = 0
        self.quest_distance_traveled = 0
        self.quest_survival_time = 0
        self.quest_was_leader = False
        self.quest_bosses_killed = 0
        self.quest_effect_apples_eaten = 0
        self.quest_skin_changes = 0
    
    def update_progress(self):
        if self.quest_completed or not self.current_quest:
            return
        
        progress = self.current_quest['get_progress']()
        self.quest_progress = min(progress, self.quest_target)
        
        if self.quest_progress >= self.quest_target and not self.quest_reward_claimed:
            self.quest_completed = True
    
    def claim_reward(self):
        if self.quest_completed and not self.quest_reward_claimed:
            self.quest_reward_claimed = True
            reward = self.current_quest['reward']
            return reward
        return 0
    
    def track_direction_change(self, current_angle):
        if self.last_direction is not None:
            angle_diff = abs(current_angle - self.last_direction)
            if angle_diff > 10:
                self.quest_direction_changes += 1
        self.last_direction = current_angle
    
    def track_movement(self, current_position):
        if self.last_position is not None:
            dx = current_position[0] - self.last_position[0]
            dy = current_position[1] - self.last_position[1]
            distance = math.hypot(dx, dy)
            self.quest_distance_traveled += distance
        self.last_position = current_position
    
    def draw_quest(self, canvas, screen_width):
        if not self.current_quest or self.quest_reward_claimed:
            return
        
        panel_width = 350
        panel_height = 80
        panel_x = screen_width // 2 - panel_width // 2
        panel_y = 10
        
        canvas.create_rectangle(
            panel_x, panel_y,
            panel_x + panel_width, panel_y + panel_height,
            fill='#1a1a2e', outline='#FFD700', width=2
        )
        
        canvas.create_text(
            panel_x + 40, panel_y + panel_height // 2 - 5,
            text=self.current_quest['icon'],
            font=("Arial", 10),
            anchor="center"
        )
        
        canvas.create_text(
            panel_x + 180, panel_y + 15,
            text=f"Задание: {self.current_quest['name']}",
            fill='#FFFFFF',
            font=("Arial", 3, "bold"),
            anchor="n"
        )
        
        progress_text = f"{self.quest_progress}/{self.quest_target}"
        canvas.create_text(
            panel_x + 240, panel_y + 35,
            text=progress_text,
            fill='#87CEEB',
            font=("Arial", 3),
            anchor="n"
        )
        
        bar_width = panel_width - 100
        bar_height = 12
        bar_x = panel_x + 90
        bar_y = panel_y + 55
        
        canvas.create_rectangle(
            bar_x, bar_y,
            bar_x + bar_width, bar_y + bar_height,
            fill='#333333', outline='#555555'
        )
        
        if self.quest_target > 0:
            fill_width = (self.quest_progress / self.quest_target) * bar_width
            fill_color = '#00FF00' if self.quest_progress >= self.quest_target else '#FFD700'
            
            canvas.create_rectangle(
                bar_x, bar_y,
                bar_x + fill_width, bar_y + bar_height,
                fill=fill_color, outline=''
            )
        
        canvas.create_text(
            panel_x + panel_width - 30, panel_y + panel_height // 2,
            text=f"+{self.current_quest['reward']}💰",
            fill='#FFD700',
            font=("Arial", 3, "bold"),
            anchor="e"
        )


class SnakeGame(tk.Frame):
    ANIMAL_SKINS = {
        'cat': {
            'name': 'Кот',
            'head_color': '#FFA500',
            'ear_color': '#FF8C00',
            'eye_color': '#00FF00',
            'price': 100
        },
        'dog': {
            'name': 'Пёс',
            'head_color': '#8B4513',
            'ear_color': '#A0522D',
            'eye_color': '#FFFFFF',
            'price': 80
        },
        'rabbit': {
            'name': 'Кролик',
            'head_color': '#D3D3D3',
            'ear_color': '#FFB6C1',
            'eye_color': '#FF0000',
            'price': 120
        },
        'pig': {
            'name': 'Хрюшка',
            'head_color': '#FFC0CB',
            'ear_color': '#FF69B4',
            'eye_color': '#000000',
            'price': 70
        },
        'bear': {
            'name': 'Медведь',
            'head_color': '#8B4513',
            'ear_color': '#D2691E',
            'eye_color': '#000000',
            'price': 200
        },
        'fox': {
            'name': 'Лис',
            'head_color': '#FF4500',
            'ear_color': '#FF0000',
            'eye_color': '#000000',
            'price': 150
        },
        'panda': {
            'name': 'Панда',
            'head_color': '#FFFFFF',
            'ear_color': '#000000',
            'eye_color': '#000000',
            'price': 180
        },
        'tiger': {
            'name': 'Тигр',
            'head_color': '#FF8C00',
            'ear_color': '#FF6600',
            'eye_color': '#FFD700',
            'price': 200
        },
        'wolf': {
            'name': 'Волк',
            'head_color': '#808080',
            'ear_color': '#696969',
            'eye_color': '#FF0000',
            'price': 130
        },
        'deer': {
            'name': 'Олень',
            'head_color': '#D2691E',
            'ear_color': '#8B4513',
            'eye_color': '#000000',
            'price': 160
        },
        'dragon': {
            'name': 'Дракон',
            'head_color': '#FF4444',
            'ear_color': '#FF6600',
            'eye_color': '#FFFF00',
            'price': 500
        },
        'phoenix': {
            'name': 'Феникс',
            'head_color': '#FF6600',
            'ear_color': '#FF3300',
            'eye_color': '#FF0000',
            'price': 450
        },
        'unicorn': {
            'name': 'Единорог',
            'head_color': '#FFFFFF',
            'ear_color': '#FF69B4',
            'eye_color': '#FF00FF',
            'price': 400
        },
        'ninja': {
            'name': 'Ниндзя',
            'head_color': '#1a1a1a',
            'ear_color': '#333333',
            'eye_color': '#FF0000',
            'price': 350
        },
        'robot': {
            'name': 'Робот',
            'head_color': '#C0C0C0',
            'ear_color': '#A9A9A9',
            'eye_color': '#00FF00',
            'price': 380
        },
        'zombie': {
            'name': 'Зомби',
            'head_color': '#556B2F',
            'ear_color': '#6B8E23',
            'eye_color': '#00FF00',
            'price': 300
        },
        'vampire': {
            'name': 'Вампир',
            'head_color': '#800000',
            'ear_color': '#A52A2A',
            'eye_color': '#FF0000',
            'price': 420
        },
        'werewolf': {
            'name': 'Оборотень',
            'head_color': '#8B4513',
            'ear_color': '#A0522D',
            'eye_color': '#FF4500',
            'price': 480
        },
        'ghost_skin': {
            'name': 'Призрак',
            'head_color': '#E8E8E8',
            'ear_color': '#D3D3D3',
            'eye_color': '#000000',
            'price': 280
        },
        'demon': {
            'name': 'Демон',
            'head_color': '#8B0000',
            'ear_color': '#DC143C',
            'eye_color': '#FFD700',
            'price': 550
        }
    }
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.attributes('-fullscreen', True)
        
        self.configure(bg='black', highlightthickness=0, bd=0, relief='flat')
        self.grid()
        
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.world_width = 3000
        self.world_height = 3000
        
        self.camera_x = 0
        self.camera_y = 0
        
        self.square_size = 20
        self.head_size = 30
        self.apple_size = 30
        self.golden_apple_size = 45
        self.apple_max = 200
        
        self.joystick_active = False
        self.joystick_angle = None
        
        self.snakes = []
        self.apples = []
        self.golden_apples = []
        self.effect_apples = []
        self.max_effect_apples = 5
        
        self.game_canvas = None
        
        self.is_accelerating = False
        self.player_apple_count = 0
        self.player_coins = 1000
        
        self.coins_earned_this_round = 0
        self.starting_coins = 1000
        
        self.after_id = None
        self.is_game_running = False
        self.round_start_time = time.time()
        
        self.joystick = None
        self.accel_button = None
        self.minimap = None
        self.leaderboard = None
        self.pause_button = None
        self.return_to_menu_button = None
        self.menu_canvas = None
        self.shop_canvas = None
        
        self.best_score = 0
        self.big_start_active = False
        self.big_start_used = False
        
        self.boss = None
        self.boss_timer = 30
        self.boss_active = False
        self.boss_duration = 30
        self.boss_appearance_time = 0
        self.boss_lives = 3
        self.boss_spawn_count = 0
        self.boss_max_spawns = 1
        self.boss_mode = False
        self.boss_entry_cost = 1000
        self.boss_respawn_timer = 0
        self.boss_current_phase = 1
        
        self.quest_system = None
        
        self.player_skin_key = None
        self.player_skin = None
        self.owned_skins = set()
        self.selected_skin_key = None
        
        self._frame_counter = 0
        self._apple_check_counter = 0
        self._ui_update_counter = 0
        self._grid_cache = {'last_camera': None}
        self._last_draw_time = 0
        
        self.active_effects = {}
        self.effect_spawn_timer = 0
        self.total_apples_eaten = 0
        self.effect_apple_threshold = 30
        
        self.ghost_mode = False
        self.phase_mode = False  # Режим фазы (неуязвимость)
        
        self.show_main_menu()
    
    def draw_world_borders(self):
        """Рисует красные границы на границах мира"""
        # Верхняя граница мира
        y_top = self.camera_y
        if 0 <= y_top <= self.world_height:
            sx1, sy1 = self.world_to_screen(0, 0)
            sx2, sy2 = self.world_to_screen(self.world_width, 0)
            self.game_canvas.create_line(max(0, sx1), max(0, sy1), min(self.screen_width, sx2), max(0, sy2), 
                                         fill='#FF0000', width=3)
        
        # Нижняя граница мира
        y_bottom = self.camera_y + self.screen_height
        if 0 <= y_bottom <= self.world_height:
            sx1, sy1 = self.world_to_screen(0, self.world_height)
            sx2, sy2 = self.world_to_screen(self.world_width, self.world_height)
            self.game_canvas.create_line(max(0, sx1), min(self.screen_height, sy1), 
                                         min(self.screen_width, sx2), min(self.screen_height, sy2), 
                                         fill='#FF0000', width=3)
        
        # Левая граница мира
        x_left = self.camera_x
        if 0 <= x_left <= self.world_width:
            sx1, sy1 = self.world_to_screen(0, 0)
            sx2, sy2 = self.world_to_screen(0, self.world_height)
            self.game_canvas.create_line(max(0, sx1), max(0, sy1), max(0, sx2), min(self.screen_height, sy2), 
                                         fill='#FF0000', width=3)
        
        # Правая граница мира
        x_right = self.camera_x + self.screen_width
        if 0 <= x_right <= self.world_width:
            sx1, sy1 = self.world_to_screen(self.world_width, 0)
            sx2, sy2 = self.world_to_screen(self.world_width, self.world_height)
            self.game_canvas.create_line(min(self.screen_width, sx1), max(0, sy1), 
                                         min(self.screen_width, sx2), min(self.screen_height, sy2), 
                                         fill='#FF0000', width=3)
    
    def spawn_effect_apple(self):
        """Создает специальное яблоко с эффектом"""
        if len(self.effect_apples) >= self.max_effect_apples:
            return
        
        effect_type = choice(list(EffectApple.EFFECT_TYPES.keys()))
        
        for _ in range(50):
            x = randint(50, self.world_width - 50)
            y = randint(50, self.world_height - 50)
            
            too_close = False
            for apple in self.apples + self.golden_apples:
                if math.hypot(apple[0] - x, apple[1] - y) < 50:
                    too_close = True
                    break
            
            for effect_apple in self.effect_apples:
                if math.hypot(effect_apple.x - x, effect_apple.y - y) < 100:
                    too_close = True
                    break
            
            if not too_close:
                self.effect_apples.append(EffectApple(x, y, effect_type))
                break
    
    def check_effect_apple_collision(self, snake):
        """Проверяет столкновение со специальными яблоками"""
        head_x, head_y = snake['position'][-1]
        
        for idx, effect_apple in enumerate(self.effect_apples):
            distance = math.hypot(effect_apple.x - head_x, effect_apple.y - head_y)
            if distance < self.head_size + effect_apple.size/2:
                effect_type = effect_apple.effect_type
                del self.effect_apples[idx]
                
                if snake['label'] == 'Игрок':
                    self.apply_effect_to_player(effect_type)
                    if self.quest_system:
                        self.quest_system.quest_effect_apples_eaten += 1
                else:
                    self.apply_effect_to_bot(snake, effect_type)
                
                return True
        return False
    
    def apply_effect_to_player(self, effect_type):
        """Применяет эффект к игроку"""
        duration = EffectApple.EFFECT_TYPES[effect_type]['duration']
        end_time = time.time() + duration
        
        if effect_type == 'ghost':
            self.ghost_mode = True
            self.active_effects[effect_type] = end_time
        elif effect_type == 'phase':
            self.phase_mode = True
            self.active_effects[effect_type] = end_time
        elif effect_type == 'freeze':
            self.active_effects[effect_type] = end_time
        else:
            self.active_effects[effect_type] = end_time
    
    def apply_effect_to_bot(self, snake, effect_type):
        """Применяет эффект к боту"""
        duration = EffectApple.EFFECT_TYPES[effect_type]['duration']
        end_time = time.time() + duration
        
        if 'active_effects' not in snake:
            snake['active_effects'] = {}
        
        snake['active_effects'][effect_type] = end_time
    
    def has_effect(self, snake, effect_type):
        """Проверяет, активен ли эффект у змеи"""
        current_time = time.time()
        
        if snake['label'] == 'Игрок':
            if effect_type == 'phase' and self.phase_mode:
                if self.active_effects.get(effect_type, 0) > current_time:
                    return True
                elif effect_type in self.active_effects:
                    del self.active_effects[effect_type]
                    self.phase_mode = False
            
            if effect_type == 'ghost' and self.ghost_mode:
                if self.active_effects.get(effect_type, 0) > current_time:
                    return True
                elif effect_type in self.active_effects:
                    del self.active_effects[effect_type]
                    self.ghost_mode = False
            
            if effect_type in self.active_effects:
                if self.active_effects[effect_type] > current_time:
                    return True
                else:
                    del self.active_effects[effect_type]
                    if effect_type == 'ghost':
                        self.ghost_mode = False
                    if effect_type == 'phase':
                        self.phase_mode = False
        else:
            if 'active_effects' in snake and effect_type in snake['active_effects']:
                if snake['active_effects'][effect_type] > current_time:
                    return True
                else:
                    del snake['active_effects'][effect_type]
        
        return False
    
    def get_effect_remaining_time(self, effect_type):
        """Возвращает оставшееся время эффекта для игрока"""
        if effect_type == 'phase' and effect_type in self.active_effects:
            remaining = self.active_effects[effect_type] - time.time()
            return max(0, remaining)
        if effect_type == 'ghost' and effect_type in self.active_effects:
            remaining = self.active_effects[effect_type] - time.time()
            return max(0, remaining)
        if effect_type in self.active_effects:
            remaining = self.active_effects[effect_type] - time.time()
            return max(0, remaining)
        return 0
    
    def draw_effect_icons(self):
        """Рисует иконки активных эффектов вверху экрана по середине"""
        if not self.active_effects and not self.ghost_mode and not self.phase_mode:
            return
        
        icon_size = 40
        spacing = 10
        effects_to_show = list(self.active_effects.keys())
        if 'ghost' not in effects_to_show and self.ghost_mode:
            effects_to_show.append('ghost')
        if 'phase' not in effects_to_show and self.phase_mode:
            effects_to_show.append('phase')
        
        total_width = len(effects_to_show) * (icon_size + spacing) - spacing
        
        start_x = self.screen_width // 2 - total_width // 2
        y = 100
        
        if not self.quest_system or self.quest_system.quest_reward_claimed:
            y = 10
        
        current_time = time.time()
        index = 0
        
        for effect_type in effects_to_show:
            if effect_type in self.active_effects and self.active_effects[effect_type] <= current_time:
                if effect_type == 'ghost':
                    self.ghost_mode = False
                if effect_type == 'phase':
                    self.phase_mode = False
                del self.active_effects[effect_type]
                continue
            
            remaining = self.active_effects.get(effect_type, current_time + 5) - current_time
            if effect_type == 'ghost':
                remaining = self.active_effects.get(effect_type, current_time + 5) - current_time
                effect_data = EffectApple.EFFECT_TYPES[effect_type]
            elif effect_type == 'phase':
                remaining = self.active_effects.get(effect_type, current_time + 5) - current_time
                effect_data = EffectApple.EFFECT_TYPES[effect_type]
            elif effect_type in EffectApple.EFFECT_TYPES:
                effect_data = EffectApple.EFFECT_TYPES[effect_type]
            else:
                continue
            
            x = start_x + index * (icon_size + spacing)
            
            self.game_canvas.create_rectangle(
                x, y, x + icon_size, y + icon_size,
                fill='#1a1a2e', outline=effect_data['color'], width=2
            )
            
            self.game_canvas.create_text(
                x + icon_size // 2, y + icon_size // 2 - 5,
                text=effect_data['icon'],
                font=("Arial", 15),
                anchor="center"
            )
            
            self.game_canvas.create_text(
                x + icon_size // 2, y + icon_size - 8,
                text=f"{int(remaining)}с",
                fill='#FFFFFF',
                font=("Arial", 2),
                anchor="center"
            )
            
            bar_height = 3
            fill_width = (remaining / effect_data['duration']) * icon_size
            
            self.game_canvas.create_rectangle(
                x, y + icon_size,
                x + fill_width, y + icon_size + bar_height,
                fill=effect_data['color'], outline=''
            )
            
            index += 1
    
    def draw_effect_apples(self):
        """Рисует специальные яблоки с эффектами"""
        current_time = time.time()
        
        for effect_apple in self.effect_apples:
            if self.is_on_screen(effect_apple.x, effect_apple.y, effect_apple.size):
                sx, sy = self.world_to_screen(effect_apple.x, effect_apple.y)
                size = effect_apple.size
                
                glow_size = size + 10 * math.sin(current_time * 3 + effect_apple.pulse_phase)
                
                self.game_canvas.create_oval(
                    sx - glow_size/2, sy - glow_size/2,
                    sx + glow_size/2, sy + glow_size/2,
                    fill='', outline=effect_apple.get_glow_color(), width=2
                )
                
                self.game_canvas.create_oval(
                    sx - size/2, sy - size/2,
                    sx + size/2, sy + size/2,
                    fill=effect_apple.get_color(), outline='white', width=2
                )
                
                self.game_canvas.create_text(
                    sx, sy,
                    text=effect_apple.effect_data['icon'],
                    font=("Arial", 12),
                    anchor="center"
                )
    
    def clean_expired_effects(self):
        """Очищает истекшие эффекты у всех змей"""
        current_time = time.time()
        
        for effect_type in list(self.active_effects.keys()):
            if self.active_effects[effect_type] <= current_time:
                if effect_type == 'ghost':
                    self.ghost_mode = False
                if effect_type == 'phase':
                    self.phase_mode = False
                del self.active_effects[effect_type]
        
        for snake in self.snakes:
            if snake['label'] != 'Игрок' and 'active_effects' in snake:
                for effect_type in list(snake['active_effects'].keys()):
                    if snake['active_effects'][effect_type] <= current_time:
                        del snake['active_effects'][effect_type]
    
    def draw_rotated_oval(self, cx, cy, w, h, angle, **kwargs):
        """Рисует повернутый овал"""
        angle_rad = math.radians(angle)
        points = []
        for i in range(0, 360, 30):
            theta = math.radians(i)
            x = cx + (w/2) * math.cos(theta) * math.cos(angle_rad) - (h/2) * math.sin(theta) * math.sin(angle_rad)
            y = cy + (w/2) * math.cos(theta) * math.sin(angle_rad) + (h/2) * math.sin(theta) * math.cos(angle_rad)
            points.extend([x, y])
        self.game_canvas.create_polygon(points, **kwargs)
    
    def draw_animal_head(self, sx, sy, snake):
        """Рисует голову животного"""
        angle_rad = math.radians(snake['direction_angle'])
        angle_deg = snake['direction_angle']
        skin = snake.get('skin')
        
        if not skin:
            if snake.get('invisible', False) and snake['label'] != 'Игрок':
                self.game_canvas.create_oval(
                    sx - self.head_size/2, sy - self.head_size/2,
                    sx + self.head_size/2, sy + self.head_size/2,
                    fill="gray", outline="", stipple='gray50'
                )
            else:
                self.game_canvas.create_oval(
                    sx - self.head_size/2, sy - self.head_size/2,
                    sx + self.head_size/2, sy + self.head_size/2,
                    fill="gray", outline=""
                )
            return
        
        head_size = self.head_size
        skin_key = snake['skin_key']
        
        is_invisible = snake.get('invisible', False) and snake['label'] != 'Игрок'
        
        def rotate_point(px, py, cx, cy, angle_rad):
            dx = px - cx
            dy = py - cy
            rotated_x = cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            rotated_y = cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            return rotated_x, rotated_y
        
        ear_distance = head_size * 0.55
        ear_size = head_size * 0.45
        
        stipple = 'gray50' if is_invisible else ''
        
        if skin_key in ['cat', 'tiger', 'wolf', 'fox']:
            for side in [-1, 1]:
                ear_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                ear_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                self.game_canvas.create_polygon(
                    ear_x, ear_y - ear_size,
                    ear_x - ear_size * 0.5 * side, ear_y,
                    ear_x + ear_size * 0.5 * side, ear_y,
                    fill=skin['ear_color'], outline="black", width=1, stipple=stipple
                )
        elif skin_key == 'rabbit':
            for side in [-1, 1]:
                ear_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.3) * ear_distance * 0.8
                ear_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.3) * ear_distance * 0.8
                self.game_canvas.create_oval(
                    ear_x - ear_size * 0.3, ear_y - ear_size * 1.5,
                    ear_x + ear_size * 0.3, ear_y,
                    fill=skin['ear_color'], outline="black", width=1, stipple=stipple
                )
        elif skin_key in ['bear', 'panda']:
            for side in [-1, 1]:
                ear_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                ear_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                self.game_canvas.create_oval(
                    ear_x - ear_size * 0.4, ear_y - ear_size * 0.4,
                    ear_x + ear_size * 0.4, ear_y + ear_size * 0.4,
                    fill=skin['ear_color'], outline="black", width=1, stipple=stipple
                )
        elif skin_key == 'deer':
            for side in [-1, 1]:
                base_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.5) * ear_distance * 0.9
                base_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.5) * ear_distance * 0.9
                tip_x = base_x + math.cos(angle_rad - math.pi/2) * ear_size * 1.5
                tip_y = base_y + math.sin(angle_rad - math.pi/2) * ear_size * 1.5
                self.game_canvas.create_line(base_x, base_y, tip_x, tip_y, 
                                             fill="#654321", width=3, stipple=stipple)
        elif skin_key in ['dog', 'pig']:
            for side in [-1, 1]:
                ear_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                ear_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.5) * ear_distance
                self.game_canvas.create_oval(
                    ear_x - ear_size * 0.4, ear_y - ear_size * 0.4,
                    ear_x + ear_size * 0.4, ear_y + ear_size * 0.4,
                    fill=skin['ear_color'], outline="black", width=1, stipple=stipple
                )
        elif skin_key == 'dragon':
            for side in [-1, 1]:
                horn_x = sx + math.cos(angle_rad - math.pi/2 + side * 0.4) * ear_distance
                horn_y = sy + math.sin(angle_rad - math.pi/2 + side * 0.4) * ear_distance
                tip_x = horn_x + math.cos(angle_rad - math.pi/2) * ear_size * 1.8
                tip_y = horn_y + math.sin(angle_rad - math.pi/2) * ear_size * 1.8
                self.game_canvas.create_line(horn_x, horn_y, tip_x, tip_y, 
                                             fill="#FF6600", width=4, stipple=stipple)
        elif skin_key == 'unicorn':
            horn_x = sx + math.cos(angle_rad - math.pi/2) * ear_distance * 0.8
            horn_y = sy + math.sin(angle_rad - math.pi/2) * ear_distance * 0.8
            tip_x = horn_x + math.cos(angle_rad - math.pi/2) * ear_size * 2
            tip_y = horn_y + math.sin(angle_rad - math.pi/2) * ear_size * 2
            self.game_canvas.create_line(horn_x, horn_y, tip_x, tip_y, 
                                         fill="#FFD700", width=5, stipple=stipple)
        elif skin_key == 'ghost_skin':
            self.game_canvas.create_oval(
                sx - head_size/2, sy - head_size/2,
                sx + head_size/2, sy + head_size/2,
                fill=skin['head_color'], outline="#AAAAAA", width=1, stipple='gray25'
            )
            return
        
        self.draw_rotated_oval(sx, sy, head_size-2, head_size-4, angle_deg, 
                              fill=skin['head_color'], outline="black", width=1, stipple=stipple)
        
        eye_color = skin['eye_color']
        eye_distance = head_size * 0.35
        eye_size = head_size * 0.2
        
        for side in [-1, 1]:
            eye_x = sx + math.cos(angle_rad + side * 0.3) * eye_distance
            eye_y = sy + math.sin(angle_rad + side * 0.3) * eye_distance
            
            self.game_canvas.create_oval(
                eye_x - eye_size/2, eye_y - eye_size/3,
                eye_x + eye_size/2, eye_y + eye_size/3,
                fill="white", outline="black", width=1
            )
            
            self.game_canvas.create_oval(
                eye_x - eye_size/4, eye_y - eye_size/4,
                eye_x + eye_size/4, eye_y + eye_size/4,
                fill=eye_color, outline=""
            )
    
    def show_shop(self):
        """Показать магазин скинов"""
        for widget in self.winfo_children():
            widget.destroy()
        self.menu_canvas = None
        self.shop_canvas = None
        
        self.shop_canvas = tk.Canvas(
            self,
            width=self.screen_width,
            height=self.screen_height,
            bg='#1a1a2e',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.shop_canvas.pack(fill='both', expand=True)
        
        self.shop_canvas.create_text(
            self.screen_width // 2, 50,
            text="МАГАЗИН СКИНОВ",
            font=("Arial", 15, "bold"),
            fill="#FFD700",
            anchor="center"
        )
        
        self.shop_canvas.create_text(
            self.screen_width - 100, 120,
            text=f"💰 {self.player_coins}",
            font=("Arial", 8, "bold"),
            fill="#FFD700",
            anchor="e"
        )
        
        return_btn_width = 200
        return_btn_height = 60
        return_btn_x = 20
        return_btn_y = 90
        
        self.shop_canvas.create_rectangle(
            return_btn_x, return_btn_y,
            return_btn_x + return_btn_width, return_btn_y + return_btn_height,
            fill="#0088ff", outline="#0066cc", width=3
        )
        self.shop_canvas.create_text(
            return_btn_x + return_btn_width // 2,
            return_btn_y + return_btn_height // 2,
            text="← НАЗАД",
            font=("Arial", 6, "bold"),
            fill="white",
            anchor="center"
        )
        
        self.return_button_coords = (
            return_btn_x, return_btn_y,
            return_btn_x + return_btn_width, return_btn_y + return_btn_height
        )
        
        skins_list = list(self.ANIMAL_SKINS.items())
        cols = 5
        rows = (len(skins_list) + cols - 1) // cols
        
        card_width = 180
        card_height = 220
        start_x = (self.screen_width - cols * card_width - (cols - 1) * 20) // 2
        start_y = 150
        
        for idx, (skin_key, skin_data) in enumerate(skins_list):
            row = idx // cols
            col = idx % cols
            
            x1 = start_x + col * (card_width + 20)
            y1 = start_y + row * (card_height + 20)
            x2 = x1 + card_width
            y2 = y1 + card_height
            
            if self.selected_skin_key == skin_key:
                outline_color = "#FFD700"
                outline_width = 3
            else:
                outline_color = "#333333"
                outline_width = 1
            
            self.shop_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill='#16213e', outline=outline_color, width=outline_width
            )
            
            self.shop_canvas.create_text(
                (x1 + x2) // 2, y1 + 25,
                text=skin_data['name'],
                font=("Arial", 4, "bold"),
                fill="white",
                anchor="center"
            )
            
            preview_x = (x1 + x2) // 2
            preview_y = y1 + 100
            
            self.shop_canvas.create_oval(
                preview_x - 25, preview_y - 22,
                preview_x + 25, preview_y + 22,
                fill=skin_data['head_color'], outline="black", width=2
            )
            
            for side in [-1, 1]:
                eye_x = preview_x + side * 12
                eye_y = preview_y - 5
                self.shop_canvas.create_oval(
                    eye_x - 6, eye_y - 5,
                    eye_x + 6, eye_y + 5,
                    fill="white", outline="black", width=1
                )
                self.shop_canvas.create_oval(
                    eye_x - 3, eye_y - 3,
                    eye_x + 3, eye_y + 3,
                    fill=skin_data['eye_color'], outline=""
                )
            
            if skin_key in self.owned_skins:
                if self.selected_skin_key == skin_key:
                    status_text = "✓ ВЫБРАН"
                    status_color = "#00FF00"
                else:
                    status_text = "КУПЛЕН"
                    status_color = "#00AA00"
                
                self.shop_canvas.create_text(
                    preview_x, y1 + 180,
                    text=status_text,
                    font=("Arial", 4, "bold"),
                    fill=status_color,
                    anchor="center"
                )
            else:
                price = skin_data['price']
                can_afford = self.player_coins >= price
                price_color = "#FFD700" if can_afford else "#FF0000"
                
                self.shop_canvas.create_text(
                    preview_x, y1 + 170,
                    text=f"💰 {price}",
                    font=("Arial", 5, "bold"),
                    fill=price_color,
                    anchor="center"
                )
                
                if can_afford:
                    self.shop_canvas.create_text(
                        preview_x, y2 - 15,
                        text="Нажмите для покупки",
                        font=("Arial", 2),
                        fill="#AAAAAA",
                        anchor="center"
                    )
            
            skin_coords_attr = f'skin_{skin_key}_coords'
            setattr(self, skin_coords_attr, (x1, y1, x2, y2))
        
        default_y = start_y + ((len(skins_list) + cols - 1) // cols) * (card_height + 20) + 20
        default_x1 = (self.screen_width - card_width) // 2
        default_x2 = default_x1 + card_width
        default_y1 = default_y
        default_y2 = default_y + card_height
        
        self.shop_canvas.create_rectangle(
            default_x1, default_y1, default_x2, default_y2,
            fill='#16213e', 
            outline="#FFD700" if self.selected_skin_key is None else "#333333",
            width=3 if self.selected_skin_key is None else 1
        )
        
        self.shop_canvas.create_text(
            (default_x1 + default_x2) // 2, default_y1 + 25,
            text="СТАНДАРТНАЯ",
            font=("Arial", 2, "bold"),
            fill="white",
            anchor="center"
        )
        
        preview_x = (default_x1 + default_x2) // 2
        preview_y = default_y1 + 100
        
        self.shop_canvas.create_oval(
            preview_x - 25, preview_y - 22,
            preview_x + 25, preview_y + 22,
            fill="#00ffff", outline="black", width=2
        )
        
        self.shop_canvas.create_text(
            preview_x, default_y1 + 180,
            text="БЕСПЛАТНО" if self.selected_skin_key is not None else "✓ ВЫБРАН",
            font=("Arial", 4, "bold"),
            fill="#00FF00" if self.selected_skin_key is not None else "#00AA00",
            anchor="center"
        )
        
        self.default_skin_coords = (default_x1, default_y1, default_x2, default_y2)
        
        self.shop_canvas.bind("<Button-1>", self.on_shop_click)
    
    def on_shop_click(self, event):
        """Обработка кликов в магазине"""
        if hasattr(self, 'return_button_coords'):
            x1, y1, x2, y2 = self.return_button_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.show_main_menu()
                return
        
        if hasattr(self, 'default_skin_coords'):
            x1, y1, x2, y2 = self.default_skin_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.selected_skin_key = None
                self.player_skin = None
                self.player_skin_key = None
                if self.quest_system:
                    self.quest_system.quest_skin_changes += 1
                self.show_shop()
                return
        
        for skin_key in self.ANIMAL_SKINS:
            coords_attr = f'skin_{skin_key}_coords'
            if hasattr(self, coords_attr):
                x1, y1, x2, y2 = getattr(self, coords_attr)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    if skin_key in self.owned_skins:
                        self.selected_skin_key = skin_key
                        self.player_skin = self.ANIMAL_SKINS[skin_key]
                        self.player_skin_key = skin_key
                        if self.quest_system:
                            self.quest_system.quest_skin_changes += 1
                        self.show_shop()
                    else:
                        price = self.ANIMAL_SKINS[skin_key]['price']
                        if self.player_coins >= price:
                            self.player_coins -= price
                            self.owned_skins.add(skin_key)
                            self.selected_skin_key = skin_key
                            self.player_skin = self.ANIMAL_SKINS[skin_key]
                            self.player_skin_key = skin_key
                            if self.quest_system:
                                self.quest_system.quest_skin_changes += 1
                            self.show_shop()
                    return
    
    def return_to_main_menu(self):
        if self.player_apple_count > self.best_score:
            self.best_score = self.player_apple_count
        
        self.is_game_running = False
        self.boss_mode = False
        self.stop_auto_move()
        
        if self.pause_button:
            self.pause_button.is_paused = False
        
        self.show_main_menu()
    
    def show_main_menu(self):
        self.is_game_running = False
        self.boss_mode = False
        self.stop_auto_move()
        
        for widget in self.winfo_children():
            widget.destroy()
        
        self.game_canvas = None
        self.menu_canvas = None
        self.shop_canvas = None
        self.joystick = None
        self.accel_button = None
        self.minimap = None
        self.leaderboard = None
        self.pause_button = None
        self.return_to_menu_button = None
        
        self.menu_canvas = tk.Canvas(
            self,
            width=self.screen_width,
            height=self.screen_height,
            bg='#87CEEB',
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.menu_canvas.pack(fill='both', expand=True)
        
        circle_btn_x = 60
        circle_btn_y = 60
        circle_btn_r = 35
        
        self.menu_canvas.create_oval(
            circle_btn_x - circle_btn_r, circle_btn_y - circle_btn_r,
            circle_btn_x + circle_btn_r, circle_btn_y + circle_btn_r,
            fill='#0088ff', outline='#0066cc', width=3
        )
        self.menu_canvas.create_text(
            circle_btn_x, circle_btn_y,
            text="🎨",
            font=("Arial", 20),
            anchor="center"
        )
        
        self.menu_canvas.create_text(
            circle_btn_x, circle_btn_y + circle_btn_r + 30,
            text="скины",
            font=("Arial", 4, "bold"),
            fill="#1a1a2e",
            anchor="n")
        
        self.shop_button_coords = (circle_btn_x - circle_btn_r, circle_btn_y - circle_btn_r,
                                   circle_btn_x + circle_btn_r, circle_btn_y + circle_btn_r)
        
        if self.player_skin_key:
            skin_name = self.ANIMAL_SKINS[self.player_skin_key]['name']
            self.menu_canvas.create_text(
                circle_btn_x, circle_btn_y + circle_btn_r + 55,
                text=f"Скин: {skin_name}",
                font=("Arial", 3),
                fill="#1a1a2e",
                anchor="n"
            )
        
        self.menu_canvas.create_text(
            self.screen_width // 2,
            self.screen_height // 3,
            text="ЗМЕЙКА",
            font=("Arial", 20, "bold"),
            fill="#1a1a2e",
            anchor="center"
        )
        
        self.menu_canvas.create_text(
            self.screen_width // 2,
            self.screen_height // 3 + 70,
            text="Битва королей",
            font=("Arial", 15),
            fill="#2d2d44",
            anchor="center"
        )
        
        self.draw_coins_in_menu()
        self.draw_best_result_in_menu()
        
        btn_width = 300
        btn_height = 100
        margin_right = 60
        margin_bottom = 60
        
        big_btn_y1 = self.screen_height - margin_bottom - btn_height * 2 - 15
        big_btn_y2 = self.screen_height - margin_bottom - btn_height - 15
        
        btn_x1 = self.screen_width - margin_right - btn_width
        btn_x2 = self.screen_width - margin_right
        
        if self.big_start_active:
            btn_color = "#00AA00"
            btn_outline = "#008800"
            btn_text = "✓ НАЧАТЬ С БОЛЬШОЙ"
        elif self.big_start_used:
            btn_color = "#FF8C00"
            btn_outline = "#FF6600"
            btn_text = "НАЧАТЬ С БОЛЬШОЙ\n100 💰"
            self.big_start_used = False
            self.big_start_active = False
        else:
            btn_color = "#FF8C00"
            btn_outline = "#FF6600"
            btn_text = "НАЧАТЬ С БОЛЬШОЙ\n100 💰"
        
        self.menu_canvas.create_rectangle(
            btn_x1, big_btn_y1, btn_x2, big_btn_y2,
            fill=btn_color, outline=btn_outline, width=4
        )
        
        self.menu_canvas.create_text(
            (btn_x1 + btn_x2) // 2,
            (big_btn_y1 + big_btn_y2) // 2,
            text=btn_text,
            font=("Arial", 3, "bold"),
            fill="#FFFFFF",
            anchor="center",
            justify="center"
        )
        
        self.big_start_button_coords = (btn_x1, big_btn_y1, btn_x2, big_btn_y2)
        
        play_btn_y1 = self.screen_height - margin_bottom - btn_height
        play_btn_y2 = self.screen_height - margin_bottom
        
        self.menu_canvas.create_rectangle(
            btn_x1, play_btn_y1, btn_x2, play_btn_y2,
            fill="#FFD700", outline="#FFA500", width=4
        )
        
        self.menu_canvas.create_text(
            (btn_x1 + btn_x2) // 2,
            (play_btn_y1 + play_btn_y2) // 2,
            text="ИГРАТЬ",
            font=("Arial", 10, "bold"),
            fill="#1a1a2e",
            anchor="center"
        )
        
        self.play_button_coords = (btn_x1, play_btn_y1, btn_x2, play_btn_y2)
        
        boss_btn_width = 220
        boss_btn_height = 100
        boss_btn_x1 = btn_x1 - boss_btn_width - 15
        boss_btn_x2 = btn_x1 - 15
        boss_btn_y1 = play_btn_y1
        boss_btn_y2 = play_btn_y2
        
        can_afford = self.player_coins >= self.boss_entry_cost
        btn_fill = "#CC0000" if can_afford else "#660000"
        btn_outline_color = "#FF3333" if can_afford else "#990000"
        
        self.menu_canvas.create_rectangle(
            boss_btn_x1, boss_btn_y1, boss_btn_x2, boss_btn_y2,
            fill=btn_fill, outline=btn_outline_color, width=4
        )
        
        self.menu_canvas.create_text(
            (boss_btn_x1 + boss_btn_x2) // 2,
            (boss_btn_y1 + boss_btn_y2) // 2 - 15,
            text="СОБЫТИЕ",
            font=("Arial", 4, "bold"),
            fill="#FFFFFF",
            anchor="center"
        )
        
        self.menu_canvas.create_text(
            (boss_btn_x1 + boss_btn_x2) // 2,
            (boss_btn_y1 + boss_btn_y2) // 2 + 10,
            text=f"ДРАКА С БОССОМ",
            font=("Arial", 3, "bold"),
            fill="#FFFFFF",
            anchor="center"
        )
        
        self.menu_canvas.create_text(
            (boss_btn_x1 + boss_btn_x2) // 2,
            (boss_btn_y1 + boss_btn_y2) // 2 + 30,
            text=f"💰 {self.boss_entry_cost}",
            font=("Arial", 4, "bold"),
            fill="#FFD700",
            anchor="center"
        )
        
        self.boss_button_coords = (boss_btn_x1, boss_btn_y1, boss_btn_x2, boss_btn_y2)
        
        self.menu_canvas.bind("<Button-1>", self.on_menu_click)
    
    def draw_coins_in_menu(self):
        coin_x = self.screen_width - 120
        coin_y = 60
        
        coin_bg_x1 = coin_x - 80
        coin_bg_y1 = coin_y - 50
        coin_bg_x2 = coin_x + 80
        coin_bg_y2 = coin_y + 25
        
        self.menu_canvas.create_rectangle(
            coin_bg_x1, coin_bg_y1, coin_bg_x2, coin_bg_y2,
            fill='#1a1a2e', outline='#FFD700', width=3
        )
        
        self.menu_canvas.create_text(
            coin_x, coin_y - 35,
            text="БАЛАНС",
            fill='#87CEEB',
            font=("Arial", 3, "bold")
        )
        
        coin_icon_x = coin_x - 30
        coin_icon_y = coin_y - 1
        
        self.menu_canvas.create_oval(
            coin_icon_x - 15, coin_icon_y - 15,
            coin_icon_x + 15, coin_icon_y + 15,
            fill='#FFD700', outline='#FFA500', width=3
        )
        
        self.menu_canvas.create_text(
            coin_icon_x, coin_icon_y - 6,
            text="$",
            fill='#B8860B',
            font=("Arial", 10, "bold")
        )
        
        self.menu_canvas.create_text(
            coin_x + 20, coin_icon_y - 1,
            text=str(self.player_coins),
            fill='#FFD700',
            font=("Arial", 4, "bold")
        )
    
    def draw_best_result_in_menu(self):
        best_x = self.screen_width - 120
        best_y = 120
        
        best_bg_x1 = best_x - 80
        best_bg_y1 = best_y - 25
        best_bg_x2 = best_x + 80
        best_bg_y2 = best_y + 50
        
        self.menu_canvas.create_rectangle(
            best_bg_x1, best_bg_y1, best_bg_x2, best_bg_y2,
            fill='#1a1a2e', outline='#FFD700', width=3
        )
        
        self.menu_canvas.create_text(
            best_x, best_y - 12,
            text="ЛУЧШИЙ",
            fill='#87CEEB',
            font=("Arial", 3, "bold")
        )
        
        self.menu_canvas.create_text(
            best_x, best_y + 25,
            text=str(self.best_score),
            fill='#FFD700',
            font=("Arial", 6, "bold")
        )
    
    def on_menu_click(self, event):
        if hasattr(self, 'shop_button_coords'):
            x1, y1, x2, y2 = self.shop_button_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.show_shop()
                return
        
        if hasattr(self, 'play_button_coords'):
            x1, y1, x2, y2 = self.play_button_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.boss_mode = False
                self.start_game()
                return
        
        if hasattr(self, 'big_start_button_coords'):
            x1, y1, x2, y2 = self.big_start_button_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if not self.big_start_active and self.player_coins >= 100:
                    self.player_coins -= 100
                    self.big_start_active = True
                    self.show_main_menu()
                return
        
        if hasattr(self, 'boss_button_coords'):
            x1, y1, x2, y2 = self.boss_button_coords
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if self.player_coins >= self.boss_entry_cost:
                    self.player_coins -= self.boss_entry_cost
                    self.boss_mode = True
                    self.start_boss_event()
                return
    
    def start_boss_event(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.joystick = None
        self.accel_button = None
        self.minimap = None
        self.leaderboard = None
        self.pause_button = None
        self.return_to_menu_button = None
        self.game_canvas = None
        self.menu_canvas = None
        self.shop_canvas = None
        
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        
        self.game_canvas = tk.Canvas(
            self,
            width=self.screen_width,
            height=self.screen_height,
            bg="#0a0a0a",
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.game_canvas.pack(fill='both', expand=True)
        
        self.update_idletasks()
        
        self.snakes = []
        self.apples = []
        self.golden_apples = []
        self.effect_apples = []
        self.active_effects = {}
        self.total_apples_eaten = 0
        
        start_x = self.world_width // 2
        start_y = self.world_height // 2
        self.snakes.append({
            'label': 'Игрок',
            'color': '#808080',  # Серая в начале
            'original_color': '#00ffff',
            'position': [(start_x, start_y)],
            'direction_angle': randint(0, 360),
            'eaten_apples': 0,
            'alive': True,
            'strategy': 'exploring',
            'target': None,
            'acceleration_cooldown': 0,
            'immune_until': time.time() + 3,  # 3 секунды неуязвимости
            'birth_time': time.time(),
            'strategy_update_counter': 0,
            'personality': 'player',
            'memory': deque(maxlen=30),
            'territory_center': (start_x, start_y),
            'patrol_points': self.generate_patrol_points(start_x, start_y),
            'patrol_index': 0,
            'skin': self.player_skin,
            'skin_key': self.player_skin_key,
            'active_effects': {},
            'phase_effect': True  # Эффект фазы активен
        })
        
        self.boss = None
        self.boss_timer = 90
        self.boss_active = False
        self.boss_lives = 3
        self.boss_spawn_count = 0
        self.boss_current_phase = 1
        self.boss_respawn_timer = 0
        
        self.spawn_apples()
        self.is_accelerating = False
        self.player_apple_count = 0
        self.joystick_active = False
        self.joystick_angle = None
        self.round_start_time = time.time()
        self.starting_coins = self.player_coins
        self.coins_earned_this_round = 0
        
        self.quest_system = None
        
        self.create_ui()
        
        self.game_canvas.bind("<B1-Motion>", self.on_mouse_click)
        self.game_canvas.bind("<Button-1>", self.on_mouse_click)
        
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)
        
        self.is_game_running = True
        self.draw_all()
        self.auto_move()
    
    def start_game(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.joystick = None
        self.accel_button = None
        self.minimap = None
        self.leaderboard = None
        self.pause_button = None
        self.return_to_menu_button = None
        self.game_canvas = None
        self.menu_canvas = None
        self.shop_canvas = None
        
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        
        self.game_canvas = tk.Canvas(
            self,
            width=self.screen_width,
            height=self.screen_height,
            bg="#0a0a0a",
            highlightthickness=0,
            bd=0,
            relief='flat'
        )
        self.game_canvas.pack(fill='both', expand=True)
        
        self.update_idletasks()
        
        self.init_game()
        
        # Делаем всех змей серыми, бессмертными и неуязвимыми на 3 секунды в начале раунда
        for snake in self.snakes:
            snake['immune_until'] = time.time() + 3
            if 'original_color' not in snake:
                snake['original_color'] = snake['color']
            snake['color'] = '#808080'
            snake['phase_effect'] = True
        
        if self.big_start_active:
            player = self.get_player_snake()
            if player:
                player['eaten_apples'] = 100
                self.player_apple_count = 100
                
                head_x, head_y = player['position'][-1]
                angle_rad = math.radians(player['direction_angle'])
                
                for i in range(99):
                    seg_x = head_x - math.cos(angle_rad) * (i + 1) * (self.square_size * 0.8)
                    seg_y = head_y - math.sin(angle_rad) * (i + 1) * (self.square_size * 0.8)
                    player['position'].insert(0, (seg_x, seg_y))
            
            self.big_start_used = True
            self.big_start_active = False
        
        self.quest_system = QuestSystem()
        self.starting_coins = self.player_coins
        self.coins_earned_this_round = 0
        
        self.effect_apples = []
        self.active_effects = {}
        self.effect_spawn_timer = 0
        self.total_apples_eaten = 0
        self.spawn_effect_apple()
        
        self.create_ui()
        
        self.game_canvas.bind("<B1-Motion>", self.on_mouse_click)
        self.game_canvas.bind("<Button-1>", self.on_mouse_click)
        
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)
        
        self.is_game_running = True
        self.draw_all()
        self.auto_move()
    
    def init_game(self):
        self.snakes = []
        self.apples = []
        self.golden_apples = []
        self.effect_apples = []
        self.active_effects = {}
        self.total_apples_eaten = 0
        
        self.boss = None
        self.boss_active = False
        
        bot_names = [
            'Альфа', 'Бета', 'Гамма', 'Дельта', 'Эпсилон',
            'Зета', 'Эта', 'Тета', 'Йота', 'Каппа',
            'Лямбда', 'Мю', 'Ню', 'Кси', 'Омикрон',
            'Пи', 'Ро', 'Сигма', 'Тау', 'Омега'
        ]
        
        start_x = randint(500, self.world_width - 500)
        start_y = randint(500, self.world_height - 500)
        self.snakes.append({
            'label': 'Игрок',
            'color': '#808080',
            'original_color': '#00ffff',
            'position': [(start_x, start_y)],
            'direction_angle': randint(0, 360),
            'eaten_apples': 0,
            'alive': True,
            'strategy': 'exploring',
            'target': None,
            'acceleration_cooldown': 0,
            'immune_until': time.time() + 3,
            'birth_time': time.time(),
            'strategy_update_counter': 0,
            'personality': 'player',
            'memory': deque(maxlen=30),
            'territory_center': (start_x, start_y),
            'patrol_points': self.generate_patrol_points(start_x, start_y),
            'patrol_index': 0,
            'skin': self.player_skin,
            'skin_key': self.player_skin_key,
            'active_effects': {},
            'phase_effect': True
        })
        
        for i in range(19):
            start_x = randint(200, self.world_width - 200)
            start_y = randint(200, self.world_height - 200)
            personality_type = choice(['hunter', 'collector', 'aggressive', 'cautious'])
            
            skin_key = choice(list(self.ANIMAL_SKINS.keys()))
            skin = self.ANIMAL_SKINS[skin_key]
            
            self.snakes.append({
                'label': bot_names[i],
                'color': '#808080',
                'original_color': skin['head_color'],
                'position': [(start_x, start_y)],
                'direction_angle': randint(0, 360),
                'eaten_apples': 0,
                'alive': True,
                'strategy': 'exploring',
                'target': None,
                'acceleration_cooldown': 0,
                'immune_until': time.time() + 3,
                'birth_time': time.time(),
                'strategy_update_counter': 0,
                'personality': personality_type,
                'memory': deque(maxlen=30),
                'territory_center': (start_x, start_y),
                'patrol_points': self.generate_patrol_points(start_x, start_y),
                'patrol_index': 0,
                'skin': skin,
                'skin_key': skin_key,
                'active_effects': {},
                'phase_effect': True
            })
        
        self.spawn_apples()
        self.is_accelerating = False
        self.player_apple_count = 0
        self.joystick_active = False
        self.joystick_angle = None
        self.round_start_time = time.time()
    
    def toggle_pause(self, is_paused):
        if is_paused:
            self.is_game_running = False
            self.stop_auto_move()
            if self.game_canvas:
                self.game_canvas.create_rectangle(
                    0, 0, self.screen_width, self.screen_height,
                    fill='black', stipple='gray50', tags='pause_overlay'
                )
                self.game_canvas.create_text(
                    self.screen_width // 2, self.screen_height // 2,
                    text="ПАУЗА",
                    font=("Arial", 20, "bold"),
                    fill="white",
                    tags='pause_text'
                )
        else:
            if self.game_canvas:
                self.game_canvas.delete('pause_overlay')
                self.game_canvas.delete('pause_text')
            self.is_game_running = True
            self.auto_move()
    
    def create_ui(self):
        if hasattr(self, 'joystick') and self.joystick:
            self.joystick.destroy()
        if hasattr(self, 'accel_button') and self.accel_button:
            self.accel_button.destroy()
        if hasattr(self, 'minimap') and self.minimap:
            self.minimap.destroy()
        if hasattr(self, 'leaderboard') and self.leaderboard:
            self.leaderboard.destroy()
        if hasattr(self, 'pause_button') and self.pause_button:
            self.pause_button.destroy()
        if hasattr(self, 'return_to_menu_button') and self.return_to_menu_button:
            self.return_to_menu_button.destroy()
        
        base_r = 120
        thumb_r = 50
        joystick_x = 50 + base_r + 20
        joystick_y = self.screen_height - 50 - base_r - 20
        
        self.joystick = JoystickWidget(
            self,
            x=joystick_x,
            y=joystick_y,
            base_radius=base_r,
            thumb_radius=thumb_r
        )
        self.joystick.set_direction_callback(self.on_joystick_move)
        
        btn_radius = 60
        btn_x = self.screen_width - 200 - btn_radius
        btn_y = self.screen_height - 200 - btn_radius
        
        self.accel_button = AccelerationButton(
            self,
            x=btn_x,
            y=btn_y,
            radius=btn_radius
        )
        self.accel_button.set_callbacks(
            press_callback=self.start_acceleration,
            release_callback=self.stop_acceleration
        )
        
        minimap_size = 180
        minimap_x = self.screen_width - minimap_size - 20
        minimap_y = 20
        self.minimap = MiniMap(
            self,
            x=minimap_x,
            y=minimap_y,
            size=minimap_size,
            world_w=self.world_width,
            world_h=self.world_height
        )
        
        return_button_size = 50
        pause_button_size = 50
        return_button_x = minimap_x - pause_button_size - return_button_size - 20
        return_button_y = minimap_y + (minimap_size - return_button_size) // 2 - 10
        
        self.return_to_menu_button = ReturnToMenuButton(
            self,
            x=return_button_x,
            y=return_button_y,
            size=return_button_size
        )
        self.return_to_menu_button.set_click_callback(self.return_to_main_menu)
        
        pause_button_x = minimap_x - pause_button_size - 10
        pause_button_y = minimap_y + (minimap_size - pause_button_size) // 2
        
        self.pause_button = PauseButton(
            self,
            x=pause_button_x,
            y=pause_button_y,
            size=pause_button_size
        )
        self.pause_button.set_pause_callback(self.toggle_pause)
        
        self.leaderboard = Leaderboard(
            self,
            x=20,
            y=20,
            width=220,
            height=400
        )
    
    def spawn_boss(self):
        side = choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            spawn_x = self.camera_x + randint(0, self.screen_width)
            spawn_y = self.camera_y - 100
        elif side == 'bottom':
            spawn_x = self.camera_x + randint(0, self.screen_width)
            spawn_y = self.camera_y + self.screen_height + 100
        elif side == 'left':
            spawn_x = self.camera_x - 100
            spawn_y = self.camera_y + randint(0, self.screen_height)
        else:
            spawn_x = self.camera_x + self.screen_width + 100
            spawn_y = self.camera_y + randint(0, self.screen_height)
        
        spawn_x = max(100, min(self.world_width - 100, spawn_x))
        spawn_y = max(100, min(self.world_height - 100, spawn_y))
        
        boss_length = 25
        angle_rad = math.radians(randint(0, 360))
        position = []
        for i in range(boss_length):
            seg_x = spawn_x - math.cos(angle_rad) * i * 20
            seg_y = spawn_y - math.sin(angle_rad) * i * 20
            position.append((seg_x, seg_y))
        
        if self.boss_current_phase == 2:
            speed = 12
            head_size = 65
            body_size = 45
        elif self.boss_current_phase == 3:
            speed = 15
            head_size = 70
            body_size = 50
        else:
            speed = 8
            head_size = 60
            body_size = 40
        
        self.boss = {
            'label': 'БОСС',
            'color': '#FF0000',
            'position': position,
            'direction_angle': randint(0, 360),
            'alive': True,
            'head_size': head_size,
            'body_size': body_size,
            'speed': speed,
            'eaten_apples': 999,
        }
        
        self.boss_active = True
        self.boss_appearance_time = time.time()
    
    def move_boss(self):
        if not self.boss or not self.boss['alive']:
            return
        
        if self.boss_respawn_timer > 0:
            self.boss_respawn_timer -= 0.05
            if self.boss_respawn_timer <= 0:
                self.spawn_boss()
            return
        
        player = self.get_player_snake()
        if not player:
            return
        
        head_x, head_y = self.boss['position'][-1]
        player_x, player_y = player['position'][-1]
        
        target_angle = math.degrees(math.atan2(player_y - head_y, player_x - head_x))
        dodge_angle = target_angle + randint(-30, 30)
        
        dist_to_player = math.hypot(player_x - head_x, player_y - head_y)
        if dist_to_player < 100 and len(player['position']) > len(self.boss['position']):
            dodge_angle = target_angle + 180 + randint(-40, 40)
        
        self.boss['direction_angle'] = dodge_angle % 360
        
        angle_rad = math.radians(self.boss['direction_angle'])
        speed = self.boss['speed']
        delta_x = speed * math.cos(angle_rad)
        delta_y = speed * math.sin(angle_rad)
        
        new_head = (head_x + delta_x, head_y + delta_y)
        new_head = (
            max(50, min(self.world_width - 50, new_head[0])),
            max(50, min(self.world_height - 50, new_head[1]))
        )
        
        self.boss['position'].append(new_head)
        if len(self.boss['position']) > 25:
            self.boss['position'].pop(0)
    
    def check_boss_collision_with_player(self):
        if not self.boss or not self.boss['alive']:
            return
        
        if self.boss_respawn_timer > 0:
            return
        
        player = self.get_player_snake()
        if not player:
            return
        
        if self.has_effect(player, 'shield'):
            return
        
        boss_head = self.boss['position'][-1]
        
        # Проверяем столкновение головы босса с хвостом игрока
        for i, segment in enumerate(player['position']):
            dist = math.hypot(boss_head[0] - segment[0], boss_head[1] - segment[1])
            if dist < (self.boss['head_size'] + self.square_size) * 0.5:
                self.boss_lives -= 1
                self.boss_active = False
                self.boss = None
                self.boss_current_phase += 1
                
                if self.boss_lives <= 0:
                    self.defeat_boss()
                else:
                    self.boss_respawn_timer = 3
                return
        
        player_head = player['position'][-1]
        dist = math.hypot(boss_head[0] - player_head[0], boss_head[1] - player_head[1])
        
        if dist < (self.boss['head_size'] + self.head_size) * 0.5:
            self.kill_snake(player)
            return
    
    def defeat_boss(self):
        self.player_coins += 100
        self.coins_earned_this_round += 100
        if self.quest_system:
            self.quest_system.quest_bosses_killed += 1
        self.boss = None
        self.boss_active = False
        self.boss_mode = False
        self.is_game_running = False
        self.stop_auto_move()
        
        if self.player_apple_count > self.best_score:
            self.best_score = self.player_apple_count
        
        if self.game_canvas:
            self.game_canvas.delete("all")
            self.game_canvas.create_rectangle(
                0, 0, self.screen_width, self.screen_height,
                fill='#000000'
            )
            self.game_canvas.create_text(
                self.screen_width // 2, self.screen_height // 2 - 50,
                text="БОСС ПОБЕЖДЁН!",
                font=("Arial", 20, "bold"),
                fill="#FFD700",
                anchor="center"
            )
            self.game_canvas.create_text(
                self.screen_width // 2, self.screen_height // 2 + 50,
                text="+100 💰",
                font=("Arial", 15, "bold"),
                fill="#FFD700",
                anchor="center"
            )
            self.game_canvas.create_text(
                self.screen_width // 2, self.screen_height // 2 + 120,
                text="Возврат в меню через 3 секунды...",
                font=("Arial", 4),
                fill="#888888",
                anchor="center"
            )
        
        self.after(3000, self.show_main_menu)
    
    def update_boss(self):
        if not self.boss_mode:
            return
        
        if self.pause_button and self.pause_button.is_paused:
            return
        
        if not self.boss_active:
            if self.boss_respawn_timer <= 0:
                self.boss_timer -= 0.05
                
                if self.boss_timer <= 0 and self.boss_lives > 0:
                    self.spawn_boss()
            else:
                self.boss_respawn_timer -= 0.05
        else:
            elapsed = time.time() - self.boss_appearance_time
            if elapsed >= self.boss_duration:
                self.boss_active = False
                self.boss = None
                self.boss_timer = 30
    
    def draw_boss(self):
        if not self.boss or not self.boss['alive']:
            return
        
        for pos in self.boss['position'][:-1]:
            sx, sy = self.world_to_screen(pos[0], pos[1])
            if self.is_on_screen(pos[0], pos[1], self.boss['body_size']):
                size = self.boss['body_size']
                self.game_canvas.create_oval(
                    sx-size/2, sy-size/2,
                    sx+size/2, sy+size/2,
                    fill="#CC0000", outline="#FF3333", width=2
                )
        
        head_x, head_y = self.boss['position'][-1]
        sx, sy = self.world_to_screen(head_x, head_y)
        if self.is_on_screen(head_x, head_y, self.boss['head_size']):
            size = self.boss['head_size']
            
            self.game_canvas.create_oval(
                sx-size/2, sy-size/2,
                sx+size/2, sy+size/2,
                fill="#FF0000", outline="#FF6666", width=3
            )
            
            phase_text = f"ФАЗА {self.boss_current_phase}"
            self.game_canvas.create_text(
                sx, sy - size - 20,
                text=phase_text,
                fill="#FF0000",
                font=("Arial", 8, "bold"),
                anchor="s"
            )
            
            hp_bar_width = 120
            hp_bar_height = 10
            hp_bar_y = sy - size - 35
            
            self.game_canvas.create_rectangle(
                sx - hp_bar_width//2, hp_bar_y,
                sx + hp_bar_width//2, hp_bar_y + hp_bar_height,
                fill="#333333", outline="#666666"
            )
            
            hp_percent = self.boss_lives / 3
            hp_fill_width = hp_bar_width * hp_percent
            hp_color = "#00FF00" if hp_percent > 0.66 else "#FFA500" if hp_percent > 0.33 else "#FF0000"
            
            self.game_canvas.create_rectangle(
                sx - hp_bar_width//2, hp_bar_y,
                sx - hp_bar_width//2 + hp_fill_width, hp_bar_y + hp_bar_height,
                fill=hp_color, outline=""
            )
            
            speed_text = f"Скорость: {self.boss['speed']}"
            self.game_canvas.create_text(
                sx, sy - size - 50,
                text=speed_text,
                fill="#FFD700",
                font=("Arial", 4, "bold"),
                anchor="s"
            )
    
    def draw_boss_timer_and_lives(self):
        if not self.boss_mode:
            return
        
        center_x = self.screen_width // 2
        
        info_width = 300
        info_height = 120
        info_x = center_x - info_width // 2
        info_y = 10
        
        self.game_canvas.create_rectangle(
            info_x, info_y,
            info_x + info_width, info_y + info_height,
            fill='#1a1a1a', outline='#FFD700', width=2
        )
        
        if not self.boss_active and self.boss_respawn_timer <= 0:
            timer_text = f"Босс через: {int(self.boss_timer)}с"
            timer_color = "#FFD700"
        elif self.boss_respawn_timer > 0:
            timer_text = f"Босс возрождается: {int(self.boss_respawn_timer)}с"
            timer_color = "#FFA500"
        else:
            elapsed = time.time() - self.boss_appearance_time
            remaining = max(0, self.boss_duration - elapsed)
            timer_text = f"Босс исчезнет через: {int(remaining)}с"
            timer_color = "#FF0000"
        
        self.game_canvas.create_text(
            center_x, info_y + 25,
            text=timer_text,
            fill=timer_color,
            font=("Arial", 3, "bold"),
            anchor="center"
        )
        
        hp_text = "HP босса:"
        self.game_canvas.create_text(
            center_x, info_y + 55,
            text=hp_text,
            fill="#FFFFFF",
            font=("Arial", 3, "bold"),
            anchor="center"
        )
        
        heart_size = 30
        heart_spacing = 40
        hearts_total_width = 3 * heart_spacing
        hearts_start_x = center_x - hearts_total_width // 2 + heart_spacing // 2
        hearts_y = info_y + 90
        
        for i in range(3):
            heart_x = hearts_start_x + i * heart_spacing
            
            if i < self.boss_lives:
                heart_color = "#FF0000"
                outline_color = "#CC0000"
            else:
                heart_color = "#333333"
                outline_color = "#666666"
            
            self.game_canvas.create_oval(
                heart_x - heart_size//4, hearts_y - heart_size//2,
                heart_x + heart_size//4, hearts_y,
                fill=heart_color, outline=outline_color, width=2
            )
            self.game_canvas.create_oval(
                heart_x - heart_size//2, hearts_y - heart_size//2,
                heart_x + heart_size//4, hearts_y,
                fill=heart_color, outline=outline_color, width=2
            )
            self.game_canvas.create_polygon(
                heart_x - heart_size//2, hearts_y - heart_size//3,
                heart_x + heart_size//2, hearts_y - heart_size//3,
                heart_x, hearts_y + heart_size//3,
                fill=heart_color, outline=outline_color, width=2
            )
        
        phase_text = f"ФАЗА {self.boss_current_phase}"
        self.game_canvas.create_text(
            center_x, info_y + info_height - 10,
            text=phase_text,
            fill="#FFD700",
            font=("Arial", 3, "bold"),
            anchor="center"
        )
    
    def on_joystick_move(self, dx, dy, angle=None):
        if angle is not None:
            self.joystick_active = True
            self.joystick_angle = angle
        else:
            self.joystick_active = False
            self.joystick_angle = None
    
    def on_key_press(self, event):
        if not self.is_game_running:
            return
        player = self.get_player_snake()
        if not player or not player['alive']:
            return
        
        key = event.keysym
        
        if key == 'Right' or key == 'd':
            player['direction_angle'] = 0
            self.joystick_active = False
        elif key == 'Left' or key == 'a':
            player['direction_angle'] = 180
            self.joystick_active = False
        elif key == 'Up' or key == 'w':
            player['direction_angle'] = 270
            self.joystick_active = False
        elif key == 'Down' or key == 's':
            player['direction_angle'] = 90
            self.joystick_active = False
        elif key == 'space':
            if self.player_apple_count > 0:
                self.start_acceleration()
        
        if self.quest_system and key in ['Right', 'd', 'Left', 'a', 'Up', 'w', 'Down', 's']:
            self.quest_system.track_direction_change(player['direction_angle'])
    
    def on_key_release(self, event):
        if event.keysym == 'space':
            self.stop_acceleration()
    
    def get_player_snake(self):
        for snake in self.snakes:
            if snake['label'] == 'Игрок' and snake['alive']:
                return snake
        return None
    
    def generate_patrol_points(self, center_x, center_y):
        points = []
        for i in range(8):
            angle = (2 * math.pi * i) / 8
            dist = randint(300, 800)
            px = center_x + math.cos(angle) * dist
            py = center_y + math.sin(angle) * dist
            px = max(100, min(self.world_width - 100, px))
            py = max(100, min(self.world_height - 100, py))
            points.append((px, py))
        return points
    
    def world_to_screen(self, world_x, world_y):
        sx = world_x - self.camera_x
        sy = world_y - self.camera_y
        return sx, sy
    
    def is_on_screen(self, world_x, world_y, margin=50):
        sx, sy = self.world_to_screen(world_x, world_y)
        return (-margin < sx < self.screen_width + margin and 
                -margin < sy < self.screen_height + margin)
    
    def update_camera(self):
        player = self.get_player_snake()
        if player and player['position']:
            px, py = player['position'][-1]
            self.camera_x = px - self.screen_width / 2
            self.camera_y = py - self.screen_height / 2
            
            self.camera_x = max(0, min(self.world_width - self.screen_width, self.camera_x))
            self.camera_y = max(0, min(self.world_height - self.screen_height, self.camera_y))
    
    def draw_grid(self):
        grid_size = 100
        start_x = int(self.camera_x // grid_size) * grid_size
        start_y = int(self.camera_y // grid_size) * grid_size
        end_x = int(self.camera_x + self.screen_width) + grid_size
        end_y = int(self.camera_y + self.screen_height) + grid_size
        
        for x in range(start_x, end_x, grid_size):
            if 0 <= x <= self.world_width:
                sx, _ = self.world_to_screen(x, 0)
                self.game_canvas.create_line(sx, 0, sx, self.screen_height, 
                                             fill="#151515", width=0.5)
        
        for y in range(start_y, end_y, grid_size):
            if 0 <= y <= self.world_height:
                _, sy = self.world_to_screen(0, y)
                self.game_canvas.create_line(0, sy, self.screen_width, sy, 
                                             fill="#151515", width=0.5)
    
    def draw_leader_indicator(self):
        if self.boss_mode:
            return
        
        leader = self.find_leader()
        if not leader or not leader['position']:
            return
        
        player = self.get_player_snake()
        if player == leader:
            return
        
        leader_x, leader_y = leader['position'][-1]
        
        margin = 50
        if (self.camera_x - margin < leader_x < self.camera_x + self.screen_width + margin and
            self.camera_y - margin < leader_y < self.camera_y + self.screen_height + margin):
            return
        
        screen_center_x = self.screen_width / 2
        screen_center_y = self.screen_height / 2
        
        dx = leader_x - (self.camera_x + screen_center_x)
        dy = leader_y - (self.camera_y + screen_center_y)
        
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
        dx_norm = dx / length
        dy_norm = dy / length
        
        arrow_size = 25
        
        intersections = []
        
        if dx_norm < 0:
            t = (arrow_size - screen_center_x) / dx_norm
            y_intersect = screen_center_y + t * dy_norm
            if arrow_size <= y_intersect <= self.screen_height - arrow_size:
                angle_deg = math.degrees(math.atan2(-dy_norm, -dx_norm))
                intersections.append((arrow_size, y_intersect, angle_deg))
        
        if dx_norm > 0:
            t = (self.screen_width - arrow_size - screen_center_x) / dx_norm
            y_intersect = screen_center_y + t * dy_norm
            if arrow_size <= y_intersect <= self.screen_height - arrow_size:
                angle_deg = math.degrees(math.atan2(-dy_norm, -dx_norm))
                intersections.append((self.screen_width - arrow_size, y_intersect, angle_deg))
        
        if dy_norm < 0:
            t = (arrow_size - screen_center_y) / dy_norm
            x_intersect = screen_center_x + t * dx_norm
            if arrow_size <= x_intersect <= self.screen_width - arrow_size:
                angle_deg = math.degrees(math.atan2(-dy_norm, -dx_norm))
                intersections.append((x_intersect, arrow_size, angle_deg))
        
        if dy_norm > 0:
            t = (self.screen_height - arrow_size - screen_center_y) / dy_norm
            x_intersect = screen_center_x + t * dx_norm
            if arrow_size <= x_intersect <= self.screen_width - arrow_size:
                angle_deg = math.degrees(math.atan2(-dy_norm, -dx_norm))
                intersections.append((x_intersect, self.screen_height - arrow_size, angle_deg))
        
        if not intersections:
            if dx < 0 and dy < 0:
                corner_x, corner_y = arrow_size, arrow_size
                base_angle = 225
            elif dx > 0 and dy < 0:
                corner_x, corner_y = self.screen_width - arrow_size, arrow_size
                base_angle = 315
            elif dx < 0 and dy > 0:
                corner_x, corner_y = arrow_size, self.screen_height - arrow_size
                base_angle = 135
            else:
                corner_x, corner_y = self.screen_width - arrow_size, self.screen_height - arrow_size
                base_angle = 45
            
            tri_size = 20
            angle_rad = math.radians(base_angle)
            self.game_canvas.create_polygon(
                corner_x + math.cos(angle_rad) * tri_size,
                corner_y - math.sin(angle_rad) * tri_size,
                corner_x + math.cos(angle_rad + 2.5) * tri_size * 0.7,
                corner_y - math.sin(angle_rad + 2.5) * tri_size * 0.7,
                corner_x + math.cos(angle_rad - 2.5) * tri_size * 0.7,
                corner_y - math.sin(angle_rad - 2.5) * tri_size * 0.7,
                fill="#FFD700", outline="#FF8C00", width=2
            )
            return
        
        for x, y, angle_deg in intersections:
            base_angle = math.radians(angle_deg)
            tri_size = 40
            
            self.game_canvas.create_polygon(
                x + math.cos(base_angle) * tri_size,
                y - math.sin(base_angle) * tri_size,
                x + math.cos(base_angle + 2.5) * tri_size * 0.7,
                y - math.sin(base_angle + 2.5) * tri_size * 0.7,
                x + math.cos(base_angle - 2.5) * tri_size * 0.7,
                y - math.sin(base_angle - 2.5) * tri_size * 0.7,
                fill="#FFD700", outline="#FF8C00", width=2
            )
    
    def draw_snake(self, snake):
        if not snake['position']:
            return
        
        birth_time = snake.get('birth_time', self.round_start_time)
        now = time.time()
        
        # Восстанавливаем цвет после окончания иммунитета
        if now >= snake.get('immune_until', 0) and snake.get('original_color'):
            if snake['color'] != snake['original_color']:
                snake['color'] = snake['original_color']
            if 'phase_effect' in snake:
                snake['phase_effect'] = False
        
        # Цвет для фазы (серая неуязвимая)
        if snake.get('phase_effect', False) or now < snake.get('immune_until', 0):
            temp_color = "#A9A9A9"
        else:
            temp_color = snake['color']
        
        is_invisible = snake.get('invisible', False) and snake['label'] != 'Игрок'
        
        for pos in snake['position'][:-1]:
            if self.is_on_screen(pos[0], pos[1], self.head_size):
                sx, sy = self.world_to_screen(pos[0], pos[1])
                size = self.square_size
                if is_invisible:
                    self.game_canvas.create_oval(
                        sx-size/2, sy-size/2, 
                        sx+size/2, sy+size/2,
                        fill=temp_color, outline="", stipple='gray50'
                    )
                else:
                    self.game_canvas.create_oval(
                        sx-size/2, sy-size/2, 
                        sx+size/2, sy+size/2,
                        fill=temp_color, outline=""
                    )
        
        head_x, head_y = snake['position'][-1]
        if not self.is_on_screen(head_x, head_y, self.head_size):
            return
            
        sx, sy = self.world_to_screen(head_x, head_y)
        
        if self.has_effect(snake, 'shield'):
            shield_size = self.head_size * 1.8
            self.game_canvas.create_oval(
                sx - shield_size/2, sy - shield_size/2,
                sx + shield_size/2, sy + shield_size/2,
                fill='', outline='#4488FF', width=3
            )
            pulse = math.sin(time.time() * 5) * 3
            self.game_canvas.create_oval(
                sx - shield_size/2 - pulse, sy - shield_size/2 - pulse,
                sx + shield_size/2 + pulse, sy + shield_size/2 + pulse,
                fill='', outline='#88BBFF', width=1
            )
        
        if self.has_effect(snake, 'speed') and snake['label'] == 'Игрок':
            angle_rad = math.radians(snake['direction_angle'])
            for i in range(3):
                offset = (i + 1) * 15
                line_x = sx - math.cos(angle_rad) * offset
                line_y = sy - math.sin(angle_rad) * offset
                line_len = 20
                self.game_canvas.create_line(
                    line_x, line_y,
                    line_x - math.cos(angle_rad) * line_len,
                    line_y - math.sin(angle_rad) * line_len,
                    fill='#00FF00', width=2
                )
        
        if self.has_effect(snake, 'magnet') and snake['label'] == 'Игрок':
            magnet_radius = 200
            magnet_sx, magnet_sy = self.world_to_screen(head_x - magnet_radius, head_y - magnet_radius)
            magnet_ex, magnet_ey = self.world_to_screen(head_x + magnet_radius, head_y + magnet_radius)
            
            self.game_canvas.create_oval(
                magnet_sx, magnet_sy,
                magnet_ex, magnet_ey,
                fill='', outline='#FF44FF', width=1, dash=(5, 5)
            )
        
        if snake['label'] == 'Игрок':
            if self.player_skin_key and self.player_skin:
                self.draw_animal_head(sx, sy, snake)
            else:
                size = self.head_size
                if is_invisible:
                    self.game_canvas.create_oval(
                        sx-size/2, sy-size/2,
                        sx+size/2, sy+size/2,
                        fill="#00ffff", outline="", stipple='gray50'
                    )
                else:
                    self.game_canvas.create_oval(
                        sx-size/2, sy-size/2,
                        sx+size/2, sy+size/2,
                        fill=temp_color, outline=""
                    )
            
            leader = self.find_leader()
            triangle_size = self.head_size * 0.75
            
            if snake == leader and not self.boss_mode:
                base_y = sy - self.head_size * 4
            else:
                base_y = sy - self.head_size
            
            self.game_canvas.create_polygon(
                sx, base_y - triangle_size,
                sx - triangle_size, base_y,
                sx + triangle_size, base_y,
                fill="blue", outline="white", width=2
            )
        else:
            if is_invisible:
                snake_copy = snake.copy()
                snake_copy['invisible'] = True
                self.draw_animal_head(sx, sy, snake_copy)
            else:
                self.draw_animal_head(sx, sy, snake)
        
        if not is_invisible:
            self.game_canvas.create_text(
                sx, sy - self.head_size,
                text=snake['label'], 
                fill="white", 
                anchor="s",
                font=("Arial", 8)
            )
        
        leader = self.find_leader()
        if snake == leader and not self.boss_mode and not is_invisible:
            crown_size = self.head_size * 1.5
            self.game_canvas.create_polygon(
                sx-crown_size/2, sy-self.head_size*4-crown_size/2,
                sx+crown_size/2, sy-self.head_size*4-crown_size/2,
                sx, sy-self.head_size*4-crown_size,
                fill="#FFD700", outline="#FFA500", width=2
            )
        
        # Эффект фазы (мерцание)
        if snake.get('phase_effect', False) or now < snake.get('immune_until', 0):
            pulse = (math.sin(now * 10) + 1) / 2
            alpha = int(50 + pulse * 50)
            self.game_canvas.create_oval(
                sx - self.head_size/2 - 5, sy - self.head_size/2 - 5,
                sx + self.head_size/2 + 5, sy + self.head_size/2 + 5,
                fill='', outline=f'#{alpha:02x}{alpha:02x}{alpha:02x}', width=2
            )
    
    def draw_all(self):
        if not self.game_canvas:
            return
        
        self.game_canvas.delete("all")
        
        self.update_camera()
        self.draw_grid()
        self.draw_world_borders()  # Рисуем красные границы мира
        
        player = self.get_player_snake()
        sorted_snakes = [s for s in self.snakes if s['alive']]
        if player and player['position']:
            px, py = player['position'][-1]
            sorted_snakes.sort(key=lambda s: 
                math.hypot(s['position'][-1][0] - px, s['position'][-1][1] - py) 
                if s['position'] else 0,
                reverse=True)
        
        for snake in sorted_snakes:
            self.draw_snake(snake)
        
        self.draw_apples()
        self.draw_golden_apples()
        self.draw_effect_apples()
        
        self.draw_boss()
        self.draw_boss_timer_and_lives()
        
        self.update_score()
        self.draw_effect_icons()
        
        if self.quest_system and not self.boss_mode:
            self.quest_system.draw_quest(self.game_canvas, self.screen_width)
        
        if hasattr(self, 'minimap') and self.minimap:
            self.minimap.update(
                self.get_player_snake(),
                self.snakes,
                self.apples,
                self.golden_apples,
                self.effect_apples,
                self.screen_width,
                self.screen_height,
                self.camera_x,
                self.camera_y,
                boss=self.boss
            )
        
        if hasattr(self, 'leaderboard') and self.leaderboard:
            self.leaderboard.update(self.snakes)
        
        self.draw_leader_indicator()
        
        if hasattr(self, 'pause_button') and self.pause_button and self.pause_button.is_paused:
            self.game_canvas.create_rectangle(
                0, 0, self.screen_width, self.screen_height,
                fill='black', stipple='gray50', tags='pause_overlay'
            )
            self.game_canvas.create_text(
                self.screen_width // 2, self.screen_height // 2,
                text="ПАУЗА",
                font=("Arial", 20, "bold"),
                fill="white",
                tags='pause_text'
            )
    
    def update_score(self):
        if self.boss_mode:
            score_text = f"Яблок: {self.player_apple_count} | Босс режим"
        else:
            score_text = f"Яблок: {self.player_apple_count}"
        self.game_canvas.create_text(250, 430, text=score_text,
                                     font=("Arial", 6, "bold"), fill="white", anchor="n")
    
    def spawn_apples(self):
        max_apples_to_add = 10
        added = 0
        
        while len(self.apples) < self.apple_max and added < max_apples_to_add:
            x = randint(50, self.world_width - 50)
            y = randint(50, self.world_height - 50)
            
            too_close = False
            for apple in self.apples[-50:]:
                if math.hypot(apple[0] - x, apple[1] - y) < self.apple_size * 2:
                    too_close = True
                    break
            
            if not too_close:
                self.apples.append((x, y))
                added += 1
    
    def draw_apples(self):
        for x, y in self.apples:
            if self.is_on_screen(x, y, self.apple_size):
                sx, sy = self.world_to_screen(x, y)
                size = self.apple_size
                self.game_canvas.create_oval(
                    sx-size/2, sy-size/2,
                    sx+size/2, sy+size/2,
                    fill="red", outline="#ff6666", width=1
                )
    
    def draw_golden_apples(self):
        for x, y in self.golden_apples:
            if self.is_on_screen(x, y, self.golden_apple_size):
                sx, sy = self.world_to_screen(x, y)
                size = self.golden_apple_size
                
                self.game_canvas.create_oval(
                    sx-size/2, sy-size/2,
                    sx+size/2, sy+size/2,
                    fill="#FFD700", outline="#FF8C00", width=2
                )
    
    def check_collision_with_apple(self, snake):
        head_x, head_y = snake['position'][-1]
        
        magnet_radius = 0
        if self.has_effect(snake, 'magnet'):
            magnet_radius = 200
        
        for idx, (apple_x, apple_y) in enumerate(self.apples):
            distance = math.hypot(apple_x-head_x, apple_y-head_y)
            if magnet_radius > 0 and distance < magnet_radius:
                if distance > 10:
                    dx = (head_x - apple_x) / distance * 15
                    dy = (head_y - apple_y) / distance * 15
                    self.apples[idx] = (apple_x + dx, apple_y + dy)
            if distance <= self.head_size:
                return ('normal', idx)
        
        for idx, (apple_x, apple_y) in enumerate(self.golden_apples):
            distance = math.hypot(apple_x-head_x, apple_y-head_y)
            if magnet_radius > 0 and distance < magnet_radius:
                if distance > 10:
                    dx = (head_x - apple_x) / distance * 10
                    dy = (head_y - apple_y) / distance * 10
                    self.golden_apples[idx] = (apple_x + dx, apple_y + dy)
            if distance <= self.head_size + self.golden_apple_size/2:
                return ('golden', idx)
        
        return None
    
    def handle_apple_collision(self, snake):
        if snake['label'] != 'Игрок':
            self._apple_check_counter += 1
            if self._apple_check_counter % 3 != 0:
                return False
        
        if self.check_effect_apple_collision(snake):
            return True
        
        collision = self.check_collision_with_apple(snake)
        if collision is not None:
            apple_type, idx = collision
            
            if apple_type == 'normal':
                del self.apples[idx]
                snake['eaten_apples'] += 1
                self.total_apples_eaten += 1
                
                if self.total_apples_eaten >= self.effect_apple_threshold and not self.boss_mode:
                    self.total_apples_eaten = 0
                    self.spawn_effect_apple()
                
                self.spawn_apples()
                
                if snake['label'] == 'Игрок':
                    self.player_apple_count += 1
                    if self.quest_system:
                        self.quest_system.quest_apples_eaten += 1
                
                if snake.get('memory') is not None:
                    snake['memory'].append(('food_found', snake['position'][-1], time.time()))
                return True
                
            elif apple_type == 'golden':
                del self.golden_apples[idx]
                for _ in range(3):
                    snake['eaten_apples'] += 1
                    if snake['label'] == 'Игрок':
                        self.player_apple_count += 1
                        if self.quest_system:
                            self.quest_system.quest_apples_eaten += 1
                
                if snake['label'] == 'Игрок':
                    self.player_coins += 1
                    self.coins_earned_this_round += 1
                    if self.quest_system:
                        self.quest_system.quest_golden_apples_eaten += 1
                
                if snake.get('memory') is not None:
                    snake['memory'].append(('golden_found', snake['position'][-1], time.time()))
                return True
        return False
    
    def update_bot_strategy(self, snake):
        if not snake['alive'] or snake['label'] == 'Игрок':
            return
        
        player = self.get_player_snake()
        if player and self.has_effect(player, 'freeze'):
            if 'freeze_slow' not in snake:
                snake['freeze_slow'] = True
        else:
            snake['freeze_slow'] = False
        
        if snake.get('freeze_slow') and random() < 0.7:
            return
        
        head_x, head_y = snake['position'][-1]
        my_length = len(snake['position'])
        personality = snake['personality']
        
        threats = []
        preys = []
        foods = []
        golden_foods = []
        effect_foods = []
        
        for other in self.snakes:
            if other == snake or not other['alive']:
                continue
            
            if other.get('invisible', False):
                continue
                
            other_head_x, other_head_y = other['position'][-1]
            dist = math.hypot(head_x - other_head_x, head_y - other_head_y)
            
            if dist > 800:
                continue
                
            if len(other['position']) > my_length:
                threats.append((other, dist))
            elif len(other['position']) < my_length:
                preys.append((other, dist))
        
        for apple in self.apples:
            dist = math.hypot(apple[0] - head_x, apple[1] - head_y)
            if dist < 600:
                foods.append((apple, dist))
        
        for apple in self.golden_apples:
            dist = math.hypot(apple[0] - head_x, apple[1] - head_y)
            if dist < 800:
                golden_foods.append((apple, dist))
        
        for effect_apple in self.effect_apples:
            dist = math.hypot(effect_apple.x - head_x, effect_apple.y - head_y)
            if dist < 700:
                effect_foods.append(((effect_apple.x, effect_apple.y), dist))
        
        threats.sort(key=lambda x: x[1])
        preys.sort(key=lambda x: x[1])
        foods.sort(key=lambda x: x[1])
        golden_foods.sort(key=lambda x: x[1])
        effect_foods.sort(key=lambda x: x[1])
        
        if effect_foods and effect_foods[0][1] < 400:
            snake['target'] = effect_foods[0][0]
            snake['strategy'] = 'searching_effect'
            return
        
        if golden_foods:
            if personality == 'aggressive' and golden_foods[0][1] < 500:
                snake['target'] = golden_foods[0][0]
                snake['strategy'] = 'searching_golden'
                return
            elif golden_foods[0][1] < 400:
                snake['target'] = golden_foods[0][0]
                snake['strategy'] = 'searching_golden'
                return
        
        caution_multiplier = 2.0 if personality == 'cautious' else 1.0
        if threats and threats[0][1] < 250 * caution_multiplier:
            snake['strategy'] = 'fleeing'
            threat = threats[0][0]
            flee_angle = math.atan2(
                head_y - threat['position'][-1][1],
                head_x - threat['position'][-1][0]
            )
            target_x = head_x + math.cos(flee_angle) * 600
            target_y = head_y + math.sin(flee_angle) * 600
            snake['target'] = (
                max(100, min(self.world_width - 100, target_x)),
                max(100, min(self.world_height - 100, target_y))
            )
            return
        
        aggression_multiplier = 1.5 if personality == 'aggressive' else 1.0
        if preys and preys[0][1] < 250 * aggression_multiplier:
            snake['strategy'] = 'attacking'
            prey = preys[0][0]
            snake['target'] = prey['position'][-1]
            return
        
        if foods:
            snake['target'] = foods[0][0] if random() < 0.7 else foods[randint(0, len(foods)-1)][0]
            snake['strategy'] = 'searching_food'
            return
        
        if len(snake.get('patrol_points', [])) > 0:
            snake['strategy'] = 'patrolling'
            target = snake['patrol_points'][snake['patrol_index']]
            snake['target'] = target
            if math.hypot(head_x - target[0], head_y - target[1]) < 60:
                snake['patrol_index'] = (snake['patrol_index'] + 1) % len(snake['patrol_points'])
            return
        
        snake['strategy'] = 'exploring'
        if snake['target'] is None or random() < 0.02:
            snake['target'] = (
                randint(100, self.world_width - 100),
                randint(100, self.world_height - 100)
            )
    
    def steer_towards_target(self, snake):
        if 'target' not in snake or snake['target'] is None:
            return
        
        head_x, head_y = snake['position'][-1]
        target_x, target_y = snake['target']
        current_angle = snake['direction_angle']
        
        ideal_angle = math.degrees(math.atan2(target_y - head_y, target_x - head_x))
        
        turn_speed = 5
        if snake['strategy'] in ['searching_golden', 'searching_effect']:
            turn_speed = 8
        
        angle_diff = (ideal_angle - current_angle + 180) % 360 - 180
        
        if abs(angle_diff) > 150:
            new_angle = ideal_angle
        elif angle_diff > turn_speed:
            new_angle = current_angle + turn_speed
        elif angle_diff < -turn_speed:
            new_angle = current_angle - turn_speed
        else:
            new_angle = ideal_angle
        
        snake['direction_angle'] = new_angle % 360
    
    def avoid_obstacles(self, snake):
        head_x, head_y = snake['position'][-1]
        current_angle = snake['direction_angle']
        
        rad = math.radians(current_angle)
        look_ahead = 100
        check_x = head_x + math.cos(rad) * look_ahead
        check_y = head_y + math.sin(rad) * look_ahead
        
        if not (60 < check_x < self.world_width - 60 and 60 < check_y < self.world_height - 60):
            for test_angle in range(0, 360, 30):
                test_rad = math.radians(test_angle)
                test_x = head_x + math.cos(test_rad) * look_ahead
                test_y = head_y + math.sin(test_rad) * look_ahead
                if 60 < test_x < self.world_width - 60 and 60 < test_y < self.world_height - 60:
                    angle_diff = (test_angle - current_angle + 180) % 360 - 180
                    if angle_diff > 0:
                        snake['direction_angle'] = (current_angle + 15) % 360
                    else:
                        snake['direction_angle'] = (current_angle - 15) % 360
                    return
            snake['direction_angle'] = (current_angle + 45) % 360
    
    def check_collisions(self, snake):
        head_x, head_y = snake['position'][-1]
        
        # Проверка на фазу (неуязвимость и прохождение сквозь других)
        if snake.get('phase_effect', False) or time.time() < snake.get('immune_until', 0):
            # Проверяем только границы мира
            if (head_x < 30 or head_x > self.world_width - 30 or
                head_y < 30 or head_y > self.world_height - 30):
                return True
            return False
        
        if self.has_effect(snake, 'ghost'):
            pass
        
        # Проверка границ карты
        if (head_x < 30 or head_x > self.world_width - 30 or
            head_y < 30 or head_y > self.world_height - 30):
            return True
        
        if self.has_effect(snake, 'shield'):
            return False
        
        if snake.get('invisible', False):
            return False
        
        for other_snake in self.snakes:
            if other_snake != snake and other_snake['alive']:
                # Если другая змея в фазе - можно проходить сквозь
                if other_snake.get('phase_effect', False) or time.time() < other_snake.get('immune_until', 0):
                    continue
                    
                if other_snake.get('invisible', False) and other_snake['label'] != 'Игрок':
                    continue
                    
                other_head_x, other_head_y = other_snake['position'][-1]
                if math.hypot(head_x - other_head_x, head_y - other_head_y) > 300:
                    continue
                    
                for ox, oy in other_snake['position']:
                    distance = math.hypot(head_x - ox, head_y - oy)
                    if distance <= self.head_size * 0.8:
                        return True
        return False
    
    def drop_apples_on_death(self, snake):
        if not snake['position']:
            return
        
        head_x, head_y = snake['position'][-1]
        golden_apples_to_drop = min(snake['eaten_apples'], 10)
        
        for i in range(golden_apples_to_drop):
            angle = (2 * math.pi * i) / max(1, golden_apples_to_drop) + random() * 0.5
            dist = self.golden_apple_size * 2 + random() * 40
            apple_x = int(head_x + math.cos(angle) * dist)
            apple_y = int(head_y + math.sin(angle) * dist)
            apple_x = max(50, min(self.world_width - 50, apple_x))
            apple_y = max(50, min(self.world_height - 50, apple_y))
            self.golden_apples.append((apple_x, apple_y))
    
    def get_player_rank(self):
        alive_snakes = [(s['label'], s['eaten_apples']) for s in self.snakes if s['alive']]
        alive_snakes.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, apples) in enumerate(alive_snakes):
            if name == 'Игрок':
                return i + 1, len(alive_snakes)
        return 0, 0
    
    def show_results_screen(self):
        if not self.game_canvas:
            return
        
        self.game_canvas.delete("all")
        self.game_canvas.configure(bg='#0a0a0a')
        
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.game_canvas.create_rectangle(
            0, 0, self.screen_width, self.screen_height,
            fill='#000000',
            stipple='gray25'
        )
        
        self.game_canvas.create_text(
            center_x, center_y - 200,
            text="ПОРАЖЕНИЕ!",
            font=("Arial", 15, "bold"),
            fill="#FF3333",
            anchor="center"
        )
        
        rank, total_alive = self.get_player_rank()
        
        y_start = center_y - 100
        
        if rank > 0:
            medal_text = ""
            if rank == 1:
                medal_text = "🥇"
            elif rank == 2:
                medal_text = "🥈"
            elif rank == 3:
                medal_text = "🥉"
            
            self.game_canvas.create_text(
                center_x, y_start,
                text=f"Место: {medal_text} {rank}/{total_alive}",
                font=("Arial", 12, "bold"),
                fill="#FFD700",
                anchor="center"
            )
        
        y_start += 50
        self.game_canvas.create_text(
            center_x, y_start,
            text=f"Собрано яблок: {self.player_apple_count}",
            font=("Arial", 5, "bold"),
            fill="#FFFFFF",
            anchor="center"
        )
        
        y_start += 30
        self.game_canvas.create_text(
            center_x, y_start,
            text=f"Очки: {self.player_apple_count}",
            font=("Arial", 6, "bold"),
            fill="#87CEEB",
            anchor="center"
        )
        
        y_start += 40
        self.game_canvas.create_text(
            center_x, y_start,
            text=f"Монет за раунд: +{self.coins_earned_this_round} 💰",
            font=("Arial", 5, "bold"),
            fill="#FFD700",
            anchor="center"
        )
        
        y_start += 30
        self.game_canvas.create_text(
            center_x, y_start,
            text=f"Баланс: {self.player_coins} 💰",
            font=("Arial", 6),
            fill="#AAAAAA",
            anchor="center"
        )
        
        y_start += 80
        self.game_canvas.create_text(
            center_x, y_start,
            text="Возврат в главное меню через 4 секунды...",
            font=("Arial", 4),
            fill="#888888",
            anchor="center"
        )
        
        self.game_canvas.update()
    
    def game_over(self):
        self.is_game_running = False
        self.boss_mode = False
        self.stop_auto_move()
        
        if self.player_apple_count > self.best_score:
            self.best_score = self.player_apple_count
        
        if hasattr(self, 'joystick') and self.joystick:
            self.joystick.destroy()
            self.joystick = None
        
        if hasattr(self, 'accel_button') and self.accel_button:
            self.accel_button.destroy()
            self.accel_button = None
        
        if hasattr(self, 'minimap') and self.minimap:
            self.minimap.destroy()
            self.minimap = None
        
        if hasattr(self, 'leaderboard') and self.leaderboard:
            self.leaderboard.destroy()
            self.leaderboard = None
        
        if hasattr(self, 'pause_button') and self.pause_button:
            self.pause_button.destroy()
            self.pause_button = None
        
        if hasattr(self, 'return_to_menu_button') and self.return_to_menu_button:
            self.return_to_menu_button.destroy()
            self.return_to_menu_button = None
        
        if self.game_canvas:
            self.show_results_screen()
            self.after(4000, self.show_main_menu)
    
    def kill_snake(self, snake):
        if not snake['alive']:
            return
        
        snake['alive'] = False
        
        if snake['label'] != 'Игрок' and self.quest_system:
            self.quest_system.quest_enemies_killed += 1
        
        if snake['label'] == 'Игрок':
            self.after(50, self.game_over)
        else:
            self.drop_apples_on_death(snake)
            self.respawn_snake(snake)
    
    def respawn_snake(self, dead_snake):
        player = self.get_player_snake()
        while True:
            start_x = randint(200, self.world_width - 200)
            start_y = randint(200, self.world_height - 200)
            if player and player['position']:
                dist = math.hypot(start_x - player['position'][-1][0], 
                                  start_y - player['position'][-1][1])
                if dist > 600:
                    break
            else:
                break
        
        personality = choice(['hunter', 'collector', 'aggressive', 'cautious'])
        skin_key = choice(list(self.ANIMAL_SKINS.keys()))
        skin = self.ANIMAL_SKINS[skin_key]
        
        new_snake = {
            'label': dead_snake['label'],
            'color': '#808080',
            'original_color': skin['head_color'],
            'position': [(start_x, start_y)],
            'direction_angle': randint(0, 360),
            'eaten_apples': 0,
            'alive': True,
            'strategy': 'exploring',
            'target': None,
            'acceleration_cooldown': 0,
            'immune_until': time.time() + 3,
            'birth_time': time.time(),
            'strategy_update_counter': 0,
            'personality': personality,
            'memory': deque(maxlen=30),
            'territory_center': (start_x, start_y),
            'patrol_points': self.generate_patrol_points(start_x, start_y),
            'patrol_index': 0,
            'skin': skin,
            'skin_key': skin_key,
            'active_effects': {},
            'phase_effect': True
        }
        self.snakes.append(new_snake)
        
        self.after(3000, lambda: self.restore_snake_color(new_snake))
    
    def restore_snake_color(self, snake):
        if snake['alive'] and 'original_color' in snake:
            snake['color'] = snake['original_color']
            snake['phase_effect'] = False
    
    def move_snake(self, snake, speed=5):
        if self.has_effect(snake, 'speed'):
            speed = int(speed * 1.5)
        
        if snake['label'] != 'Игрок':
            player = self.get_player_snake()
            if player and self.has_effect(player, 'freeze'):
                speed = max(1, int(speed * 0.5))
        
        if self.has_effect(snake, 'invisibility'):
            snake['invisible'] = True
        else:
            snake['invisible'] = False
        
        if snake['label'] == 'Игрок' and self.joystick_active and self.joystick_angle is not None:
            old_angle = snake['direction_angle']
            snake['direction_angle'] = self.joystick_angle
            
            if self.quest_system and old_angle != snake['direction_angle']:
                self.quest_system.track_direction_change(snake['direction_angle'])
        
        angle_rad = math.radians(snake['direction_angle'])
        delta_x = speed * math.cos(angle_rad)
        delta_y = speed * math.sin(angle_rad)
        
        head_x, head_y = snake['position'][-1]
        new_head_pos = (head_x + delta_x, head_y + delta_y)
        
        if snake['label'] == 'Игрок' and self.quest_system:
            self.quest_system.track_movement(new_head_pos)
        
        if self.check_collisions(snake):
            self.kill_snake(snake)
            return
        
        snake['position'].append(new_head_pos)
        
        ate_apple = self.handle_apple_collision(snake)
        
        if not ate_apple:
            if len(snake['position']) > 1:
                snake['position'].pop(0)
    
    def auto_move(self):
        if self.is_game_running:
            self._frame_counter += 1
            
            if self._frame_counter % 10 == 0:
                self.clean_expired_effects()
            
            self.effect_spawn_timer += 1
            if self.effect_spawn_timer >= 300 and not self.boss_mode:
                self.effect_spawn_timer = 0
                if random() < 0.3:
                    self.spawn_effect_apple()
            
            self.update_boss()
            
            if self._frame_counter % 5 == 0:
                if self.quest_system and not self.boss_mode:
                    self.quest_system.quest_survival_time = time.time() - self.round_start_time
                    
                    leader = self.find_leader()
                    player = self.get_player_snake()
                    if leader and player and leader == player:
                        self.quest_system.quest_was_leader = True
                    
                    self.quest_system.update_progress()
                    
                    if self.quest_system.quest_completed and not self.quest_system.quest_reward_claimed:
                        reward = self.quest_system.claim_reward()
                        if reward > 0:
                            self.player_coins += reward
                            self.coins_earned_this_round += reward
            
            if self.boss_active and self.boss:
                self.move_boss()
                self.check_boss_collision_with_player()
            
            for snake in self.snakes:
                if snake['alive']:
                    now = time.time()
                    if now >= snake.get('immune_until', 0) and snake.get('original_color'):
                        if snake['color'] != snake['original_color']:
                            snake['color'] = snake['original_color']
                        if 'phase_effect' in snake:
                            snake['phase_effect'] = False
            
            snakes_to_process = [s for s in self.snakes if s['alive']]
            
            for snake in snakes_to_process:
                if not snake['alive']:
                    continue
                
                speed = 5
                
                if snake['label'] == 'Игрок' and self.is_accelerating:
                    if self.player_apple_count > 0:
                        speed = 15
                        if self._frame_counter % 3 == 0:
                            self.lose_apples_and_shrink(snake)
                
                elif snake['label'] != 'Игрок':
                    player = self.get_player_snake()
                    is_frozen = player and self.has_effect(player, 'freeze')
                    snake['frozen'] = is_frozen
                    
                    head_x, head_y = snake['position'][-1]
                    if player and player['alive']:
                        px, py = player['position'][-1]
                        dist_to_player = math.hypot(head_x - px, head_y - py)
                    else:
                        dist_to_player = 9999
                    
                    update_interval = 3 if dist_to_player < 1000 else 8
                    if is_frozen:
                        update_interval = 15
                    
                    if self._frame_counter % update_interval == 0:
                        snake['strategy_update_counter'] += 1
                        update_frequency = 5
                        
                        if snake['strategy'] in ['fleeing', 'attacking', 'searching_golden', 'searching_effect']:
                            update_frequency = 3
                        
                        if snake['strategy_update_counter'] >= update_frequency:
                            snake['strategy_update_counter'] = 0
                            self.update_bot_strategy(snake)
                    
                    self.steer_towards_target(snake)
                    self.avoid_obstacles(snake)
                    
                    if self._frame_counter % 5 == 0:
                        bot_speed_boost = self.has_effect(snake, 'speed')
                        
                        if snake['acceleration_cooldown'] == 0:
                            should_boost = False
                            if snake['strategy'] == 'fleeing':
                                should_boost = True
                            elif snake['strategy'] == 'attacking' and snake['target']:
                                target_x, target_y = snake['target']
                                if math.hypot(head_x - target_x, head_y - target_y) < 150:
                                    should_boost = True
                            elif snake['strategy'] == 'searching_golden':
                                should_boost = True
                            elif snake['strategy'] == 'searching_effect':
                                should_boost = True
                            
                            if should_boost and snake['eaten_apples'] > 0:
                                boost_speed = 15
                                if bot_speed_boost:
                                    boost_speed = int(boost_speed * 1.5)
                                speed = boost_speed
                                self.bot_loses_apples_and_shrink(snake)
                                snake['acceleration_cooldown'] = 10
                        else:
                            if bot_speed_boost:
                                speed = int(speed * 1.5)
                
                self.move_snake(snake, speed=speed)
                
                if snake['acceleration_cooldown'] > 0:
                    snake['acceleration_cooldown'] -= 1
            
            self.snakes = [s for s in self.snakes if s['alive'] or s['label'] == 'Игрок']
            
            self.draw_all()
            
            self.after_id = self.after(33, self.auto_move)
    
    def stop_auto_move(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
    
    def on_mouse_click(self, event):
        if hasattr(self, 'pause_button') and self.pause_button and self.pause_button.is_paused:
            return
        
        if not self.is_game_running:
            return
        
        player_snake = self.get_player_snake()
        if player_snake and not self.joystick_active:
            world_x = event.x + self.camera_x
            world_y = event.y + self.camera_y
            snake_head_x, snake_head_y = player_snake['position'][-1]
            
            dx = world_x - snake_head_x
            dy = world_y - snake_head_y
            angle = math.degrees(math.atan2(dy, dx))
            
            if self.quest_system:
                self.quest_system.track_direction_change(angle % 360)
            
            player_snake['direction_angle'] = angle % 360
    
    def start_acceleration(self):
        if self.player_apple_count > 0:
            self.is_accelerating = True
            if self.quest_system:
                self.quest_system.quest_boosts_used += 1
    
    def stop_acceleration(self):
        self.is_accelerating = False
    
    def lose_apples_and_shrink(self, snake):
        if snake['eaten_apples'] > 0:
            loss_rate = min(2, snake['eaten_apples'])
            
            for _ in range(loss_rate):
                if snake['eaten_apples'] <= 0:
                    break
                snake['eaten_apples'] -= 1
                self.player_apple_count -= 1
            
            target_length = 1 + snake['eaten_apples']
            
            while len(snake['position']) > target_length:
                tail_pos = snake['position'].pop(0)
                if random() < 0.3:
                    self.spawn_apples_at_point(*tail_pos)
    
    def bot_loses_apples_and_shrink(self, snake):
        if snake['eaten_apples'] > 0:
            snake['eaten_apples'] -= 1
            
            target_length = 1 + snake['eaten_apples']
            
            while len(snake['position']) > target_length:
                tail_pos = snake['position'].pop(0)
                if random() < 0.2:
                    self.spawn_apples_at_point(*tail_pos)
    
    def spawn_apples_at_point(self, x, y):
        self.apples.append((x, y))
    
    def find_leader(self):
        max_apples = -1
        leader = None
        for snake in self.snakes:
            if snake['alive'] and snake['eaten_apples'] > max_apples:
                max_apples = snake['eaten_apples']
                leader = snake
        return leader


if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeGame(master=root)
    app.mainloop()
