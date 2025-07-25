import tkinter as tk
import random

# Game settings
GAME_WIDTH = 1280
GAME_HEIGHT = 720
SPEED = 70
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "Light Green"
FOOD_COLOR = "Red"
BG_COLOR = "Black"
MARGIN = 200  # Fruit will not spawn within 200px of the right/bottom edge

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas, snake):
        min_x = 0
        max_x = (GAME_WIDTH - MARGIN) // SPACE_SIZE - 1
        min_y = 0
        max_y = (GAME_HEIGHT - MARGIN) // SPACE_SIZE - 1
        while True:
            grid_x = random.randint(min_x, max_x)
            grid_y = random.randint(min_y, max_y)
            x = grid_x * SPACE_SIZE
            y = grid_y * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break
        self.coordinates = [x, y]
        self.oval = canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food, canvas, label, window):
    global direction, score, game_running
    if not game_running:
        return
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food(canvas, snake)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over(canvas)
        return
    window.after(SPEED, next_turn, snake, food, canvas, label, window)

def change_direction(new_direction):
    global direction
    opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
    if new_direction != opposites.get(direction):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over(canvas):
    global game_running
    game_running = False
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=("Times New Roman", 100), text="GAME OVER", fill="red", tag="gameover")

def main():
    global direction, score, game_running
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)
    score = 0
    direction = "down"
    game_running = True
    label = tk.Label(window, text=f"Score: {score}", font=("Times New Roman", 40))
    label.pack()
    canvas = tk.Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()
    window.update()
    # Center window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}")
    # Controls
    window.bind("<a>", lambda event: change_direction("left"))
    window.bind("<d>", lambda event: change_direction("right"))
    window.bind("<w>", lambda event: change_direction("up"))
    window.bind("<s>", lambda event: change_direction("down"))
    window.bind("<A>", lambda event: change_direction("left"))
    window.bind("<D>", lambda event: change_direction("right"))
    window.bind("<W>", lambda event: change_direction("up"))
    window.bind("<S>", lambda event: change_direction("down"))
    window.bind("<Left>", lambda event: change_direction("left"))
    window.bind("<Right>", lambda event: change_direction("right"))
    window.bind("<Up>", lambda event: change_direction("up"))
    window.bind("<Down>", lambda event: change_direction("down"))
    # Game objects
    global snake
    snake = Snake(canvas)
    food = Food(canvas, snake)
    next_turn(snake, food, canvas, label, window)
    window.mainloop()

if __name__ == "__main__":
    main()
