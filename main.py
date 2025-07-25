from tkinter import*
import random

game_width = 1600
game_height = 800
speed = 70
space_size = 50
body_parts = 3
snake_colour = "Light Green"
food_colour = "Red"
background_color = "Black"

class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = [] 

        for i in range(0, body_parts):
            self.coordinates.append([0,0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+space_size, y+space_size, fill=snake_colour, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        margin = 100
        # Calculate the maximum number of grid positions that fit in the safe area
        min_x = margin // space_size
        max_x = (game_width - margin) // space_size - 1
        min_y = margin // space_size
        max_y = (game_height - margin) // space_size - 1

        while True:
            grid_x = random.randint(min_x, max_x)
            grid_y = random.randint(min_y, max_y)
            x = grid_x * space_size
            y = grid_y * space_size

            position_occupied = False
            for segment in snake.coordinates:
                if segment[0] == x and segment[1] == y:
                    position_occupied = True
                    break

            if not position_occupied:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_colour, tag="food")


def next_turn(snake):
    global score, food
    
    x,y = snake.coordinates[0]

    if direction == "up":
        y -= space_size
    
    elif direction == "down":
        y += space_size
        
    elif direction == "left":
        x -= space_size
    
    elif direction == "right":
        x += space_size

    snake.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x, y, x+space_size, y+space_size, fill=snake_colour)
    
    snake.squares.insert(0,square)



    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(speed, next_turn, snake) 


def change_direction(new_direction):
    global direction 
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

    

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= game_width:
        return True
    elif y < 0 or y >= game_height:
        return True
    
    # Check if snake collides with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_reqwidth()/2, canvas.winfo_reqheight()/2,
                      font=('Times New Roman', 70), text="GAME OVER", fill="red", tag="gameover") 

window = Tk()
window.title("Snake Game")
window.resizable(False,False)

score = 0
direction = "down"
label = Label(window, text="Score {}".format(score), font=("Times New Roman", 40))
label.pack()

canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width /2))
y = int((screen_height/2) - (window_height /2))

window.geometry(f"{game_width}x{game_height}+{x}+{y}")

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

snake = Snake()
food = Food()

next_turn(snake)

window.mainloop()