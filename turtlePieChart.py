from turtle import Turtle, Screen
from itertools import cycle
import sys

#plotz =[('3391', 8), ('4444', 9), ('3392', 9), ('3390', 9), ('8080', 15), ('5555', 28), ('81', 71), ('3389', 158)]
COLORS = cycle(['yellow', 'green', 'red', 'cyan', 'orchid', 'blue', 'mediumpurple', 'lime'])

def pie(some_turtle):
    if (some_turtle.ds):
        plotz = some_turtle.ds
    else:
        plotz =[('61.19.82.166', 114), ('37.49.229.202', 45), ('71.83.6.18', 16)]
    if(some_turtle.rad):
        RADIUS = some_turtle.rad
    else: RADIUS = 275
    LABEL_RADIUS = RADIUS * 1.15
    FONTSIZE = 8
    FONT = ("Ariel", FONTSIZE, "bold")
    total = sum(fraction for _, fraction in plotz)  # data doesn't sum to 100 so adjust
    some_turtle.penup()# The pie slices
    some_turtle.sety(-RADIUS)
    some_turtle.pendown()
    for label, fraction in plotz:
        #try:#IP address
            #if fraction < 2:c = '169.169.169'
            #c = label.split('.')
            #some_turtle.fillcolor(int(c[0]),int(c[1]),int(c[2]))
        #except IndexError:
        some_turtle.fillcolor(next(COLORS))
        some_turtle.begin_fill()
        some_turtle.circle(RADIUS, fraction * 360 / total)
        position = some_turtle.position()
        some_turtle.goto(0, 0)
        some_turtle.end_fill()
        some_turtle.setposition(position)
    some_turtle.penup()# The labels
    if 'lable':
        some_turtle.sety(-LABEL_RADIUS)
        for label, fraction in plotz:
            some_turtle.circle(LABEL_RADIUS, fraction * 360 / total / 2)
            if fraction<10:some_turtle.write('.', align="center", font=FONT)
            else:some_turtle.write(label+':'+str(fraction), align="center", font=FONT)
            some_turtle.circle(LABEL_RADIUS, fraction * 360 / total / 2)
        some_turtle.hideturtle()
    
if __name__ == "__main__":
    leo = Turtle(shape="turtle")
    leo.ht()
    leo.speed(10)
    leo.penup()
    tp = (0,-300)
    leo.setposition(tp)
    leo.rad = 450
    window = Screen()
    window.setup(1200, 1024)
    window.bgcolor("white smoke")
    window.colormode(255)
    leo.ds =[('61.19.82.166', 114), ('37.49.229.202', 45), ('71.83.6.18', 16)]
    pie(leo)
    window.exitonclick()
