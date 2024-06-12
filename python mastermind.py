import tkinter as tk
from random import choice, shuffle

class MastermindGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Game")

        self.colors = ["pink", "yellow", "green", "red", "blue", "white"]
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=400, height=600, bg='saddlebrown')
        self.canvas.pack()

        self.pegs = [[None for _ in range(4)] for _ in range(10)]
        self.hints = [[None for _ in range(4)] for _ in range(10)]

        for row in range(10):
            for col in range(4):
                self.pegs[row][col] = self.canvas.create_oval(
                    50 * col + 50, 50 * (10 - row) + 50, 50 * col + 90, 50 * (10 - row) + 90, fill="gray")
                self.hints[row][col] = self.canvas.create_oval(
                    50 * col + 270, 50 * (10 - row) + 50, 50 * col + 290, 50 * (10 - row) + 70, fill="white")

        self.color_buttons = {}
        for i, color in enumerate(self.colors):
            button = tk.Button(self.root, bg=color, command=lambda c=color: self.select_color(c))
            button.place(x=50 * i + 50, y=520, width=40, height=40)
            self.color_buttons[color] = button

        self.guess_button = tk.Button(self.root, text="Make Guess", command=self.make_guess)
        self.guess_button.place(x=300, y=520, width=80, height=40)

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game)
        self.reset_button.place(x=300, y=570, width=80, height=40)

    def reset_game(self):
        self.code = [choice(self.colors) for _ in range(4)]
        self.current_guess = []
        self.current_row = 0
        for row in range(10):
            for col in range(4):
                self.canvas.itemconfig(self.pegs[row][col], fill="gray")
                self.canvas.itemconfig(self.hints[row][col], fill="white")
        self.canvas.delete("message")

    def select_color(self, color):
        if len(self.current_guess) < 4:
            self.current_guess.append(color)
            self.canvas.itemconfig(self.pegs[self.current_row][len(self.current_guess) - 1], fill=color)

    def make_guess(self):
        if len(self.current_guess) == 4:
            feedback = self.get_feedback(self.current_guess)
            shuffle(feedback)
            for i, hint in enumerate(feedback):
                self.canvas.itemconfig(self.hints[self.current_row][i], fill=hint)

            if feedback == ["black"] * 4:
                self.end_game("You won!")
            elif self.current_row == 9:
                self.end_game("You lost!")

            self.current_guess = []
            self.current_row += 1

    def get_feedback(self, guess):
        feedback = []
        code_copy = self.code[:]
        guess_copy = guess[:]

        for i in range(4):
            if guess[i] == code_copy[i]:
                feedback.append("black")
                code_copy[i] = guess_copy[i] = None

        for i in range(4):
            if guess_copy[i] and guess_copy[i] in code_copy:
                feedback.append("white")
                code_copy[code_copy.index(guess_copy[i])] = None

        return feedback + ["white"] * (4 - len(feedback))

    def end_game(self, message):
        self.canvas.create_text(200, 550, text=message, font=("Arial", 24), fill="red", tags="message")
        if message == "You lost!":
            for i, color in enumerate(self.code):
                self.canvas.create_oval(
                    50 * i + 50, 50 * (10 - self.current_row) + 50, 50 * i + 90, 50 * (10 - self.current_row) + 90, fill=color, tags="message"
                )

if __name__ == "__main__":
    root = tk.Tk()
    game = MastermindGame(root)
    root.mainloop()
