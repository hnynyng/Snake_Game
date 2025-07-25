from tkinter import *
import random

# Game constants
game_width = 1280  # Width of the game window
game_height = 720 # Height of the game window
speed = 70  # Speed of the game (milliseconds per turn)
space_size = 50  # Size of each grid cell
body_parts = 3  # Initial size of the snake
snake_colour = "#00FF00"  # Snake color (light green)
food_colour = "#FF0000"  # Food color (red)
background_color = "#000000"  # Background color (black)

# Initialize global variables
score = 0
direction = "down"
snake = None
food = None


class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        # Initialize the snake's starting position
        for i in range(0, body_parts):
            self.coordinates.append([0, 0])

        # Draw the snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_colour, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        # Calculate maximum grid indices
        max_x = (game_width // space_size) - 1
        max_y = (game_height // space_size) - 1

        # Generate random grid-aligned coordinates
        x = random.randint(0, max_x) * space_size
        y = random.randint(0, max_y) * space_size

        # Store the coordinates
        self.coordinates = [x, y]

        # Draw the food on the canvas
        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_colour, tag="food")


def next_turn():
    global score, food

    # Get the current head position
    x, y = snake.coordinates[0]

    # Update the head position based on the direction
    if direction == "up":
        y -= space_size
    elif direction == "down":
        y += space_size
    elif direction == "left":
        x -= space_size
    elif direction == "right":
        x += space_size

    # Insert the new head position
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_colour, tag="snake")
    snake.squares.insert(0, square)

    # Check if the snake eats the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")

        # Delete the old food and spawn new food
        canvas.delete("food")
        food = Food()
    else:
        # Remove the tail of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions():
        game_over()
    else:
        # Schedule the next turn
        window.after(speed, next_turn)


def change_direction(new_direction):
    global direction

    # Prevent reversing direction (e.g., moving left while going right)
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions():
    x, y = snake.coordinates[0]

    # Check for wall collisions
    if x < 0 or x >= game_width or y < 0 or y >= game_height:
        return True

    # Check for self-collisions
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    # Clear the canvas
    canvas.delete(ALL)

    # Display "GAME OVER" text
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )


# Main window setup
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Score label
label = Label(window, text=f"Score: {score}", font=("consolas", 40))
label.pack()

# Canvas setup
canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

# Center the window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind keyboard events
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Add WASD key bindings
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))
window.bind("<A>", lambda event: change_direction("left"))  # Support for uppercase letters
window.bind("<D>", lambda event: change_direction("right"))
window.bind("<W>", lambda event: change_direction("up"))
window.bind("<S>", lambda event: change_direction("down"))

# Initialize the snake and food
snake = Snake()
food = Food()

# Start the game loop
next_turn()

# Run the main event loop
window.mainloop()