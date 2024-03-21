import Physics
import random

def nudge():
    return random.uniform(-1.5, 1.5)

table = Physics.Table()

pos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH * 0.75)
cueball = Physics.StillBall(0, pos)

pos.x = Physics.TABLE_WIDTH/2
pos.y = Physics.TABLE_WIDTH/2
ball1 = Physics.StillBall(1, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball9 = Physics.StillBall(9, pos)
pos9 = pos

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball2 = Physics.StillBall(2, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball11 = Physics.StillBall(11, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball5 = Physics.StillBall(5, pos)

pos.x = Physics.TABLE_WIDTH/2 + Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y = Physics.TABLE_WIDTH/2 + Physics.BALL_DIAMETER/2 + 2 + nudge()
ball10 = Physics.StillBall(10, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball8 = Physics.StillBall(8, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball4 = Physics.StillBall(4, pos)

pos.x -= Physics.BALL_DIAMETER/2 + 2 + nudge()
pos.y -= Physics.BALL_DIAMETER/2 + 2 + nudge()
ball14 = Physics.StillBall(14, pos)

table += cueball
table += ball1
table += ball2

table += ball4
table += ball5

table += ball8

table += ball10
table += ball11

table += ball14


with open("table.svg", "w") as file:
    file.write(table.svg())