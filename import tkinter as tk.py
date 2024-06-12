import tkinter as tk
from tkinter import ttk
import random

class SnakeGame:
    def __init__(self, root, player_name, difficulty):
        self.root = root
        self.root.title("Snake Game")
        self.player_name = player_name
        self.difficulty = difficulty
        self.set_speed()
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.control_frame = tk.Frame(root, bg="black")
        self.control_frame.pack()

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10, background="black", foreground="green")

        self.up_button = ttk.Button(self.control_frame, text="Up", command=self.move_up, style="TButton")
        self.up_button.grid(row=0, column=1, padx=5, pady=5)
        self.left_button = ttk.Button(self.control_frame, text="Left", command=self.move_left, style="TButton")
        self.left_button.grid(row=1, column=0, padx=5, pady=5)
        self.down_button = ttk.Button(self.control_frame, text="Down", command=self.move_down, style="TButton")
        self.down_button.grid(row=1, column=1, padx=5, pady=5)
        self.right_button = ttk.Button(self.control_frame, text="Right", command=self.move_right, style="TButton")
        self.right_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.snake = [(200, 200), (190, 200), (180, 200)]
        self.snake_dir = "Right"
        self.food = self.create_food()
        self.game_running = True
        self.score = 0

        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def set_speed(self):
        if self.difficulty == "Easy":
            self.speed = 150
        elif self.difficulty == "Medium":
            self.speed = 100
        elif self.difficulty == "Hard":
            self.speed = 50

    def create_food(self):
        while True:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        if event.keysym == "Up" and self.snake_dir != "Down":
            self.snake_dir = "Up"
        elif event.keysym == "Down" and self.snake_dir != "Up":
            self.snake_dir = "Down"
        elif event.keysym == "Left" and self.snake_dir != "Right":
            self.snake_dir = "Left"
        elif event.keysym == "Right" and self.snake_dir != "Left":
            self.snake_dir = "Right"

    def move_up(self):
        if self.snake_dir != "Down":
            self.snake_dir = "Up"

    def move_down(self):
        if self.snake_dir != "Up":
            self.snake_dir = "Down"

    def move_left(self):
        if self.snake_dir != "Right":
            self.snake_dir = "Left"

    def move_right(self):
        if self.snake_dir != "Left":
            self.snake_dir = "Right"

    def update(self):
        if not self.game_running:
            self.root.destroy()
            game_over_window(self.player_name, self.score)
            return

        new_head = self.move_snake()
        if self.check_collision(new_head):
            self.game_running = False
        else:
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.food = self.create_food()
                self.score += 1
            else:
                self.snake.pop()

            self.redraw()

        self.root.after(self.speed, self.update)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_dir == "Up":
            head_y -= 10
        elif self.snake_dir == "Down":
            head_y += 10
        elif self.snake_dir == "Left":
            head_x -= 10
        elif self.snake_dir == "Right":
            head_x += 10
        return (head_x, head_y)

    def check_collision(self, new_head):
        x, y = new_head
        return (x < 0 or x >= 400 or y < 0 or y >= 400 or new_head in self.snake)

    def redraw(self):
        self.canvas.delete(tk.ALL)
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")
        x, y = self.food
        self.canvas.create_oval(x, y, x + 10, y + 10, fill="red")
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

def start_game():
    player_name = name_entry.get()
    difficulty = difficulty_var.get()
    start_window.destroy()
    root = tk.Tk()
    game = SnakeGame(root, player_name, difficulty)
    root.mainloop()

def save_high_score(player_name, score):
    with open("high_scores.txt", "a") as file:
        file.write(f"{player_name}: {score}\n")

def get_previous_high_score():
    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
            if lines:
                return max([int(line.split(": ")[1].strip()) for line in lines])
            else:
                return 0
    except FileNotFoundError:
        return 0

def display_high_scores():
    high_scores_win = tk.Tk()
    high_scores_win.title("High Scores")
    high_scores_win.geometry("300x250")
    high_scores_win.configure(bg="black")

    high_scores_label = tk.Label(high_scores_win, text="High Scores", font=("Arial", 16), bg="black", fg="white")
    high_scores_label.pack(pady=20)

    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
            scores = [line.strip().split(": ") for line in lines]
            scores.sort(key=lambda x: int(x[1]), reverse=True)
            for player, score in scores:
                player_label = tk.Label(high_scores_win, text=f"{player}: {score}", font=("Arial", 12), bg="black", fg="white")
                player_label.pack()
    except FileNotFoundError:
        no_scores_label = tk.Label(high_scores_win, text="No high scores yet.", font=("Arial", 12), bg="black", fg="white")
        no_scores_label.pack()

    high_scores_win.mainloop()

def game_over_window(player_name, score):
    previous_high_score = get_previous_high_score()
    save_high_score(player_name, score)

    game_over_win = tk.Tk()
    game_over_win.title("Game Over")
    game_over_win.geometry("300x250")
    game_over_win.configure(bg="black")

    game_over_label = tk.Label(game_over_win, text="Game Over", font=("Arial", 16), bg="black", fg="white")
    game_over_label.pack(pady=20)

    player_name_label = tk.Label(game_over_win, text=f"Player: {player_name}", font=("Arial", 14), bg="black", fg="white")
    player_name_label.pack(pady=5)

    score_label = tk.Label(game_over_win, text=f"Score: {score}", font=("Arial", 14), bg="black", fg="white")
    score_label.pack(pady=5)

    previous_high_score_label = tk.Label(game_over_win, text=f"Previous High Score: {previous_high_score}", font=("Arial", 14), bg="black", fg="white")
    previous_high_score_label.pack(pady=5)

    high_scores_button = ttk.Button(game_over_win, text="High Scores", command=display_high_scores, style="TButton")
    high_scores_button.pack(pady=10)

    game_over_win.mainloop()

# Start window
start_window = tk.Tk()
start_window.title("Start Snake Game")
start_window.geometry("300x300")
start_window.configure(bg="black")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, background="black", foreground="green")

start_label = tk.Label(start_window, text="Welcome to Snake Game", font=("Arial", 16), bg="black", fg="white")
start_label.pack(pady=20)

name_label = tk.Label(start_window, text="Enter your name:", font=("Arial", 12), bg="black", fg="white")
name_label.pack(pady=5)
name_entry = tk.Entry(start_window, font=("Arial", 12))
name_entry.pack(pady=5)

difficulty_label = tk.Label(start_window, text="Select difficulty:", font=("Arial", 12), bg="black", fg="white")
difficulty_label.pack(pady=5)
difficulty_var = tk.StringVar(value="Easy")
difficulty_menu = ttk.OptionMenu(start_window, difficulty_var, "Easy", "Easy", "Medium", "Hard")
difficulty_menu.pack(pady=5)

start_button = ttk.Button(start_window, text="Start Game", command=start_game, style="TButton")
start_button.pack(pady=20)

start_window.mainloop()
