import Physics
import random
from math import sqrt

def nudge():
    return random.uniform(-1.5, 1.5)

def CreateTable():

    table = Physics.Table()

    pos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH * 0.75)
    cueball = Physics.StillBall(0, pos)

    pos.x = Physics.TABLE_WIDTH/2
    pos.y = Physics.TABLE_WIDTH/2
    ball1 = Physics.StillBall(1, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball9 = Physics.StillBall(9, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball2 = Physics.StillBall(2, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball11 = Physics.StillBall(11, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball5 = Physics.StillBall(5, pos)

    pos.x = Physics.TABLE_WIDTH/2 + ((Physics.BALL_DIAMETER + 4)/2 + nudge())
    pos.y = Physics.TABLE_WIDTH/2 - (sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge())
    ball10 = Physics.StillBall(10, pos)
    pos10 = Physics.Coordinate(pos.x, pos.y)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball8 = Physics.StillBall(8, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball4 = Physics.StillBall(4, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball14 = Physics.StillBall(14, pos)

    pos = pos10
    pos.x += (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball3 = Physics.StillBall(3, pos)
    pos3 = Physics.Coordinate(pos.x, pos.y)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball12 = Physics.StillBall(12, pos)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball6 = Physics.StillBall(6, pos)

    pos = pos3
    pos.x += (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball13 = Physics.StillBall(13, pos)
    pos13 = Physics.Coordinate(pos.x, pos.y)

    pos.x -= (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball15 = Physics.StillBall(15, pos)

    pos = pos13
    pos.x += (Physics.BALL_DIAMETER + 4)/2 + nudge()
    pos.y -= sqrt(3.0)/2.0*(Physics.BALL_DIAMETER + 4) + nudge()
    ball7 = Physics.StillBall(7, pos)

    table += cueball
    table += ball1
    table += ball2
    table += ball3
    table += ball4
    table += ball5
    table += ball6
    table += ball7
    table += ball8
    table += ball9
    table += ball10
    table += ball11
    table += ball12
    table += ball13
    table += ball14
    table += ball15

    return table

if __name__ == "__main__":
    with open("table.svg", "w") as file:
        file.write(CreateTable().svg())