import tkinter as tk 
import turtle
import time
import random
from pygame import mixer

#code of the background
from PIL import ImageTk
from PIL import Image

root = tk.Tk()

mixer.init()    # initializing the mixer


root.title('Snake Game')
root.state('zoomed')
root.iconbitmap(r'C:/Users/Ossama/Desktop/project/favicon (1).ico')

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Frame Jungle 
nightImage = Image.open('C:/Users/Ossama/Desktop/project/jungle.jpg')
nightImage = nightImage.resize((width,height),Image.ANTIALIAS)
resized1 = ImageTk.PhotoImage(nightImage)

backgroundLabel = tk.Label(root,image = resized1)
backgroundLabel.place(x=0,y=0)

#Create a turtle screen 
canvas = tk.Canvas(root,width=600, height=600)
turtle_screen=turtle.TurtleScreen(canvas)
turtle_screen.bgcolor('#ffe6cc')
canvas.pack(pady=70)

# Win sound
def Win_music():
    mixer.music.load("win (online-audio-converter.com).wav")
    mixer.music.play()

# Game over sound
def game_over_music():
    mixer.music.load("game Over (online-audio-converter.com).wav")
    mixer.music.play()

# eat sound
def eat_music():
    mixer.music.load("eat (online-audio-converter.com).wav")
    mixer.music.play()

# SCORE 
global score
score = 0

# Display Score
def display_Score():
    w =tk.Label(root,text="Score: {}".format(score),
                font=('Arial',40,'bold'),
                fg='white',
                bg='#001e3a',
                bd=0,
                padx=50,
                pady=10)
    w.place(x=1100,y=100)

# Display High Score
def display_H_score():
    w =tk.Label(root,text="High Score: {}".format(high_score.read_H_score()),
                font=('Arial',30,'bold'),
                fg='#001e3a',
                bd=0,
                padx=50,
                pady=10,)
    w.place(x=1100,y=200)

class High_score:

    # Write the score
    def write_score(self, sc):
        write = open("C:/Users/Ossama/Desktop/project/High Score.txt","w")
        write.write(str(sc))
        write.close()

    # Read High Score
    def read_H_score(self):
        self.read = open("C:/Users/Ossama/Desktop/project/High Score.txt","r")
        for line in self.read:
            self.score_str = int(line)
        self.read.close()
        return self.score_str

# Snake head
head = turtle.RawTurtle(turtle_screen)
head.shape("circle")
head.color("#33691e")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.RawTurtle(turtle_screen)
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = [] 

# Add segment
def add_segment():
    new_segment = turtle.RawTurtle(turtle_screen)
    new_segment.speed(0)
    new_segment.shape("circle")
    new_segment.color('#76ff03')
    new_segment.penup()
    segments.append(new_segment)

# Functions
def go_up():
    head.direction = "up"
    
def go_down():
    head.direction = "down"
    
def go_left():
    head.direction = "left"
    
def go_right():
    head.direction = "right"    
    
    
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
        
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
        
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bingings

turtle_screen.listen()
turtle_screen.onkeypress(go_up,"w")
turtle_screen.onkeypress(go_down,"s")
turtle_screen.onkeypress(go_right,"d")
turtle_screen.onkeypress(go_left,"a")

turtle_screen.onkeypress(go_up,"W")
turtle_screen.onkeypress(go_down,"S")
turtle_screen.onkeypress(go_right,"D")
turtle_screen.onkeypress(go_left,"A")

#Main game loop 
while True:
    
    root.update()
    move()
    high_score = High_score()
    # Check for a collision with border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        if high_score.read_H_score() <= score:
            Win_music()
            turtle_screen.bgcolor('#4bf035')
        else:
            game_over_music()
            turtle_screen.bgcolor('red')

        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"
        turtle_screen.bgcolor('#ffe6cc')
        score = 0
        display_Score()
        
        # Hide the segment list 
        for segment in segments:
            segment.goto(1000,1000)
        # Clear the segment list
            segments = []
            
        
    # Check for head collision with the body segments (Eat yourself) 
    for index, segment in enumerate(segments):
        if(index > 1):
            # Check for collision with segment 
            if head.distance(segment) < 20:
                if high_score.read_H_score() <= score:
                    Win_music()
                    turtle_screen.bgcolor('#4bf035')
                else:
                    game_over_music()
                    turtle_screen.bgcolor('red')
                time.sleep(1)
                head.goto(0,0)
                head.direction = "stop"
                # Clear the segment list
                segments = []
                score = 0
                turtle_screen.bgcolor('#ffe6cc')
                display_Score()
                
                  
    
    
    # Check for collision with food 
    if head.distance(food) < 20:
        eat_music()
        # Move the food to a random spot
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        food.goto(x,y)
        # Add a segment 
        if score == 0:
            add_segment()
        add_segment()
        score += 10
        display_Score()

    # Move the eng segment first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x,y)
        
    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)
    
    # Check High Score
    if high_score.read_H_score() <= score:
        high_score.write_score(score)
        display_H_score()

    time.sleep(0.1)


root.mainloop()