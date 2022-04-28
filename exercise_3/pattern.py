import turtle
t = turtle.Turtle()
t.hideturtle()
#SQUARE
side = 40
t.left(45)
for i in range(4):
   t.forward(side)
   t.left(90)


t.penup()
t.sety(-5)
t.setx(32)
t.pendown()
#CIRCLE
radius = 45
t.circle(radius)

#HEXAGON
t.right(45)
t.penup()
t.sety(80)
t.setx(-30)
t.pendown()
side=60
for i in range(6):
   t.forward(side)
   t.left(300)

turtle.done()   